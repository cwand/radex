#	Handles statisitcal analysis of counting data

import numpy as np
import math

# Returns the uncertainty (sqrt of the variance) on a counting rate
def sigma_rate(counting_rate, counting_time):
	return math.sqrt(counting_rate/counting_time)


def sigma_rate_bkg(net_counting_rate, background_counting_rate, counting_time):
	return math.sqrt((net_counting_rate + 2.0*background_counting_rate)/counting_time)
