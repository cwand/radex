import utils
import spectrum
import activity
import file_handler
import extract_dicom_spectrum
import argparse
import physics
import datetime
import radiumlog
import shutil, os


print('')
print(' -------  RADEX -------')
print(''); print('')


#   Setup

#   Where we look for dicom files
pardir = 'C:\\Users\\bub8ga\\radex\\train\\DICOM\\'
archdir = 'C:\\Users\\bub8ga\\radex\\train\\archive\\'

#   Prepare file handler and discover all dicom files in the directory
fh = file_handler.FileHandler(pardir)
fh.discover()



#   Get all descriptions discovered
descr = fh.descriptions()
if not descr:
    #   No dicom files found
    print('Der blev ikke fundet nogle målinger. Tjek at der ligger filer med '
          'endelsen .dcm i mappen ' + pardir + '. Filerne må gerne ligge i '
          'undermapper.')
    input("Tryk Enter for at afslutte programmet...")
    exit()



#   Query user for background spectrum to use from available descriptions
bkg_idx = utils.list_choose(
    'Hvilken serie skal benyttes som baggrund? (Skriv nummeret ud for den ønskede valgmulighed)',
    'Baggrundsserie: ',
    descr)
bkg_descr = descr[bkg_idx]
print('')
print('Du har valgt ' + bkg_descr + ' som baggrundsmåling!')
print('')

#   Remove chosen description from list og descriptions
descr.pop(bkg_idx)



#   Query user for known source spectrum to use from available descriptions
src_idx = utils.list_choose(
    'Hvilken serie skal benyttes som kilde? (Skriv nummeret ud for den ønskede valgmulighed)',
    'Kildeserie: ',
    descr)
src_descr = descr[src_idx]
print('')
print('Du har valgt ' + src_descr + ' som kilde!')
print('')

#   Remove chosen description from list of descriptions
descr.pop(src_idx)

#   Query user for activity of known source
print('Hvad er aktiviteten (Bq) af kilden?')
src_act = int(input("Aktivitet i Bq: "))
print('')


print('Alle resterende serier vil blive analyseret med den valgte baggrund '
        'og kilde.')
print('')
print('')



print('Analyserer kilde og baggrund...')
print('')

#   Fetch spectra for background and source
bkg_files = fh.files(bkg_descr) # List of files for background
bkg_spec = extract_dicom_spectrum.extract_spectrum(bkg_files[0]) # Extract for first file
for fn in bkg_files[1:]:
    bkg_spec = spectrum.add(bkg_spec,extract_dicom_spectrum.extract_spectrum(fn)) # Add the other spectra

# ...and again for source
src_files = fh.files(src_descr)
src_spec = extract_dicom_spectrum.extract_spectrum(src_files[0])
for fn in src_files[1:]:
    src_spec = spectrum.add(src_spec,extract_dicom_spectrum.extract_spectrum(fn))

#   Subtract background from source
src_spec = spectrum.subtract(src_spec,bkg_spec)

sens = {}
mda = {}

#   In each window, measure sensitivity and MDA
for window in physics.windows['Ra223']:
    print(' - {}keV - {}keV:'.format(window[0],window[1]))
    src_rate = src_spec.window_rate(window)
    print('     Kilde net. tællerate: {:.0f}cps'.format(src_rate))
    sens[window] = src_rate/src_act
    print('     Følsomhed i vindue: {:.3f}cps/Bq'.format(sens[window]))
    mda[window] = activity.mda_simple(bkg_spec, sens[window], window)
    print('     MDA i vindue: {:.0f}Bq'.format(mda[window]))

    print('')

print('')


#   Measure activity for each description
for des in descr:
    print('Analyserer serie "{}"'.format(des))
    print('')

    #   Load spectra
    ser_files = fh.files(des)
    ser_spec = extract_dicom_spectrum.extract_spectrum(ser_files[0])
    for fn in ser_files[1:]:
        ser_spec = spectrum.add(ser_spec,extract_dicom_spectrum.extract_spectrum(fn))

    #   Subtract background
    ser_spec = spectrum.subtract(ser_spec, bkg_spec)

    #   Go through windows:
    max_act = 0
    for window in physics.windows['Ra223']:
        print(' - {}keV - {}keV:'.format(window[0],window[1]))
        ser_rate = ser_spec.window_rate(window)
        ser_act = ser_rate/sens[window]
        if ((ser_act >= max_act) and (ser_act >= mda[window])):
            max_act = ser_act
        print('     Net. tællerate i vindue: {:.0f}cps'.format(ser_rate))
        print('     Net. aktivitet i vindue: {:.0f}Bq'.format(ser_act))

        print('')

    if (max_act > 0):
        print('Aktivitet i serie "{}": {:.0f}Bq'.format(des, max_act))
        decay_days = activity.decay(max_act, 300, physics.half_life['Ra223'])
        mdate = ser_spec.mdate # Date of measurement
        decay_date = mdate + datetime.timedelta(days=decay_days)
        print('Bortskaffelse d. {}'.format(decay_date.strftime('%d-%m-%Y')))
        print('')

        # Query user to write to log file
        yn = utils.list_choose("Hvis du synes at beregningen ser rigtig ud og den skal "
                    "gemmes, skal den skrives til loggen.",
                    "Gem til log?", ['Ja','Nej'])
        if yn == 0:
            radiumlog.write(mdate, des, mda[window], sens[window], max_act,
                decay_days, decay_date)



    else:
        print('Ingen aktivitet i serie "{}"'.format(des))

    input("Tryk Enter for at fortsætte...")
    print('')
    print('')


archive = utils.list_choose(
    "Hvis du er færdig med at arbejde med dette data, kan arkivere det.",
    "Arkiver data?", ['Ja','Nej'])

if archive == 0:
    arch_today_dir = archdir+datetime.date.today().isoformat()
    os.mkdir(arch_today_dir)
    shutil.move(pardir,arch_today_dir+'\\')
