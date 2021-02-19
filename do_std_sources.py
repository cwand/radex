#	Analyse std sources and write spectra to files for easy access

import spectrum
import ra223sources
from file_handler import FileHandler
from extract_dicom_spectrum import extract_sum


#	Initiate file handler
fh = FileHandler(ra223sources.source_dir)
fh.discover()


#	Go through each source-background combination
for bkg in ra223sources.backgrounds:

	#	Load background spectra from dicom files
	bkg_files = fh.files(bkg)
	bkg_spec = extract_sum(bkg_files)

	#	Print background spectrum separately
	filename = ra223sources.source_spectra + bkg + '.txt'
	bkg_spec.print_to_file(filename)

	for src in ra223sources.sources:

		#	Load source spectra from dicom files
		src_files = fh.files(src)
		src_spec = extract_sum(src_files)

		#	Subtract background from source
		src_spec = spectrum.subtract(src_spec,bkg_spec)

		#	Save resulting spectrum to file
		filename = ra223sources.source_spectra + src + '_' + bkg + '.txt'
		src_spec.print_to_file(filename)
