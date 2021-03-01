import utils
import spectrum
import activity
from file_handler import FileHandler
from extract_dicom_spectrum import extract_sum
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

	# Extract the combined spectra (all files added)
	src_bkg_spec = extract_sum(src_bkg_files)
	src_spec = extract_sum(src_files)

else:
	# Standard spectrum and background, load from file
	src_spec = spectrum.load_from_file(ra223sources.source_spectra + source + '.txt')
	src_bkg_spec = spectrum.load_from_file(ra223sources.source_spectra + source_bkg + '.txt')


#   Fetch spectra for background
bkg_files = fh.files(bkg_descr) # List of files for background
bkg_spec = extract_sum(bkg_files)


# Calculate MDA and report to user
mda_res = activity.mda_analysis(bkg_spec, src_spec, src_bkg_spec, src_act, physics.windows['Ra223'])
print('MDA: {:.0f}Bq'.format(mda_res.mda))
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
	ser_spec = extract_sum(ser_files)


	act_res = activity.activity_analysis(
		bkg_spec,ser_spec, mda_res.sens, mda_res.dsens, physics.windows['Ra223'])
	print('     Net. aktivitet: {:.0f} +/- {:.0f}Bq'.format(act_res.act,act_res.dact))
	print('')

	if (act_res.act > physics.acc_act['Ra223']):
		print('Aktivitet i serie "{}": {:.0f}Bq'.format(des, act_res.act))
		decay_days = activity.decay(
			act_res.act, physics.acc_act['Ra223'], physics.half_life['Ra223'])
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
