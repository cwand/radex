# Analyse std sources and write spectra to files for easy access

import radex

# Initiate file handler
fh = radex.FileHandler()
fh.discover()

descr = fh.descriptions()
print(descr)

# Load background spectra from dicom files
bkg_files = fh.files('Bg 2')
bkg_spec = radex.extract_sum(bkg_files)

# Remove unwanted series
descr.remove('Bg 2')  # Dont do background
descr.remove('Bg')    # Ditto
descr.remove('Kilde 1+2')  # This is just a test series


for src in descr:

	# Load source spectra from dicom files
	src_files = fh.files(src)
	src_spec = radex.extract_sum(src_files)

	# Subtract background
	net_spec = radex.subtract_spectrum(src_spec, bkg_spec)

	# Save resulting spectrum to file
	net_spec.print_to_file('known_sources\\ra223\\' + src + '.txt')
