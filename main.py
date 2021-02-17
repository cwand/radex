import utils
import spectrum
import activity
import file_handler
import extract_dicom_spectrum
import argparse
import physics
import ra223sources
import datetime
import radiumlog
import shutil, os


#   Setup

# Maximum allowed MDA:
max_mda = 100

#   Where we look for dicom files
pardir = 'C:\\Users\\bub8ga\\radex\\train\\DICOM\\'
archdir = 'C:\\Users\\bub8ga\\radex\\train\\archive\\'

src_description = 'kilde 2' # Series description on known source we use
src_background = 'Bg 2' # Series description on background of known source we use



print('')
print(' -------  RADEX -------')
print(''); print('')


#   Analysis of known source

#   Use file handler to discover all dicom files in the known source folder
srcfh = file_handler.FileHandler(ra223sources.known_source_dir)
srcfh.discover()

#   Load spectrum from known source and accompanying background
src_bkg_files = srcfh.files(src_background) # List of files for background
src_bkg_spec = extract_dicom_spectrum.extract_spectrum(src_bkg_files[0]) # Extract for first file
for fn in src_bkg_files[1:]:
    src_bkg_spec = spectrum.add(src_bkg_spec,extract_dicom_spectrum.extract_spectrum(fn)) # Add the other spectra

# ...and again for source
src_files = srcfh.files(src_description)
src_spec = extract_dicom_spectrum.extract_spectrum(src_files[0])
for fn in src_files[1:]:
    src_spec = spectrum.add(src_spec,extract_dicom_spectrum.extract_spectrum(fn))

#   Subtract background from source
src_spec = spectrum.subtract(src_spec,src_bkg_spec)

#   Get activity of known source
src_act = ra223sources.known_source_act[src_description]


#   Analysis of measurements

#   Prepare file handler and discover all dicom files in the main directory
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


print('Alle resterende serier vil blive analyseret med den valgte baggrund.')
input("Tryk Enter for at fortsætte...")
print('')
print('')


print('Analyserer baggrund...')
print('')

#   Fetch spectra for background
bkg_files = fh.files(bkg_descr) # List of files for background
bkg_spec = extract_dicom_spectrum.extract_spectrum(bkg_files[0]) # Extract for first file
for fn in bkg_files[1:]:
    bkg_spec = spectrum.add(bkg_spec,extract_dicom_spectrum.extract_spectrum(fn)) # Add the other spectra

sens = {}
mda = {}
windows = [] # Windows we will end up using

#   In each window, measure sensitivity and MDA
for window in physics.windows['Ra223']:
    print(' - {}keV - {}keV:'.format(window[0],window[1]))
    src_rate = src_spec.window_rate(window)
    sens[window] = src_rate/src_act
    mda[window] = activity.mda_simple(bkg_spec, sens[window], window)
    print('     MDA i vindue: {:.0f}Bq'.format(mda[window]))
    if mda[window] > max_mda:
        print('     Vindue ignoreres pga. dårlig MDA')
    else:
        windows.append(window)

    print('')

input("Tryk Enter for at fortsætte...")
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
    for window in windows:
        print(' - {}keV - {}keV:'.format(window[0],window[1]))
        ser_rate = ser_spec.window_rate(window)
        ser_act = ser_rate/sens[window]
        if ((ser_act >= max_act) and (ser_act >= mda[window])):
            max_act = ser_act
        print('     Net. aktivitet i vindue: {:.0f}Bq'.format(ser_act))

        print('')

    if (max_act > physics.acc_act['Ra223']):
        print('Aktivitet i serie "{}": {:.0f}Bq'.format(des, max_act))
        decay_days = activity.decay(
            max_act, physics.acc_act['Ra223'], physics.half_life['Ra223'])
        mdate = ser_spec.mdate # Date of measurement
        decay_date = mdate + datetime.timedelta(days=decay_days)
        print('Bortskaffelse d. {}'.format(decay_date.strftime('%d-%m-%Y')))
        print('')

        # Query user to write to log file
        yn = utils.list_choose("Hvis du synes at beregningen ser rigtig ud og den skal "
                    "gemmes, skal den skrives til loggen.",
                    "Gem til log?", ['Ja','Nej'])
        if yn == 0:
            radiumlog.write(mdate, des, window, mda[window], sens[window], max_act,
                decay_days, decay_date)



    else:
        print('Serie "{}" er ikke mærkbart forurenet.'.format(des))

    input("Tryk Enter for at fortsætte...")
    print('')
    print('')


archive = utils.list_choose(
    "Hvis du er færdig med at arbejde med disse data, kan du arkivere det.",
    "Arkiver data?", ['Ja','Nej'])

if archive == 0:
    arch_today_dir = archdir+datetime.date.today().isoformat()
    os.makedirs(arch_today_dir, exist_ok=True)
    shutil.move(pardir,arch_today_dir+'\\')
