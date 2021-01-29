import numpy as np
import os
import matplotlib.pyplot as plt

#   Stores a spectrum with some useful information about the measurement
#   Fields:
#       + counts_by_kev:
#           2D numpy array storing:
#               the energy bins in keV in the first column
#               the counts in the second column
#       + count_time:
#           The count time in seconds

class Spectrum:

    def __init__(self, counts_by_kev, count_time):

        self.counts_by_kev  =   counts_by_kev
        self.count_time     =   count_time


    #   Save the spectrum to a file.
    def printToFile(self, file_name):

        np.savetxt(file_name,self.counts_by_kev,
            fmt='%d\t%.5f',
            delimiter='\t',
            comments='',
            header='{}\n'
                   'Energy [keV]\tCounts'.format(self.count_time))


    #   Plot the spectrum count data on the screen (halts execution)
    def plot(self, title=""):

        plt.plot(self.counts_by_kev[:,0],self.counts_by_kev[:,1])
        plt.xlabel("Energy [keV]")
        plt.ylabel("Counts")
        plt.title(title)
        plt.show()

#   Load a spectrum from a file saved by using the printToFile method
def loadFromFile(file_name):

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
        print("ERROR: Cannot add spectra with differing count times")
        exit()

    #   Check that the energy bins are the same in both spectra
    if not np.array_equal(spec1.counts_by_kev[:,0],spec2.counts_by_kev[:,0]):
        print("ERROR: Cannot add spectra with different energy bins")
        exit()

    res_spec = spec1.counts_by_kev
    res_spec[:,1] += spec2.counts_by_kev[:,1]
    count_time = spec1.count_time
    return Spectrum(res_spec, count_time)

#   Subtract the counts of two spectra from each other.
#   Meant to be used for subtracting background from a spectrum. The count time
#   of both files must therefore be the same, and will also be the same in the
#   resulting spectrum.
def subtract(spec1, spec2):

    #   Check that the count time is the same
    if not spec1.count_time == spec2.count_time:
        print("ERROR: Cannot subtract spectra with differing count times")
        exit()

    #   Check that the energy bins are the same in both spectra
    if not np.array_equal(spec1.counts_by_kev[:,0],spec2.counts_by_kev[:,0]):
        print("ERROR: Cannot subtract spectra with different energy bins")
        exit()

    res_spec = spec1.counts_by_kev
    res_spec[:,1] -= spec2.counts_by_kev[:,1]
    count_time = spec1.count_time
    return Spectrum(res_spec, count_time)
