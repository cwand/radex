from scipy.stats import norm
import spectrum
import math

# This file defines behaviour related to the statistical analysis of a spectrum


# Simple return value class, used for reporting the result of an analysis
class SpectrumAnalysisResult:

	def __init__(self, detected, net_signal, conf):
		self.detected 		=	detected		# Whether the signal was detected or not
		self.net_signal 	=	net_signal	# The net signal (rate)
		self.conf					= conf				# Confidence

		# Interpretation of conf-value:
		# If detected = True:
		# 	In this case the conf value is the width of the confidence interval.
		#		E.g: If net_signal = 10 and conf = 3, then the true value of the signal
		#		is with probability 1-gamma in the interval [7,13]
		# If detected = False:
		#		In this case the conf value is the distance from the net signal value
		#		to the upper limit bound on the true signal value.
		#		E.g.: If net_signal = 6 and conf = 2, then the registered signal had a
		#		value of 6, while the true signal is with probability 1-gamma below 8.


# Main analysis class used for performing the analysis
class SpectrumAnalysisModel:

	# Confidence parameters
	alpha = 0.05		# Acceptable risk of type I errors (false positive)
	beta = 0.05			# Acceptable risk of type II errors (false negative)
	gamma = 0.05		# Confidence interval size (1-gamma) of true signal

	background = None	# Background spectrum to apply
	spectrum = None		#	Gross spectrum to analyse
	windows = None		# The relevant windows from where counts should be extracted

	sens = 1.0			# Sensitivity [cps/Bq]
	dsens = 0.0			# Statistical uncertainty on the sensitivity


	# Set the relevant windows (a list of tuples, e.g. [(200,260),(300,320)])
	def set_windows(self, windows):
		self.windows = windows

	# Get the total number of counts in the background spectrum
	def __bkg_window_counts(self):
		count_time = self.background.count_time
		total_rate = 0
		if self.windows is None:
			# No windows set, use entire spectrum
			total_rate = self.background.window_rate()
		else:
			for window in self.windows:
				total_rate += self.background.window_rate(window)
		return total_rate * count_time		# Multiply with time to get counts

	# Same as above, but for the gross spectrum
	def __spc_window_counts(self):
		count_time = self.spectrum.count_time
		total_rate = 0
		if self.windows is None:
			total_rate = self.spectrum.window_rate()
		else:
			for window in self.windows:
				total_rate += self.spectrum.window_rate(window)
		return total_rate * count_time

	# Same as above, but for the net spectrum
	def __net_window_counts(self):
		net_spectrum = spectrum.subtract(self.spectrum,self.background)
		count_time = net_spectrum.count_time
		total_rate = 0
		if self.windows is None:
			total_rate = net_spectrum.window_rate()
		else:
			for window in self.windows:
				total_rate += net_spectrum.window_rate(window)
		return total_rate * count_time


	# Set the background to apply
	def set_background(self, bkg):
		self.background = bkg


	# Calculate the critical level (rate)
	# Any net rate above this level counts a posteriori as a detected signal
	def critical_level(self):

		kalpha = norm.ppf(1.0 - self.alpha)
		count_time = self.background.count_time

		# Get total counts in background spectrum
		bkg_counts = self.__bkg_window_counts()

		# Critical level in counts
		lc = kalpha * math.sqrt(2.0 * bkg_counts)
		return lc / count_time


	# Calculate detection limit (rate)
	# Any net rate above this limit can a priori be expected to produce a
	# detecable signal.
	def detection_limit(self):

		kalpha = norm.ppf(1.0 - self.alpha)
		kbeta = norm.ppf(1.0 - self.beta)

		count_time = self.background.count_time

		# Critical level in counts
		lc = self.critical_level()*count_time

		# Detection limit in counts
		ld = lc + kbeta**2/2.0 * ( 1.0 + math.sqrt( 1.0 + 4.0*lc/kbeta**2 + 4.0*lc**2 / (kbeta**2 * kalpha**2 ) ) )

		return ld/count_time


	# Set the gross spectrum to analyse
	def set_spectrum(self, spec):
		self.spectrum = spec

	def set_sensitivity(self, sens, dsens):
		self.sens = sens
		self.dsens = dsens


	# Perform the analysis of the spectrum
	def analyse_spectrum(self):

		count_time = self.spectrum.count_time

		# Get counts from background and gross spectrum
		bkg_counts		= self.__bkg_window_counts()
		gross_counts	= self.__spc_window_counts()

		# Calculate error on net signal
		sigma = math.sqrt(bkg_counts + gross_counts)

		# Net signal in counts
		S = self.__net_window_counts()
		# Net signal in rate
		S_rate = S/count_time

		if S_rate > self.critical_level():
			# Signal detected, calculate confidence limit
			z = norm.ppf(1.0 - self.gamma/2.0)
			cl_rate = z*sigma/count_time
			det = True

		else:
			# Signal not detected, calculate upper limit
			z = norm.ppf(1.0 - self.gamma)
			cl_rate = z*sigma/count_time
			det = False

		return SpectrumAnalysisResult(det, S_rate, cl_rate)
