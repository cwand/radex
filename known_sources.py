import numpy as np
import math
import spectrum
import physics
import configparser
from pathlib import Path

# Get spectrum data from sources with known activity and measure sensitivity
def sensitivity():

	# Read configuration to find calibration data
	config = configparser.ConfigParser()
	config.read('config.ini')

	# Create known source index from index file
	ks_index = {}
	with open(config['calib']['calfiles']+'src.txt') as f:
		lines = [line.rstrip() for line in f]
	for s in lines:
		cont = s.split(';')
		ks_index[cont[0]] = int(cont[1])

	sens_obs = []
	for src in ks_index:

		# Load spectrum from file
		src_spec = spectrum.load_from_file(config['calib']['calfiles']+src+'.txt')

		# Calculate sensitivity (cps/Bq) from known source

		#	Get rate in windows
		r_s = 0			# Net source rate
		for window in physics.windows['Ra223']:
			r_s += src_spec.window_rate(window)

		# Get known activity
		src_act = ks_index[src]

		# Calculate sensitivity estimate from this source
		sens_obs.append(r_s/src_act)		# Sensitivity [cps/Bq]

	# Calculate mean sensivity and uncertainty on sensitivity
	sens_obs = np.array(sens_obs)
	sens = np.mean(sens_obs)
	if sens_obs.size == 1:
		print('Usikkerhed på følsomhed bliver ignoreret, '
					'da der kun er registreret 1 kalibrering!')
		dsens = 0
	else:
		dsens = np.std(sens_obs, ddof=1)/math.sqrt(sens_obs.size)
	return (sens,dsens)


def write_calibration(spectrum, activity, uncertainty_act, name):

	# Read configuration
	config = configparser.ConfigParser()
	config.read('config.ini')

	# Get all calibration files saved so far
	ks_index = {}
	my_file = Path(config['calib']['calfiles']+'src.txt')
	if my_file.is_file():
		with open(config['calib']['calfiles']+'src.txt') as f:
			lines = [line.rstrip() for line in f]
		for s in lines:
			cont = s.split(';')
			ks_index[cont[0]] = int(cont[1])


	# Check if name already exists, in that case report error
	if name in ks_index:
		print('Navn på kalibrering eksisterer allerede. '
					'Vælg et andet navn eller slet den gamle kalibrering.')
		exit()

	# Save spectrum to file
	res_name = config['calib']['calfiles']+ name + '.txt'
	spectrum.print_to_file(res_name)

	# Save activity to index file
	with open(config['calib']['calfiles']+'src.txt', 'a') as f:
		f.write('{};{};{}\n'.format(name,activity,uncertainty_act))

	return res_name
