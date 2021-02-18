#	Analyse std sources and write spectra to files for easy access

import spectrum
import ra223sources
import file_handler
import extract_dicom_spectrum


#	Initiate file handler
fh = file_handler.FileHandler(ra223sources.source_dir)
fh.discover()


#	Go through each source-background combination
for src in ra223sources.sources:

	for bkg in ra223sources.backgrounds:

		#	Load source spectra from dicom files
		src_files = fh.files(src)
		# Extract first spectrum...
		src_spec = extract_dicom_spectrum.extract_spectrum(src_files[0])
		# ... and add the rest
		for fn in src_files[1:]:
		    src_spec = spectrum.add(
				src_spec,extract_dicom_spectrum.extract_spectrum(fn))

		#	Load background spectra from dicom files
		bkg_files = fh.files(bkg)
		bkg_spec = extract_dicom_spectrum.extract_spectrum(bkg_files[0])
		for fn in bkg_files[1:]:
		    bkg_spec = spectrum.add(
				bkg_spec,extract_dicom_spectrum.extract_spectrum(fn))


		#	Subtract background from source
		src_spec = spectrum.subtract(src_spec,bkg_spec)

		#	Save resulting spectrum to file
		filename = ra223sources.source_spectra + src + '_' + bkg + '.txt'
		src_spec.print_to_file(filename)
