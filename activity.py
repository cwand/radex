import spectrum
import numpy as np
import math

#   Calculate minimum detectable activity given a background spectrum and a
#   sensitivty factor in some given window.
#   Parameters:
#       +   bkg_spec: the background spectrum
#       +   sensitivty_factor: sensitivity [cps/Bq]
#       +   window: energy window of interest in keV (e.g. [200,225]),
#                   defaults to entire spectrum
def mda_simple(bkg_spec, sensitivty_factor=1.0, window=[]):
    return 0
