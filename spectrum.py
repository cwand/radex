import numpy as np
import os
import matplotlib.pyplot as plt

#   Stores a spectrum with some useful information about the measurement
#   Fields:
#       + counts_by_kev:
#           2D numpy array storing:
#               the energy bins in keV in the first column
#               the count rate (cps)
#       + count_time:
#           The count time in seconds

class Spectrum:

    def __init__(self, rate_by_kev, count_time):

        self.rate_by_kev    =   rate_by_kev
        self.count_time     =   count_time


    #   Save the spectrum to a file.
    def print_to_file(self, file_name):

        np.savetxt(file_name,self.rate_by_kev,
            fmt='%d\t%.5f',
            delimiter='\t',
            comments='',
            header='{}\n'
                   'Energy [keV]\tRate [cps]'.format(self.count_time))

    #   Get the total count rate in a given window (defaults to entire spectrum)
    def window_rate(self, window = []):

        check_window = window
        if not check_window:
            check_window = [self.rate_by_kev[0,0],self.rate_by_kev[-1,0]]
        total_rate = 0
        for kev,rate in self.rate_by_kev:
            if ((kev >= check_window[0]) and (kev <= check_window[1])):
                total_rate += rate
        return total_rate




    #   Plot the spectrum count data on the screen (halts execution)
    def plot(self, title=""):

        plt.plot(self.counts_by_kev[:,0],self.counts_by_kev[:,1])
        plt.xlabel("Energy [keV]")
        plt.ylabel("Rate [cps]")
        plt.title(title)
        plt.show()

#   Load a spectrum from a file saved by using the printToFile method
def load_from_file(file_name):

    #   Read spectrum part of file
    spectrum = np.loadtxt(file_name,delimiter='\t',skiprows=2)

    #   Read count time from the first line of the file
    f = open(file_name)
    count_time = float(f.readline().rstrip())
    return Spectrum(spectrum, count_time)

#   Add the counts of two spectra together. Meant to be used for when multiple
#   detectors have measured separate spectra at the same time, which should be
#   merged (i.e. increasing the count rate). The count time of both files must
#   therefore be the same, and will also be the same in the resulting spectrum.
def add(spec1, spec2):

    #   Check that the count time is the same
    if not spec1.count_time == spec2.count_time:
        raise ValueError("Spectra must have identical count time when adding")

    #   Check that the energy bins are the same in both spectra
    if not np.array_equal(spec1.rate_by_kev[:,0],spec2.rate_by_kev[:,0]):
        raise ValueError("Spectra must have identical energy bins when adding")

    res_spec = spec1.rate_by_kev
    res_spec[:,1] += spec2.rate_by_kev[:,1]
    count_time = spec1.count_time
    return Spectrum(res_spec, count_time)

#   Subtract the counts of two spectra from each other.
#   Meant to be used for subtracting background from a spectrum. The count time
#   of both files must therefore be the same, and will also be the same in the
#   resulting spectrum.
def subtract(spec1, spec2):

    #   Check that the count time is the same
    if not spec1.count_time == spec2.count_time:
        raise ValueError("Spectra must have identical count time when subtracting")

    #   Check that the energy bins are the same in both spectra
    if not np.array_equal(spec1.rate_by_kev[:,0],spec2.rate_by_kev[:,0]):
        raise ValueError("Spectra must have identical energy bins when subtracting")

    res_spec = spec1.rate_by_kev
    res_spec[:,1] -= spec2.rate_by_kev[:,1]
    count_time = spec1.count_time
    return Spectrum(res_spec, count_time)
