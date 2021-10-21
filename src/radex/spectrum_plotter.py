import matplotlib.pyplot as plt
import numpy as np

from . import spectrum


class SpectrumPlotter:

	bkg = None
	spec = None
	name = "Spectrum"

	def set_background(self, background):
		self.bkg = background

	def set_spectrum(self, spectrum):
		self.spec = spectrum

	def set_title(self,title):
		self.name = title

	def plot(self):

		if self.bkg is None:
			net_spec = self.spec
		else:
			net_spec = spectrum.subtract_spectrum(self.spec, self.bkg)

		plt.plot(net_spec.rate_by_kev[:,0],net_spec.rate_by_kev[:,1],
				label='Net spectrum')


		if physics.windows['Ra223'] is None:
			xlist = net_spec.rate_by_kev[:,0]
			ylist = net_spec.rate_by_kev[:,1]
			plt.fill_between(xlist,ylist)
		else:
			for window in physics.windows['Ra223']:
				xlist = np.arange(window[0],window[1]+1,1.0)
				ylist = net_spec.rate_by_kev[window[0]:window[1]+1,1]
				plt.fill_between(xlist,ylist)

		if self.bkg is not None:
			plt.plot(self.bkg.rate_by_kev[:,0],self.bkg.rate_by_kev[:,1],
				linestyle='--',color='0.4',label='background')

		plt.legend()
		plt.xlabel("Energy [keV]")
		plt.ylabel("Rate [cps]")
		plt.title(self.name)
		print("   Viser plot. Luk vinduet når du er færdig, for at fortsætte.")
		plt.show()
