import utils
import spectrum
import activity
import file_handler
import extract_dicom_spectrum
import argparse


print('')
print(' -------  RADEX -------')
print(''); print('')


#   Setup

#   Where we look for dicom files
pardir = 'C:\\Users\\bub8ga\\radex\\train\\'

#   Prepare file handler and discover all dicom files in the directory
fh = file_handler.FileHandler(pardir)
fh.discover()



#   Get all descriptions discovered
descr = fh.descriptions()




#   Query user for background spectrum to use from available descriptions
bkg_idx = utils.list_choose(
    'Hvilken serie skal benyttes som baggrund? (Skriv nummeret ud for den ønskede valgmulighed)',
    'Baggrundsserie: ',
    descr)
bkg_descr = descr[bkg_idx]
print('')
print('Du har valgt ' + bkg_descr + ' som baggrundsmåling!')
print('')

#   Remove chosen description from list og descriptions
descr.pop(bkg_idx)



#   Query user for known source spectrum to use from available descriptions
src_idx = utils.list_choose(
    'Hvilken serie skal benyttes som kilde? (Skriv nummeret ud for den ønskede valgmulighed)',
    'Kildeserie: ',
    descr)
src_descr = descr[src_idx]
print('')
print('Du har valgt ' + src_descr + ' som kilde!')
print('')

#   Query user for activity of known source
print('Hvad er aktiviteten (Bq) af kilden?')
src_act = int(input("Aktivitet i Bq: "))
print(src_act)
print('')
