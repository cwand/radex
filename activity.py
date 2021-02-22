import spectrum
import numpy as np
import math
import count_statistics as cs

#	Simple class used to present the results of an MDA analysis
class MDAResults:

	def __init__(self, sens, dsens, mda, dmda):
		self.sens		= sens
		self.dsens	= dsens
		self.mda		= mda
		self.dmda		= dmda

#	Perform an MDA analysis. Determines the sensitivity and MDA for detecting
#	Ra-223 in the given window based on the measured background as well as
#	the known source and the background of the known source.
#	Parameters:
#		+	bkg_spec: the measured background spectrum
#		+	src_spec:	the gross spectrum measured on the known source (incl background)
#		+	src_bkg_spec: the background spectrum of the known source (may be the same as bkg_spec if source was measured on the same occasion)
#		+	src_act: the activity of the known source
#		+	window: the energy window to analyse as a tuple (e.g. (200,250))
#	Returns:
#		An instance of the MDAResults class
def mda_analysis(bkg_spec, src_spec, src_bkg_spec, src_act, window):

	# Net source spectrum
	net_spec = spectrum.subtract(src_spec, src_bkg_spec)

	#	Get rates in window:
	r_s = net_spec.window_rate(window)			# Net source rate
	r_bs = src_bkg_spec.window_rate(window)	# Source background rate
	t_s = net_spec.count_time 							# Equal to t_bs for subtraction to work
	r_b = bkg_spec.window_rate(window)			#	Background rate
	t_b = bkg_spec.count_time

	dr_b = cs.sigma_rate(r_b, t_b)	# Uncertainty on background rate
	dr_s = cs.sigma_rate_bkg(r_s, r_bs, t_s) # Uncertainty on net source rate

	s = r_s/src_act		# Sensitivity [cps/Bq]
	ds = dr_s/src_act	# Uncertainty on sensitivity

	l = 3.0 * math.sqrt(r_b/t_b)	# Detection limit (Simple)
	dl = l*dr_b/(2.0*r_b)		# Uncertainty on minimum detectable count rate
	#l = 2.71 + 4.65 * math.sqrt(r_b/t_b)	# (Currie variation)
	#dl = 2.325 / (math.sqrt(r_b*t_b))

	M = m/s	# MDA
	dM = math.sqrt( dm**2/s**2 + (M*ds)**2/s**2 )

	return MDAResults(s,ds,M,dM)



#   Calculate minimum detectable activity given a background spectrum and a
#   sensitivty factor in some given window.
#   Parameters:
#       +   bkg_spec: the background spectrum
#       +   sensitivty: sensitivity [cps/Bq]
#       +   window: energy window of interest in keV (e.g. [200,225]),
#                   defaults to entire spectrum
def mda_simple(bkg_spec, sensitivty=1.0, window=[]):
    window_rate = bkg_spec.window_rate(window)
    count_time = bkg_spec.count_time

    min_det_count_rate = 3.0*math.sqrt(window_rate/count_time)
    mda = min_det_count_rate/sensitivty
    return mda


#	Simple class used to present the results of an Activity analysis
class ActivityResults:

	def __init__(self, act, dact):
		self.act	= act
		self.dact	= dact


def activity_analysis(bkg_spec, spec, sens, dsens, window):

	#	Subtract background from spectrum
	net_spec = spectrum.subtract(spec, bkg_spec)

	# Get rates in window
	r 	= net_spec.window_rate(window)	# Net counting rate
	rb 	= bkg_spec.window_rate(window)	# Background rate
	t		= net_spec.count_time	# Equal for background

	dr = cs.sigma_rate_bkg(r, rb, t)		# Uncertainty on counting rate

	A = r/sens	# Activity
	dA = math.sqrt(dr**2/sens**2 + (A*dsens)**2/sens**2)

	return ActivityResults(A,dA)



#   Calculate the amount of time until an initial activity has decayed to
#   a target activity given the half life.
#   The unit of the returned time is the same as the unit on the half life
def decay(activity_i, activity_f, half_life):
    return -half_life*math.log(activity_f/activity_i)/math.log(2.0)
