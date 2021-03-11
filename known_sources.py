import numpy as np
import math
import spectrum
import physics

# Get spectrum data from sources with known activity and measure sensitivity
def sensitivity():

  # Create known source index from index file
  ks_index = {}
  with open('known_sources\\ra223\\src.txt') as f:
    lines = [line.rstrip() for line in f]
  for s in lines:
    cont = s.split(';')
    ks_index[cont[0]] = int(cont[1])

  sens_obs = []
  for src in ks_index:

  	# Load spectrum from file
  	src_spec = spectrum.load_from_file('known_sources\\ra223\\'+src+'.txt')

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
  dsens = np.std(sens_obs, ddof=1)/math.sqrt(sens_obs.size)
  return (sens,dsens)
