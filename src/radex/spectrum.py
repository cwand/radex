from datetime import date
import numpy as np
import numpy.typing as npt


#   Stores a spectrum with some useful information about the measurement
#   Fields:
#       + rate_by_kev:
#           2D numpy array storing:
#               the energy bins in keV in the first column
#               the count rate (cps)
#       + count_time:
#           The count time in seconds
#       + mdate:
#           The date the spectrum was measured
class Spectrum:

	def __init__(self, rate_by_kev: npt.NDArray[np.float64], count_time: float,
			mdate: date | None = None):

		dim = rate_by_kev.shape
		if len(dim) != 2:
			raise ValueError("Input spectrum array must be two-dimensional")
		if dim[1] != 2:
			raise ValueError("Input spectrum array must have two columns")

		self.rate_by_kev = rate_by_kev.copy()
		self.count_time = count_time
		self.mdate = mdate

	#   Save the spectrum to a file.
	def print_to_file(self, file_name: str):

		np.savetxt(
			file_name, self.rate_by_kev,
			fmt='%d\t%.5f',
			delimiter='\t',
			comments='',
			header='{}\nEnergy [keV]\tRate [cps]'.format(self.count_time))

	#   Get the total count rate in a given window (defaults to entire spectrum)
	def window_rate(self, window: tuple[int, int]) -> float:
		total_rate = 0
		for kev, rate in self.rate_by_kev:
			if (kev >= window[0]) and (kev <= window[1]):
				total_rate += rate
		return total_rate

	#   Plot the spectrum count data on the screen (halts execution)
	# def plot(self, title=""):

	#    plt.plot(self.counts_by_kev[:,0],self.counts_by_kev[:,1])
	#    plt.xlabel("Energy [keV]")
	#    plt.ylabel("Rate [cps]")
	#    plt.title(title)
	#    plt.show()


#   Load a spectrum from a file saved by using the printToFile method
def load_spectrum_from_file(file_name):

	#   Read spectrum part of file
	spectrum = np.loadtxt(file_name, delimiter='\t', skiprows=2)

	#   Read count time from the first line of the file
	f = open(file_name)
	count_time = float(f.readline().rstrip())
	return Spectrum(spectrum, count_time)


#   Add the counts of two spectra together. Meant to be used for when multiple
#   detectors have measured separate spectra at the same time, which should be
#   merged (i.e. increasing the count rate). The count time and measurement date
#   of both files must therefore be the same, and will also be the same in the
#   resulting spectrum.
def add_spectrum(spec1, spec2):

	#   Check that the count time is the same
	if not spec1.count_time == spec2.count_time:
		raise ValueError("Spectra must have identical count time when adding")

	#   Check that the date is the same
	if not spec1.mdate == spec2.mdate:
		raise ValueError("Spectra must have identical date when adding")

	#   Check that the energy bins are the same in both spectra
	if not np.array_equal(spec1.rate_by_kev[:, 0], spec2.rate_by_kev[:, 0]):
		raise ValueError("Spectra must have identical energy bins when adding")

	res_spec = spec1.rate_by_kev.copy()
	res_spec[:, 1] += spec2.rate_by_kev[:, 1]
	count_time = spec1.count_time
	mdate = spec1.mdate
	return Spectrum(res_spec, count_time, mdate)


#   Subtract the counts of two spectra from each other.
#   Meant to be used for subtracting background from a spectrum. The count time
#   and date of both files must therefore be the same, and will also be the same
#   in the resulting spectrum.
def subtract_spectrum(spec1, spec2):

	#   Check that the count time is the same
	if not spec1.count_time == spec2.count_time:
		raise ValueError("Spectra must have identical count time when subtracting")

	#   Check that the date is the same
	if not spec1.mdate == spec2.mdate:
		raise ValueError("Spectra must have identical date when adding")

	#   Check that the energy bins are the same in both spectra
	if not np.array_equal(spec1.rate_by_kev[:, 0], spec2.rate_by_kev[:, 0]):
		raise ValueError("Spectra must have identical energy bins when subtracting")

	res_spec = spec1.rate_by_kev.copy()
	res_spec[:, 1] -= spec2.rate_by_kev[:, 1]
	count_time = spec1.count_time
	mdate = spec1.mdate
	return Spectrum(res_spec, count_time, mdate)
