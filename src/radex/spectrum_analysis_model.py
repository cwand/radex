from scipy.stats import norm
import math

import radex


# This file defines behaviour related to the statistical analysis of a spectrum


# Simple return value class, used for reporting the result of an analysis
class SpectrumAnalysisResult:

    def __init__(self, detected: bool, net_signal: float, conf: float):
        self.detected = detected  # Whether the signal was detected or not
        self.net_signal = net_signal  # The net signal (rate)
        self.conf = conf  # Confidence

    # Interpretation of conf-value:
    # If detected = True:
    # 	In this case the conf value is the width of the confidence interval.
    #       E.g: If net_signal = 10 and conf = 3, then the true value of the signal
    #       is with probability 1-gamma in the interval [7,13]
    # If detected = False:
    #       In this case the conf value is the distance from the net signal value
    #       to the upper limit bound on the true signal value.
    #       E.g.: If net_signal = 6 and conf = 2, then the registered signal had a
    #       value of 6, while the true signal is with probability 1-gamma below 8.


# Main analysis class used for performing the analysis
class SpectrumAnalysisModel:

    def __init__(self, background: radex.Spectrum, windows: list[tuple[int, int]] | None = None):
        self.alpha = 0.05
        self.beta = 0.05
        self.gamma = 0.05

        self.sens = 1.0
        self.dsens = 0.0

        self.background = background
        self.spectrum: radex.Spectrum | None = None

        ra223 = radex.Radium223()
        if windows is None:
            self.windows = ra223.windows.copy()
        else:
            self.windows = windows

    def set_spectrum(self, spectrum: radex.Spectrum):
        self.spectrum = spectrum

    # Get the total number of counts in the background spectrum
    def __bkg_window_counts(self) -> float:
        count_time = self.background.count_time
        total_rate = 0.0
        for window in self.windows:
            total_rate += self.background.window_rate(window)
        return total_rate * count_time  # Multiply with time to get counts

    # Same as above, but for the gross spectrum
    def __spc_window_counts(self) -> float:
        if self.spectrum is None:
            raise AttributeError("Spectrum has not been initialised!")
        count_time = self.spectrum.count_time
        total_rate = 0.0
        for window in self.windows:
            total_rate += self.spectrum.window_rate(window)
        return total_rate * count_time

    # Same as above, but for the net spectrum
    def __net_window_counts(self) -> float:
        if self.spectrum is None:
            raise AttributeError("Spectrum has not been initialised!")
        net_spectrum = radex.subtract_spectrum(self.spectrum, self.background)
        count_time = net_spectrum.count_time
        total_rate = 0.0
        for window in self.windows:
            total_rate += net_spectrum.window_rate(window)
        return total_rate * count_time

    # Calculate the critical level (rate)
    # Any net rate above this level counts a posteriori as a detected signal
    def critical_level(self) -> float:

        kalpha = float(norm.ppf(1.0 - self.alpha))
        count_time = self.background.count_time

        # Get total counts in background spectrum
        bkg_counts = self.__bkg_window_counts()

        # Critical level in counts
        lc = kalpha * math.sqrt(2.0 * bkg_counts)
        return lc / count_time

    # Calculate detection limit (rate)
    # Any net rate above this limit can a priori be expected to produce a
    # detecable signal.
    def detection_limit(self) -> float:

        kalpha = float(norm.ppf(1.0 - self.alpha))
        kbeta = float(norm.ppf(1.0 - self.beta))

        count_time = self.background.count_time

        # Critical level in counts
        lc = self.critical_level() * count_time

        # Detection limit in counts
        ld = lc + kbeta ** 2 / 2.0 * (1.0 + math.sqrt(
            1.0 + 4.0 * lc / kbeta ** 2 + 4.0 * lc ** 2 / (kbeta ** 2 * kalpha ** 2)))

        return ld / count_time

    def set_sensitivity(self, sens: float, dsens: float):
        self.sens = sens
        self.dsens = dsens

    # Perform the analysis of the spectrum
    def analyse_spectrum(self) -> SpectrumAnalysisResult:
        if self.spectrum is None:
            raise AttributeError("Spectrum has not been initialised!")
        count_time = self.spectrum.count_time

        # Get counts from background and gross spectrum
        bkg_counts = self.__bkg_window_counts()
        gross_counts = self.__spc_window_counts()

        # Calculate error on net signal (from counting statistics)
        sigma_s = math.sqrt(bkg_counts + gross_counts)

        # Net signal in counts
        s = self.__net_window_counts()
        # Net signal in rate
        s_rate = s / count_time

        # Factor in sensitivity (to yield an activity)
        a = s_rate / self.sens
        # Calculate error on activity
        sigma_a = math.sqrt(sigma_s ** 2 / count_time ** 2 + a ** 2 * self.dsens ** 2) / self.sens

        if s_rate > self.critical_level():
            # Signal detected, calculate confidence limit
            z = norm.ppf(1.0 - self.gamma / 2.0)
            cl = z * sigma_a
            det = True

        else:
            # Signal not detected, calculate upper limit
            z = norm.ppf(1.0 - self.gamma)
            cl = z * sigma_a
            det = False

        return SpectrumAnalysisResult(det, a, cl)
