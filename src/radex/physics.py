import math


#   File containg physcis related stuff

class Radium223:

	def __init__(self):
		self.windows = [
			(76, 89),  # Emissions at 81.1keV (15.2%), 83.8keV (25.1%)
			(133, 165),  # Emissions at 144keV (3%) and 154keV (6%)
			(255, 283),  # Emission at 269.5keV (13.9%) and 271.2keV from Rn-219
			(322, 366),  # Emission at 324 and 338keV, and 351.1keV from Bi-211
			(383, 422)  # Emission at 401.8keV from Rn-219 and at 404.9 from Pb-211
		]

		self.half_life = 11.4  # days

		self.acc_act = 300  # Bq


def get_sens(fp: str) -> dict[tuple[int, int], tuple[float, float]]:
	sens_dict = {}
	with open(fp) as f:
		for line in f:
			s = line.split()
			sens_dict[(int(s[0]), int(s[1]))] = (float(s[2]), float(s[3]))
	return sens_dict


#   Calculate the amount of time until an initial activity has decayed to
#   a target activity given the half life.
#   The unit of the returned time is the same as the unit on the half life
def decay(activity_i: float, activity_f: float, half_life: float) -> float:
	return -half_life * math.log(activity_f / activity_i) / math.log(2.0)
