import radex

import configparser


#   Load configuration

config = configparser.ConfigParser()
config.read('config.ini')

#   Prepare file handler and discover all dicom files in the main directory
fh = radex.FileHandler()
fh.discover()

#   Get all descriptions discovered
descr = fh.descriptions()
if not descr:
    # No dicom files found
    print(
        'Der blev ikke fundet nogle målinger. Tjek at der ligger filer med '
        'endelsen .dcm i mappen ' + config['dicom']['data'] + ''
        '. Filerne må gerne ligge i undermapper.'
    )
    input('Tryk Enter for at afslutte programmet...')
    exit()

#   Query user for background spectrum to use from available descriptions
ser_idx = radex.list_choose(
    'Hvilken serie skal printes? (Skriv nummeret ud for den ønskede valgmulighed)',
    'Serie: ',
    descr)
ser_descr = descr[ser_idx]
print('')
print('Du har valgt at printe ' + ser_descr)
print('')

# Fetch spectrum
ser_files = fh.files(ser_descr)  # List of files for background
ser_spec = radex.extract_sum(ser_files)


fp = input('Hvor vil du gemme det læste spektrum?\n')
ser_spec.print_to_file(fp)
