import matplotlib.pyplot as plt
import numpy as np

import radex


class SpectrumPlotter:

	def __init__(self, background: radex.Spectrum | None, spectrum: radex.Spectrum):
		self.bkg = background
		self.spec = spectrum
		self.name = "Spectrum"

	def set_title(self, title: str):
		self.name = title

	def plot(self):

		if self.bkg is None:
			net_spec = self.spec
		else:
			net_spec = radex.subtract_spectrum(self.spec, self.bkg)

		plt.plot(net_spec.rate_by_kev[:, 0], net_spec.rate_by_kev[:, 1], label='Net spectrum')

		ra223 = radex.Radium223()
		for window in ra223.windows:
			xlist = np.arange(window[0], window[1] + 1, 1.0)
			ylist = net_spec.rate_by_kev[window[0]:window[1] + 1, 1]
			plt.fill_between(xlist, ylist)

		if self.bkg is not None:
			plt.plot(self.bkg.rate_by_kev[:, 0], self.bkg.rate_by_kev[:, 1],
					linestyle='--', color='0.4', label='background')

		plt.legend()
		plt.xlabel("Energy [keV]")
		plt.ylabel("Rate [cps]")
		plt.title(self.name)
		print("   Viser plot. Luk vinduet når du er færdig, for at fortsætte.")
		plt.show()
