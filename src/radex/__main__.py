import configparser
import datetime
import shutil
import os

import radex

#   Load configuration

config = configparser.ConfigParser()
config.read('config.ini')


print('')
print(' -------  RADEX -------')
print('')
print('')

# Prepare file handler and discover all dicom files in the main directory
fh = radex.FileHandler()
fh.discover()


#   Get all descriptions discovered
descr = fh.descriptions()
if not descr:
	#   No dicom files found
	print('Der blev ikke fundet nogle målinger. Tjek at der ligger filer med '
		'endelsen .dcm i mappen ' + config['dicom']['data'] + '. '
				'Filerne må gerne ligge i undermapper.')
	input('Tryk Enter for at afslutte programmet...')
	exit()


#   Query user for background spectrum to use from available descriptions
bkg_idx = radex.list_choose(
	'Hvilken serie skal benyttes som baggrund? (Skriv nummeret ud for den ønskede valgmulighed)',
	'Baggrundsserie: ',
	descr)
bkg_descr = descr[bkg_idx]
print('')
print('Du har valgt ' + bkg_descr + ' som baggrundsmåling!')
print('')

# Remove background from list of descriptions
descr.remove(bkg_descr)


print('Alle resterende serier vil blive analyseret med den valgte baggrund.')
input("Tryk Enter for at fortsætte...")
print('')
print('')


# Fetch spectra for background
bkg_files = fh.files(bkg_descr)  # List of files for background
bkg_spec = radex.extract_sum(bkg_files)


# Measure sensitivity from known sources
(sens, dsens) = radex.sensitivity()


# Prepare Spectrum Analysis Model
m = radex.SpectrumAnalysisModel(bkg_spec)
m.set_sensitivity(sens, dsens)
m.alpha = config.getfloat('stats', 'alpha', fallback=0.05)
m.beta = config.getfloat('stats', 'beta', fallback=0.05)
m.gamma = config.getfloat('stats', 'gamma', fallback=0.05)

# Calculate detection limit/MDA and report to user
mda = m.detection_limit() / sens
ra223 = radex.Radium223()

if config['settings']['verbose'] == "1":
	print('Baggrundsanalyse:')
	print('   Følsomhed: {:.3f} +/- {:.3f} cps/Bq'.format(sens, dsens))
	# print('   Kritisk niveau: {:.0f}Bq'.format(m.critical_level()/sens))
	print('   MDA:       {:.0f}Bq'.format(mda))
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
	ser_spec = radex.extract_sum(ser_files)

	m.set_spectrum(ser_spec)
	res = m.analyse_spectrum()
	act = res.net_signal
	conf_act = res.conf
	if res.detected:
		# Signal above critical level

		print('   Netto aktivitet: {:.0f} +/- {:.0f}Bq'.format(act, conf_act))

		if config['settings']['plot'] == "1":
			sp = radex.SpectrumPlotter(bkg_spec, ser_spec)
			sp.set_title(des)
			sp.plot()

		if (act + conf_act) > ra223.acc_act:

			if config['settings']['plot'] == "2":
				sp = radex.SpectrumPlotter(bkg_spec, ser_spec)
				sp.set_title(des)
				sp.plot()

			# Net activity above acceptable level, calculate disposal date
			decay_days = radex.decay(
				act + conf_act, ra223.acc_act, ra223.half_life)
			mdate = ser_spec.mdate  # Date of measurement
			if mdate is None:
				exit("Mangler dato på målinger!")
			decay_date = mdate + datetime.timedelta(days=decay_days)
			print('   Bortskaffelse d. {}'.format(decay_date.strftime('%d-%m-%Y')))
			print('')

			# Query user to write to log file
			yn = radex.list_yn("Hvis du synes at beregningen ser rigtig ud og den skal "
															"gemmes, skal den skrives til loggen.",
															"Gem til log?")
			if yn:
				radex.write_log(mdate, des, mda, sens, act + conf_act, decay_days, decay_date)

		else:
			print('   Aktiviteten er under det maksimalt accepterede niveau. '
								'Kan bortskaffes nu.')

	else:
		print('Ingen aktivitet registreret (øvre grænse: {:.0f}Bq)'.format(act + conf_act))

		if config['settings']['plot'] == "1":
			sp = radex.SpectrumPlotter(bkg_spec, ser_spec)
			sp.set_title(des)
			sp.plot()

		print('Kan bortskaffes nu.')

	print('')
	input("Tryk Enter for at fortsætte...")
	print('')
	print('')


archive = radex.list_yn(
	"Hvis du er færdig med at arbejde med disse data, kan du arkivere det.",
	"Arkiver data?")

if archive:
	arch_today_dir = config['dicom']['archive'] + datetime.date.today().isoformat()
	os.makedirs(arch_today_dir, exist_ok=True)
	shutil.move(config['dicom']['data'], arch_today_dir + '\\')
	# Recreate parent directory without contents
	os.makedirs(config['dicom']['data'], exist_ok=True)
