import numpy as np
import math


#   Calculate the amount of time until an initial activity has decayed to
#   a target activity given the half life.
#   The unit of the returned time is the same as the unit on the half life
def decay(activity_i, activity_f, half_life):
    return -half_life*math.log(activity_f/activity_i)/math.log(2.0)
