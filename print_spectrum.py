import utils
import spectrum
import spectrum_analysis_model as sam
import activity
from file_handler import FileHandler
from extract_dicom_spectrum import extract_sum
import physics
import known_sources as ks
import radiumlog
from spectrum_plotter import SpectrumPlotter

import configparser
import datetime
import shutil, os
import numpy as np
import math


#   Load configuration

config = configparser.ConfigParser()
config.read('config.ini')



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
ser_idx = utils.list_choose(
    'Hvilken serie skal printes? (Skriv nummeret ud for den ønskede valgmulighed)',
    'Serie: ',
    descr)
ser_descr = descr[ser_idx]
print('')
print('Du har valgt at printe ' + ser_descr)
print('')

# Fetch spectrum
ser_files = fh.files(ser_descr) # List of files for background
ser_spec = extract_sum(ser_files)


fp = input('Hvor vil du gemme det læste spektrum?\n')
ser_spec.print_to_file(fp)
