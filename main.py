import utils
import spectrum
import activity
from file_handler import FileHandler
from extract_dicom_spectrum import extract_spectrum
import argparse
import physics
import ra223sources
import datetime
import radiumlog
import shutil, os


#   Setup

#	Maximum allowed MDA [Bq] for usable energy windows:
max_mda = 100

#   Where we look for dicom files
pardir = 'C:\\Users\\bub8ga\\radex\\train\\DICOM\\'
archdir = 'C:\\Users\\bub8ga\\radex\\train\\archive\\'

#	Series description of known source and corresponding background
source = 'kilde 1'
source_bkg = 'Bg 2'

#	Activity of known source
src_act = ra223sources.activities[source]

#	Whether to look for the known source (and background) in "pardir"
#	instead of the standard location
use_own_source = False



print('')
print(' -------  RADEX -------')
print(''); print('')



#   Parse input arguments
parser = argparse.ArgumentParser()

parser.add_argument('-s',
    metavar='source_description',
	help='Series description of the known source. You can use one of the '
		 'standard sources (' + ', '.join(ra223sources.sources) + '), '
		 'or you can use your own source. If you use your own source, be sure '
		 'to specify the activity with the -S option. '
		 'Defaults to "'+ source + '".')

parser.add_argument('-S',
    metavar='activity',
    help='Signal to the program that the known source should be taken from the '
		 'measurements rather than the standard sources. The activity of the '
		 'source must be specified in [Bq].'
    )

parser.add_argument('-b',
    metavar='source_background_description',
	help='Series description of the background to subtract from the known '
		 'source. You can use one of the standard backgrounds '
		 '(' + ', '.join(ra223sources.backgrounds) + '). '
		 'If you use your own source (with the -S option) the background '
		 'chosen for the measurements will also be applied to the source, and '
		 'this option is ignored. '
		 'Defaults to "' + source_bkg + '".')


args = parser.parse_args()

if args.s is not None:
	# Use alternative source
	source = args.s
	if args.S is None:
		# Alternative source is a standard source, get activity
		src_act = ra223sources.activities[source]

if args.b is not None:
	# Use alternative background for source subtraction
	source_bkg = args.b

if args.S is not None:
	# Alternative source is supplied by user, get activity
	src_act = int(args.S)
	use_own_source = True




#   Prepare file handler and discover all dicom files in the main directory
fh = FileHandler(pardir)
fh.discover()


#   Get all descriptions discovered
descr = fh.descriptions()
if use_own_source:
    # If a source has been supplied, remove that from the list of descriptions
    descr.remove(source)
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

#	Remove background from list of descriptions
descr.remove(bkg_descr)


print('Alle resterende serier vil blive analyseret med den valgte baggrund.')
input("Tryk Enter for at fortsætte...")
print('')
print('')


print('Analyserer baggrund...')
print('')


#	Load known source
if use_own_source:
	# User supplied source (and background)
	src_bkg_files = fh.files(bkg_descr) # List of files for background
	src_files = fh.files(source) # List of files for source

	# Extract spectrum from first file
	src_bkg_spec = extract_spectrum(src_bkg_files[0])
	src_spec = extract_spectrum(src_files[0])
	for fn in src_bkg_files[1:]:
	    src_bkg_spec = spectrum.add(src_bkg_spec,extract_spectrum(fn)) # Add the other spectra

	for fn in src_files[1:]:
	    src_spec = spectrum.add(src_spec,extract_spectrum(fn))

	#   Subtract background from source
	src_spec = spectrum.subtract(src_spec,src_bkg_spec)
else:
	# Standard spectrum and background, load from file
	filename = ra223sources.source_spectra + source + '_' + source_bkg + '.txt'
	src_spec = spectrum.load_from_file(filename)


#   Fetch spectra for background
bkg_files = fh.files(bkg_descr) # List of files for background
bkg_spec = extract_spectrum(bkg_files[0]) # Extract for first file
for fn in bkg_files[1:]:
    bkg_spec = spectrum.add(bkg_spec,extract_spectrum(fn)) # Add the other spectra

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
    ser_spec = extract_spectrum(ser_files[0])
    for fn in ser_files[1:]:
        ser_spec = spectrum.add(ser_spec,extract_spectrum(fn))

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
                    "Gem til log?", ['Nej','Ja'])
        if yn == 1:
            radiumlog.write(mdate, des, window, mda[window], sens[window], max_act,
                decay_days, decay_date)



    else:
        print('Serie "{}" er ikke mærkbart forurenet.'.format(des))

    input("Tryk Enter for at fortsætte...")
    print('')
    print('')


archive = utils.list_choose(
    "Hvis du er færdig med at arbejde med disse data, kan du arkivere det.",
    "Arkiver data?", ['Nej','Ja'])

if archive == 1:
    arch_today_dir = archdir+datetime.date.today().isoformat()
    os.makedirs(arch_today_dir, exist_ok=True)
    shutil.move(pardir,arch_today_dir+'\\')
