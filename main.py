import utils
import spectrum
import spectrum_analysis_model as sam
import activity
from file_handler import FileHandler
from extract_dicom_spectrum import extract_sum
import argparse
import physics
import known_sources as ks
import datetime
import radiumlog
import shutil, os
import numpy as np
import math


#   Setup

#   Where we look for dicom files
pardir = 'Y:\\Radium\\Data\\'
archdir = 'Y:\\Radium\\Archive\\'

#	Whether to look for the known source (and background) in "pardir"
#	instead of the standard location
use_own_source = False



print('')
print(' -------  RADEX -------')
print(''); print('')



#   Prepare file handler and discover all dicom files in the main directory
fh = FileHandler(pardir)
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

#	Remove background from list of descriptions
descr.remove(bkg_descr)


print('Alle resterende serier vil blive analyseret med den valgte baggrund.')
input("Tryk Enter for at fortsætte...")
print('')
print('')


print('Analyserer baggrund...')
print('')

# Fetch spectra for background
bkg_files = fh.files(bkg_descr) # List of files for background
bkg_spec = extract_sum(bkg_files)


# Measure sensitivity from known sources
(sens,dsens) = ks.sensitivity()


# Prepare Spectrum Analysis Model
m = sam.SpectrumAnalysisModel()
m.set_windows(physics.windows['Ra223'])
m.set_background(bkg_spec)
m.set_sensitivity(sens, dsens)



# Calculate detection limit/MDA and report to user
mda = m.detection_limit()/sens

print('Følsomhed: {:.3f} +/- {:.3f} cps/Bq'.format(sens,dsens))
#print('Kritisk niveau: {:.0f}Bq'.format(m.critical_level()/sens))
print('MDA:       {:.0f}Bq'.format(mda))
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

	m.set_spectrum(ser_spec)
	res = m.analyse_spectrum()
	act = res.net_signal
	conf_act = res.conf
	if res.detected:
		# Signal above critical level

		print('   Netto aktivitet: {:.0f} +/- {:.0f}Bq'.format(act,conf_act))

		if (act+conf_act) >  physics.acc_act['Ra223']:
			# Net activity above acceptable level, calculate disposal date
			decay_days = activity.decay(
				act+conf_act, physics.acc_act['Ra223'], physics.half_life['Ra223'])
			mdate = ser_spec.mdate # Date of measurement
			decay_date = mdate + datetime.timedelta(days=decay_days)
			print('   Bortskaffelse d. {}'.format(decay_date.strftime('%d-%m-%Y')))
			print('')

			# Query user to write to log file
			yn = utils.list_choose("Hvis du synes at beregningen ser rigtig ud og den skal "
															"gemmes, skal den skrives til loggen.",
															"Gem til log?", ['Nej','Ja'])
			if yn == 1:
				radiumlog.write(mdate, des, mda, sens, act+conf_act,
					decay_days, decay_date)

		else:
			print('   Aktiviteten er under det maksimalt accepterede niveau. '
								'Kan bortskaffes nu.')

	else:
		print('Ingen aktivitet registreret (øvre grænse: {:.0f}Bq)'.format(act+conf_act))
		print('Kan bortskaffes nu.')


	print('')
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
	# Recreate parent directory without contents
	os.makedirs(pardir, exist_ok=True)
