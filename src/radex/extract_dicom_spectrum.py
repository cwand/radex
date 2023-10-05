import numpy as np
import pydicom
import tempfile

import radex

# Extract spectrum from dicom file
# Spectrum is extracted from the selected dicom file and written in plain
# text to another file.

# =================================================================


# --- Helper function for reading spectrum from a dicom file ---
# The best thing to do here is to turn on code folding, fold away this function
# and pray that it keeps working, so you won't have to fix it

def _findspec(dataset: pydicom.FileDataset, indent: int, specstr: str) -> str:

    dont_print = ['Pixel Data', 'File Meta Information Version']

    for data_element in dataset:

        if data_element.VR == "SQ":   # a sequence
            for sequence_item in data_element.value:
                specstr = _findspec(sequence_item, indent + 1, specstr)
        else:
            if data_element.name in dont_print:
                print("""<item not printed -- in the "don't print" list>""")
                return ""

            else:
                repr_value = repr(data_element.value)

                if len(repr_value) > 50:
                    repr_value = repr_value[:80] + "..."

                if len(repr(data_element.value)) > 1000:

                    if indent == 3:
                        spectrum = data_element.value
                        regular_spectrum = spectrum.decode('utf-8')
                        specstr += regular_spectrum

    return specstr


# ==========================================================

#   Extract spectrum from a dicom file. Returns a spectrum type if all went well

def extract_spectrum(file_name):

    ds = pydicom.dcmread(file_name)

    # --- Read necessary tags from DICOM file
    frame_duration = ds[0x0018, 0x1242].value
    meas_date = ds[0x0008, 0x0012].value
    # Convert meas_date to a python date object
    mdate = radex.yyyymmdd2date(meas_date)

    #  ---  Read spectrum data ---
    #       (Hacked to within an inch of its life.
    #       If you can make it cleaner, be my guest)

    # Make virtual file with data from the correct tag
    file = tempfile.SpooledTemporaryFile()
    file.write(ds[0x0009, 0x10e6].value)

    # Read data from virtual DICOM file
    med_ds = pydicom.dcmread(file, force=True)  # type: ignore
    file.close()

    # Use helper file to get spectrum as a string
    specstr = _findspec(med_ds, 0, "")

    # Convert spectrum to numpy array
    # Ignore the last three characters of the string
    # as end of file characters
    cps = np.fromstring(specstr[:-3], sep=' ').reshape(-1, 2)

    spec = cps
    # spec[:,1] = cps[:,1]*frame_duration/1000 # Convert from cps to counts

    return radex.Spectrum(spec, frame_duration / 1000, mdate)


# -------------------------------

# Extract spectra for a list of files and return the sum of all the spectra
def extract_sum(filenames):

    # Extract first spectrum
    spec = extract_spectrum(filenames[0])

    # Add the rest
    for fn in filenames[1:]:
        spec = radex.add_spectrum(spec, extract_spectrum(fn))

    return spec
