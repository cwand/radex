import utils
import spectrum
from file_handler import FileHandler
from extract_dicom_spectrum import extract_sum
import known_sources as ks
from spectrum_plotter import SpectrumPlotter

import configparser
import datetime
import shutil, os
import numpy as np
import math

# Script used to load measurements of a calibration source and save the spectrum
# and data, so it can be used as a known source for calibration.

#   Load configuration

config = configparser.ConfigParser()
config.read('config.ini')


print('')
print(' -------  RADEX CALIBRATION -------')
print(''); print('')

#   Prepare file handler and discover all dicom files in the main directory
fh = FileHandler()
fh.discover()


#   Get all descriptions discovered
descr = fh.descriptions()
if not descr:
  #   No dicom files found
  print('Der blev ikke fundet nogle målinger. Tjek at der ligger filer med '
        'endelsen .dcm i mappen ' + config['dicom']['data'] + '. '
				'Filerne må gerne ligge i undermapper.')
  input('Tryk Enter for at afslutte programmet...')
  exit()

#   Query user for background spectrum to use from available descriptions
bkg_idx = utils.list_choose(
    'Hvilken serie skal benyttes som baggrund? (Skriv nummeret ud for den ønskede valgmulighed)',
    'Baggrundsserie: ',
    descr)
bkg_descr = descr[bkg_idx]
print('')
print('Du har valgt ' + bkg_descr + ' som baggrundsmåling!')
print(''); print('')

#	Remove background from list of descriptions
descr.remove(bkg_descr)

# Fetch spectra for background
bkg_files = fh.files(bkg_descr) # List of files for background
bkg_spec = extract_sum(bkg_files)


#   Query user for calibration spectrum to use from available descriptions
cal_idx = utils.list_choose(
    'Hvilken serie skal benyttes som kalibrering? (Skriv nummeret ud for den ønskede valgmulighed)',
    'Kalibrering: ',
    descr)
cal_descr = descr[cal_idx]
print('')
print('Du har valgt ' + cal_descr + ' som kalibrering!')
print(''); print('')

# Fetch spectra for calibration
cal_files = fh.files(cal_descr) # List of files for calibration
cal_spec = extract_sum(cal_files)


# Calculate net spectrum
net_spec = spectrum.subtract(cal_spec,bkg_spec)


# Query user for activity and calibration name
cal_act = input("Hvad er kalibreringskildens aktivitet på optagetidspunktet (Bq)? ")
cal_sa = input("Hvad er usikkerheden på kalibreringskildens aktivitet på optagetidspunktet (Bq)? ")
cal_name = input("Giv kalibreringskilden et navn: ")

sp = SpectrumPlotter()
sp.set_spectrum(net_spec)
sp.set_title(cal_name)
sp.plot()

cal_fname = ks.write_calibration(net_spec, cal_act, cal_sa, cal_name)
print('Netto spektrum er gemt i stien: ' + cal_fname)

print('Kalibrering er gemt!')
input('Tryk Enter for at afslutte...')
