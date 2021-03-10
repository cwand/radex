import numpy as np
import math
import ra223sources
import spectrum
import physics

def sensitivity():

  # Measure sensitivity from known sources
  sens_obs = []
  src_bkg_spec = spectrum.load_from_file(ra223sources.source_spectra + 'Bg 2.txt')
  for src in ra223sources.sources:

  	# Standard spectrum and background, load from file
  	src_spec = spectrum.load_from_file(ra223sources.source_spectra + src + '.txt')

  	# Calculate sensitivity (cps/Bq) from known source
  	# Net source spectrum
  	net_src_spec = spectrum.subtract(src_spec, src_bkg_spec)

  	#	Get rate in windows
  	r_s = 0			# Net source rate
  	for window in physics.windows['Ra223']:
  		r_s += net_src_spec.window_rate(window)

  	# Get known activity
  	src_act = ra223sources.activities[src]

  	# Calculate sensitivity estimate from this source
  	sens_obs.append(r_s/src_act)		# Sensitivity [cps/Bq]

  # Calculate mean sensivity and uncertainty on sensitivity
  sens_obs = np.array(sens_obs)
  sens = np.mean(sens_obs)
  dsens = np.std(sens_obs, ddof=1)/math.sqrt(sens_obs.size)
  return (sens,dsens)
