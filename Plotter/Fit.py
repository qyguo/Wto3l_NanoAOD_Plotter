import numpy as np
from scipy.optimize import curve_fit
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def SigFit(data,sample,output):

	if not os.path.exists("/orange/avery/nikmenendez/Output/%s/sig_yields/"%(output)): os.makedirs("/orange/avery/nikmenendez/Output/%s/sig_yields/"%(output))

	def Gauss(x, A, mu, sigma):
		return A*np.exp(-(x-mu)**2/(2*sigma**2))

	A, mu, sigma = {}, {}, {}
	A_list, mu_list, sigma_list, mass_list = [], [], [], []
	for s in sample:
		if not ("Wto3l" in s):
			continue
		
		fit_window = 0.1
		split = 40

		mass = float(s.partition("_M")[2])
		fit_min = mass - mass*fit_window
		fit_max = mass + mass*fit_window
			
		if mass>=split: M = "M1"
		else:			M = "M2"

		sel = data[s]["selection"]
		fit_sel = (sel*(data[s][M]>fit_min)) & (sel*(data[s][M]<fit_max))
		to_fit = data[s][M][fit_sel]
		fit_weight = data[s]["eventWeight"][fit_sel]

		nbins = 100
		steps = (fit_max-fit_min)/nbins
		y,binEdges = np.histogram(to_fit,bins=nbins,range=(fit_min,fit_max),weights=fit_weight)
		x = np.arange(fit_min,fit_max,steps)

		p0 = [2500/mass, mass, mass*.01]
		params, covs = curve_fit(Gauss, x, y, p0)
		A[s], mu[s], sigma[s] = params

		fit = Gauss(x, A[s], mu[s], sigma[s])
		plt.plot(x, y, '.', label='Signal')
		plt.plot(x, fit, '--', label="A=%.2f, mu=%.2f, sigma=%.2f"%(A[s],mu[s],sigma[s]))
		plt.legend(loc='best')
		plt.xlabel("OS Di-Muon Mass (GeV)")
		plt.ylabel("Event Yield")
		plt.ylim(bottom=0)
		plt.savefig("/orange/avery/nikmenendez/Output/%s/sig_yields/sig_yields_M%i.png"%(output,mass))
		plt.clf()
		
		A_list.append(A[s])
		mu_list.append(mu[s])
		sigma_list.append(sigma[s])
		mass_list.append(mass)

	masses = np.asarray(mass_list)
	As = np.asarray(A_list)
	mus = np.asarray(mu_list)
	sigmas = np.asarray(sigma_list)

	def ExpDecay(x, m, t):
		return m * np.exp(-t * x)

	def linear(x, m, t):
		return m + x*t

	Aparams, Acv = curve_fit(ExpDecay, masses, As)
	Am, At = Aparams
	muparams, mucv = curve_fit(linear, masses, mus)
	mum, mut = muparams
	sigmaparams, sigmacv = curve_fit(linear, masses, sigmas)
	sigmam, sigmat = sigmaparams

	x = np.arange(80)

	Afit = ExpDecay(x, Am, At)
	plt.plot(masses, As, '.', label="Signal Amplitude")
	plt.plot(x, Afit, '--', label="A = %.2f*e^(-%.2fx)"%(Am, At))
	plt.legend(loc='best')
	plt.xlabel("Z' Mass (GeV)")
	plt.ylabel("Z' Peak Amplitude")
	plt.savefig("/orange/avery/nikmenendez/Output/%s/sig_yields/Fit_Amplitudes.png"%(output))
	plt.clf()

	mufit = linear(x, mum, mut)
	plt.plot(masses, mus, '.', label="Signal Mu")
	plt.plot(x, mufit, '--', label="Mu = %.2f + %.2fx"%(mum, mut))
	plt.legend(loc='best')
	plt.xlabel("Z' Mass (GeV)")
	plt.ylabel("Z' Peak Center")
	plt.savefig("/orange/avery/nikmenendez/Output/%s/sig_yields/Fit_Centers.png"%(output))
	plt.clf()
	
	sigmafit = linear(x, sigmam, sigmat)
	plt.plot(masses, sigmas, '.', label="Signal Sigma")
	plt.plot(x, sigmafit, '--', label="Sigma = %.2f + %.2fx"%(sigmam, sigmat))
	plt.legend(loc='best')
	plt.xlabel("Z' Mass (GeV)")
	plt.ylabel("Z' Peak Width")
	plt.savefig("/orange/avery/nikmenendez/Output/%s/sig_yields/Fit_Width.png"%(output))
	plt.clf()

	rel_sigma = []
	for i in range(len(masses)):
		rel_sigma.append((sigmas[i]*2)/masses[i])

	goal = [0.02]*len(x)
	relparams, relcv = curve_fit(linear, masses, rel_sigma)
	relm, relt = relparams
	relfit = linear(x, relm, relt)

	plt.plot(masses, rel_sigma, '.', label="Signal")
	plt.plot(x, relfit, '--', label="Rel Sigma = %f + %fx"%(relm, relt))
	plt.plot(x, goal, '--', label="2% width")
	plt.legend(loc='best')
	plt.xlabel("Z' Mass (GeV)")
	plt.ylabel("Relative Z' Peak Width")
	plt.savefig("/orange/avery/nikmenendez/Output/%s/sig_yields/Fit_Width_Relative.png"%(output))
	plt.clf()

