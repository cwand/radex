from scipy.stats import norm
import math

class SpectrumAnalysisResult:

	def __init__(self, detected, net_signal, upper_limit, conf):
		self.detected 		=	detected
		self.net_signal 	=	net_signal
		self.conf					= conf


class SpectrumAnalysisModel:

	alpha = 0.05		# Acceptable risk of type I errors (false positive)
	beta = 0.05			# Acceptable risk of type II errors (false negative)
	gamma = 0.05		# Confidence interval size (1-gamma)

	background = None
	spectrum = None
	windows = None

	def set_windows(self, windows):
		self.windows = windows


	def set_background(self, bkg):
		self.background = bkg




	def critical_level(self):

		kalpha = norm.ppf(1.0 - self.alpha)
		count_time = self.background.count_time

		# Get total count rate and counts in background spectrum
		total_rate = 0
		if self.windows is None:
			total_rate = self.background.window_rate()
		else:
			for window in self.windows:
				total_rate += self.background.window_rate(window)
		total_counts = total_rate * count_time


		# Critical level in counts
		lc = kalpha * math.sqrt(2.0 * total_counts)
		return lc / count_time


	def detection_limit(self):

		kalpha = norm.ppf(1.0 - self.alpha)
		kbeta = norm.ppf(1.0 - self.beta)

		count_time = self.background.count_time

		# Critical level in counts
		lc = self.critical_level()*count_time

		# Detection limit in counts
		ld = lc + kbeta**2/2.0 * ( 1.0 + math.sqrt( 1.0 + 4.0*lc/kbeta**2 + 4.0*lc**2 / (kbeta**2 * kalpha**2 ) ) )

		return ld/count_time



	def set_spectrum(self, spec):
		self.spectrum = spec



	def analyse_spectrum(self):
		return SpectrumAnalysisResult(False, 0, 0, 0)
