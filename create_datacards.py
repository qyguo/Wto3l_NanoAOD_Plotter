import csv
from math import exp, pow
import numpy as np
import scipy.optimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_datacards(output,xs_sig,xs_err,AccEff):
	file_M1 = open("DataCards/data_out_mass1.txt","r")
	data_M1 = list(csv.reader(file_M1,delimiter=","))
	file_M1.close()
	file_M2 = open("DataCards/data_out_mass2.txt","r")
	data_M2 = list(csv.reader(file_M2,delimiter=","))
	file_M2.close()
	
	#print(data)
	#xs_sig = {"Wto3l_M4":  7.474, "Wto3l_M5":  5.453, "Wto3l_M15": 1.0042, "Wto3l_M30": 0.17985, "Wto3l_M45": 0.02502214, "Wto3l_M60": 0.0021799,}
	#for key in xs_sig:
	#	xs_sig[key] *= 3
	split = 40
	M1fit = "exp2"
	M2fit = "exp2"
	year = 2017
	
	#sig_yields = {}
	#sig_slots = {}
	x_list, y_list = [], []
	x_list1, x_list2, y_list1, y_list2 = [], [], [], []
	y_errs1, y_errs2 = [], []
	xs_list,xs_errs,xs_rele = [], [], []
	acc_list, eff_list = [], []
	for i in range(len(data_M2)):
		if "Wto3l" in data_M2[i][0]:
			this_mass = int(data_M2[i][0].partition("M")[2])
			yields = []
	
			x_list.append(this_mass)
			xs_list.append(xs_sig["Wto3l_M%i"%(this_mass)])
			xs_errs.append(xs_err["Wto3l_M%i"%(this_mass)])
			xs_rele.append(xs_err["Wto3l_M%i"%(this_mass)]/xs_sig["Wto3l_M%i"%(this_mass)])
			acc_list.append(AccEff["Wto3l_M%i"%(this_mass)][0])
			eff_list.append(AccEff["Wto3l_M%i"%(this_mass)][1])

			if this_mass<=split:
				data = data_M2
				for j in range(1,len(data[i])):
					yields.append(float(data[i][j]))
				x_list1.append(this_mass)
				y_list1.append(max(yields))
				y_errs1.append(np.sqrt(max(yields)))
			if this_mass>=split:
				data = data_M1
				for j in range(1,len(data[i])):
					yields.append(float(data[i][j]))
				x_list2.append(this_mass)
				y_list2.append(max(yields))
				y_errs2.append(np.sqrt(max(yields)))
	
			y_list.append(max(yields))

			#for j in range(1,len(data[i])):
			#	yields.append(float(data[i][j]))
	
			#sig_yields[this_mass] = max(yields)
			#sig_slots[this_mass] = yields.index(sig_yields[this_mass])

	#x_list.append(80)
	#y_list.append(0)
	#x_list2.append(80)
	#y_list2.append(0)
	#xs_list.append(0)

	## Testing
	#x_list1.append(45)
	#y_list1.append(y_list2[0])

	x = np.asarray(x_list)
	y = np.asarray(y_list)
	xs= np.asarray(xs_list)
	xe= np.asarray(xs_errs)
	xr= np.asarray(xs_rele)
	
	x1 = np.asarray(x_list1)
	x2 = np.asarray(x_list2)
	y1 = np.asarray(y_list1)
	y2 = np.asarray(y_list2)
	e1 = np.asarray(y_errs1)
	e2 = np.asarray(y_errs2)
	
	def monoExp(x, m, t, q):
		return m * np.exp(-t*x + q)
	
	def linear(x, m, t, q, p):
		return t + m*x + q*np.power(x,2) + p*np.power(x,3)

	def forYi(x, a, b, c, d):
		return np.exp(a+b*np.power(x,1)+c*np.power(x,2)+d*np.power(x,3))

	def forXS(x, a, b, c, d, e):#, f):
		return np.exp(a+b*np.power(x,1)+c*np.power(x,2)+d*np.power(x,3)+e*np.power(x,4)+0*np.power(x,5))
	
	def ZXS(x):
		return np.exp(0.000001*np.power(x,4)-0.000163*np.power(x,3)+0.008513*np.power(x,2)-0.291490*x+4.321499)
	
	# perform the fit
	p0 = [55, .05, .01, .01] # start with values near those we expect
	pM1 = [-10.426, 0.689723, -0.00934949, 0.0000230266] 
	pM2 = [7.83452, -0.0773427, 0.00136481, -0.0000461371]
	#p01 = [4.321499, -0.291490, 0.008513, -0.000163, 0.000001]#, 0]
	p01 = [4.321499, -0.291490, 0, 0, 0]
	#p02 = [4.321499, -0.291490, 0.008513, -0.000163, 0.000001]
	p02 = [0.4302015825, -0.2349086721, 0.0053650056, -0.000089271, 0.0000004936]
	#p01 = [0.4, -0.2, 0.005, -0.0001, 0.00001]
	
	if M2fit=="exp": params1, cv1 = scipy.optimize.curve_fit(monoExp, x1, y1, p0, sigma=e1)
	elif M2fit=="line": params1, cv1 = scipy.optimize.curve_fit(linear , x1, y1, p0, sigma=e1)
	elif M2fit=="exp2": params1, cv1 = scipy.optimize.curve_fit(forYi, x1, y1, pM2, sigma=e1)
	m1, t1, q1, p1= params1
	if M1fit=="exp": params2, cv2 = scipy.optimize.curve_fit(monoExp, x2, y2, p0, sigma=e2)
	elif M1fit=="line": params2, cv2 = scipy.optimize.curve_fit(linear , x2, y2, p0, sigma=e2)
	elif M2fit=="exp2": params2, cv1 = scipy.optimize.curve_fit(forYi, x2, y2, pM1, sigma=e2)
	m2, t2, q2, p2 = params2

	params3, cv3 = scipy.optimize.curve_fit(forXS, x, xs, p01, sigma=xe)
	a, b, c, d, e = params3
	params4, cv4 = scipy.optimize.curve_fit(forXS, x, xr, p01)
	ae, be, ce, de, ee = params4
	#params3, cv3 = scipy.optimize.curve_fit(monoExp , x, xs, p0)
	#a, b = params3

	#sampleRate = 20_000 # Hz
	#tauSec1 = (1 / t1) / sampleRate
	#
	## determine quality of the fit
	#squaredDiffs = np.square(y - monoExp(x, m, t))
	#squaredDiffsFromMean = np.square(y - np.mean(y))
	#rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
	#print(f"R2 = {rSquared}")
	
	# Plot the results
	x3 = np.arange(split)
	if M2fit=="exp": y3 = monoExp(x3, m1, t1, q1)
	elif M2fit=="line": y3 = linear(x3, m1, t1, q1, p1)
	elif M2fit=="exp2": y3 = forYi(x3, m1, t1, q1, p1)
	x4 = np.arange(split,80)
	if M1fit=="exp": y4 = monoExp(x4, m2, t2, q2)
	elif M1fit=="line": y4 = linear(x4, m2, t2, q2, p2)
	elif M1fit=="exp2": y4 = forYi(x4, m2, t2, q2, p2)
	plt.plot(x, y, '.', label="signal yields")
	if M2fit=="exp": plt.plot(x3, y3, '--', color='orange',label="Y = %fe^(-%fx)"%(m1,t1))
	elif M2fit=="line": plt.plot(x3, y3, '--', color='orange',label="Y = %fx + %f"%(m1,t1))
	elif M2fit=="exp2": plt.plot(x3, y3, '--', color='orange',label="Y = e^(%.4f+%.4fx+%.4fx^2+%.4fx^3)"%(m1,t1,q1,p1))
	if M1fit=="exp": plt.plot(x4, y4, '--', color='blue',  label="Y = %fe^(-%fx)"%(m2,t2))
	elif M1fit=="line": plt.plot(x4, y4, '--', color='blue',  label="Y = %fx + %f"%(m2,t2))
	elif M1fit=="exp2": plt.plot(x4, y4, '--', color='orange',label="Y = e^(%.4f+%.4fx+%.4fx^2+%.4fx^3)"%(m2,t2,q2,p2))
	plt.title("Expected Signal Yields")
	plt.legend(loc='best')
	plt.xlabel("Z' Mass (GeV)")
	plt.ylabel("Event Yield")
	plt.yscale('log')
	#plt.ylim(bottom=0)
	#plt.savefig("/orange/avery/nikmenendez/Output/datacards_RBE_mva_medIdPre/sig_yields.png")
	plt.savefig("%s/sig_yields.png"%(output))
	plt.clf()

	x5 = np.arange(80)
	y5 = forXS(x5, a, b, c, d, e)#, f)
	y6 = forXS(x5, p02[0], p02[1], p02[2], p02[3], p02[4])#, f)
	#y6 = ZXS(x5)
	#y5 = monoExp(x5, a, b)
	plt.plot(x, xs, '.', label="Sig XS")
	plt.plot(x5, y5, '--', label="W XS Fit")#"Y = e^(%.4f+%.4fx+%.4fx^2+%.4fx^3+%.5fx^4)"%(a,b,c,d,e))
	plt.plot(x5, y6, '--', label="Z XS Fit")
	#plt.plot(x5, y6, '--', label="Y = e^(%.4f+%.4fx+%.4fx^2+%.4fx^3+%.5fx^4)"%(p01[0], p01[1], p01[2], p01[3], p01[4]))
	#plt.plot
	#plt.plot(x5, y5, '--', label="Y = %fe^(%fx)"%(a,b))
	plt.title("Signal Cross Section x Branching Ratio")
	plt.legend(loc='best')
	plt.xlabel("Z' Mass (GeV)")
	plt.ylabel("XS(W->Z'munu) x BR(Z'->mumu)")
	plt.yscale('log')
	#plt.ylim(bottom=0)
	plt.savefig("%s/sig_xs.png"%(output))
	plt.clf()
	print("xs = r_value*math.exp(%f + %f*window_value + %f*math.pow(window_value,2) + %f*math.pow(window_value,3))"%(a,b,c,d))
	
	y7 = forXS(x5, ae, be, ce, de, ee)
	plt.plot(x, xr, '.', label="Sig XS Uncertainty")
	plt.plot(x5, y7, '--', label="Y = e^(%.4f+%.4fx+%.4fx^2+%.4fx^3+%.5fx^4)"%(ae,be,ce,de,ee))
	plt.title("Signal Cross Section x Branching Ratio Uncertainty")
	plt.legend(loc='best')
	plt.xlabel("Z' Mass (GeV)")
	plt.ylabel("Relative Uncertainty on XS(W->Z'munu) x BR(Z'->mumu)")
	plt.yscale('log')
	plt.savefig("%s/sig_xs_error.png"%(output))
	plt.clf()

	plt.plot(x, acc_list, '.-')
	plt.title("Eta/pT Fiducial Acceptance For Three Muons at GEN-level")
	plt.xlabel("Z' Mass (GeV)")
	plt.ylabel("Acceptance of 3 Muons")
	plt.ylim(bottom=0)
	plt.savefig("%s/sig_Acceptance.png"%(output))
	plt.clf()

	plt.plot(x, eff_list, '.-')
	plt.title("Full Reconstruction Efficiency for Events Within Acceptance")
	plt.xlabel("Z' Mass (GeV)")
	plt.ylabel("Selection Efficiency")
	plt.ylim(bottom=0)
	plt.savefig("%s/sig_Efficiency.png"%(output))
	plt.clf()

	# inspect the parameters
	#print(f"Y = {m} * e^(-{t} * x) + {b}")
	#print(f"Tau = {tauSec * 1e6} micro second")
	

	for j in range(1,len(data_M2[0])):
	
		mass = float(data_M2[0][j]) #(80-4)/76*(j-1) + 4 # (Max Mass - Low Mass)/nBins + Low Mass
		datacard = open("DataCards/datacard_M%.2f.txt"%(mass),"w")
	
		if mass<split:
			data = data_M2
		else:
			data = data_M1
	
		prev_diff = 999
		for i in range(len(data)):
			#prev_diff = 999
	
			if "data" in data[i][0]:
				n_data = float(data[i][j])
			elif "WZ" in data[i][0]:
				n_WZ = float(data[i][j])
			elif "ZZ" in data[i][0]:
				n_ZZ = float(data[i][j])
			elif "DY" in data[i][0]:
				n_DY = float(data[i][j])
			elif "fake" in data[i][0]:
				n_fake = float(data[i][j])
	
			if "Wto3l" in data[i][0]:
				this_mass = int(data[i][0].partition("M")[2])
				mass_diff = abs(this_mass - mass)
				if mass_diff < prev_diff:
					sig_mass = this_mass
					n_sig = float(data[i][j])
					prev_diff = mass_diff
					sig_xs = xs_sig["Wto3l_M%i"%(sig_mass)]
					sig_err = 1 + .01
	
				#if mass in [0]:#[4,5,15,30,45,60]:
				#	n_sig = n_sig
				#else:
				#	n_sig = monoExp(mass, m, t)
	
				if mass < split:
					if M2fit=="exp": n_sig = monoExp(mass, m1, t1, q1)
					elif M2fit=="line": n_sig = linear(mass, m1, t1, q1, p1)
					elif M2fit=="exp2": n_sig = forYi(mass, m1, t1, q1, p1)
				else:
					if M1fit=="exp": n_sig = monoExp(mass, m2, t2, q2)
					elif M1fit=="line": n_sig = linear(mass, m2, t2, q2, p2)
					elif M1fit=="exp2": n_sig = forYi(mass, m2, t2, q2, p2)
					
		bin1 = "ZpToMuMu_M%.2f_%i"%(mass,year)

		datacard.write("# Simple counting experiment, with one signal and a few background processes \n")
		datacard.write("# One signal process, three background processes when using RBE \n")
		datacard.write("imax 1 number of channels\n")
		datacard.write("jmax 4 number of backgrounds\n")
		datacard.write("kmax 6 number of nuisance parameters\n")
		datacard.write("------------\n")
		datacard.write("shapes *              %s FAKE\n"%(bin1))
		datacard.write("------------\n")
		datacard.write("# we have just one channel, in which we observe %i events\n"%(n_data))
		datacard.write("bin         %s\n"%(bin1))
		datacard.write("observation %i\n"%(n_data))
		datacard.write("------------\n")
		datacard.write("# now we list the expected events for signal and all backgrounds in that bin\n")
		datacard.write("# the second 'process' line must have a positive number for backgrounds, and 0 for signal\n")
		datacard.write("# then we list the independent sources of uncertainties, and give their effect (syst. error)\n")
		datacard.write("# on each process and bin\n")
		datacard.write("bin             %s	%s	%s	%s	%s\n"%(bin1,bin1,bin1,bin1,bin1))
		datacard.write("process         ZpToMuMu_M%.2f			ZZ						WZ						DY						RBE\n"%(mass))
		datacard.write("process         0						1     					2     					3     					4\n")
		datacard.write("rate       		%f 			%f 				%f 				%f 				%f\n"%(n_sig,n_ZZ,n_WZ,n_DY,n_fake))
		datacard.write("------------\n")
		datacard.write("lumi    lnN    1.023 1.023 1.023 1.023  -    lumi affects signal, ZZ, and WZ. lnN = lognormal\n")
		datacard.write("xs_Zp   lnN    %.3f   -     -     -    -     W->Zp->3mu cross section + signal efficiency + other minor ones.\n"%(sig_err))
		datacard.write("xs_ZZ   lnN      -  1.0015   -     -    -     ZZ->4mu cross section uncertainty\n")
		datacard.write("xs_WZ   lnN      -     -  1.0031   -    -     WZ->3mu cross section uncertainty\n")
		datacard.write("xs_DY   lnN      -     -     -  1.0023  -     DY->3mu cross section uncertainty\n")
		datacard.write("bg_RBE  lnN      -     -     -     -   1.30   30% uncertainty on the reducible background estimation\n")
	
		datacard.close()
	
