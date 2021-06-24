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
		ks_index[cont[0]] = (int(cont[1]),int(cont[2]))

	sens_obs = []
	for src in ks_index:

		# Load spectrum from file
		src_spec = spectrum.load_from_file(config['calib']['calfiles']+src+'.txt')

		# Calculate sensitivity (cps/Bq) from known source

		#	Get rate in windows
		r_s = 0			# Net source rate
		for window in physics.windows['Ra223']:
			r_s += src_spec.window_rate(window)

		# Uncertainty on counting rate from poisson statistics
		dr_s = math.sqrt(r_s/src_spec.count_time)

		# Get known activity and uncertainty
		(src_act,dsrc_act) = ks_index[src]

		# Estimated sensitivity
		sens_i = r_s/src_act

		# Estimated uncertainy on sensitivity
		dsens_i = math.sqrt(dr_s**2 + sens_i**2 * dsrc_act**2)/src_act


		# Calculate sensitivity estimate from this source
		sens_obs.append((sens_i,dsens_i))		# Sensitivity [cps/Bq]

	# Calculate mean sensivity and uncertainty on sensitivity
	# Mean sensitivity = (sum_i K_i/dK_i^2)/(sum_i 1/dK_i^2)
	num = 0; den = 0
	for i in range(0,len(sens_obs)):
		num += sens_obs[i][0]/(sens_obs[i][1]**2)
		den += 1.0/(sens_obs[i][1]**2)
	sens = num/den

	# Uncertainty is sqrt(1/sum_i(1/dK_i^2)) = sqrt(1/den)
	dsens = math.sqrt(1.0/den)

	print(dsens)
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
