import spectrum
import numpy as np
import math

#   Calculate minimum detectable activity given a background spectrum and a
#   sensitivty factor in some given window.
#   Parameters:
#       +   bkg_spec: the background spectrum
#       +   sensitivty: sensitivity [cps/Bq]
#       +   window: energy window of interest in keV (e.g. [200,225]),
#                   defaults to entire spectrum
def mda_simple(bkg_spec, sensitivty=1.0, window=[]):
    window_rate = bkg_spec.window_rate(window)
    count_time = bkg_spec.count_time

    min_det_count_rate = 3.0*math.sqrt(window_rate/count_time)
    mda = min_det_count_rate/sensitivty
    return mda


#   Calculate the number of days until an initial activity has decayed to
#   a target activity given the half life
#   The unit of the returned perscribed time is the same as the unit on the
#   half life
def prescribe_activity(activity_i, activity_f, half_life):
    return -half_life_days*math.log(activity_f/activity_i)/math.log(2.0)
