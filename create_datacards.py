import csv
from math import exp, pow
import numpy as np
import scipy.optimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_datacards(output,xs_sig):
	file_M1 = open("DataCards/data_out_mass1.txt","r")
	data_M1 = list(csv.reader(file_M1,delimiter=","))
	file_M1.close()
	file_M2 = open("DataCards/data_out_mass2.txt","r")
	data_M2 = list(csv.reader(file_M2,delimiter=","))
	file_M2.close()
	
	#print(data)
	xs_sig = {"Wto3l_M4":  7.474, "Wto3l_M5":  5.453, "Wto3l_M15": 1.0042, "Wto3l_M30": 0.17985, "Wto3l_M45": 0.02502214, "Wto3l_M60": 0.0021799,}
	split = 42
	M1fit = "exp"
	M2fit = "exp"
	
	#sig_yields = {}
	#sig_slots = {}
	x_list, y_list = [], []
	x_list1, x_list2, y_list1, y_list2 = [], [], [], []
	xs_list = []
	for i in range(len(data_M2)):
		if "Wto3l" in data_M2[i][0]:
			this_mass = int(data_M2[i][0].partition("M")[2])
			yields = []
	
			x_list.append(this_mass)

			if this_mass<=split:
				data = data_M2
				for j in range(1,len(data[i])):
					yields.append(float(data[i][j]))
				x_list1.append(this_mass)
				y_list1.append(max(yields))
			else:
				data = data_M1
				for j in range(1,len(data[i])):
					yields.append(float(data[i][j]))
				x_list2.append(this_mass)
				y_list2.append(max(yields))
	
			y_list.append(max(yields))
			xs_list.append(xs_sig["Wto3l_M%i"%(this_mass)])

			#for j in range(1,len(data[i])):
			#	yields.append(float(data[i][j]))
	
			#sig_yields[this_mass] = max(yields)
			#sig_slots[this_mass] = yields.index(sig_yields[this_mass])

	x_list.append(80)
	y_list.append(0)
	x_list2.append(80)
	y_list2.append(0)
	xs_list.append(0)

	# Testing
	x_list1.append(45)
	y_list1.append(y_list2[0])

	x = np.asarray(x_list)
	y = np.asarray(y_list)
	xs= np.asarray(xs_list)
	
	x1 = np.asarray(x_list1)
	x2 = np.asarray(x_list2)
	y1 = np.asarray(y_list1)
	y2 = np.asarray(y_list2)
	
	def monoExp(x, m, t):
		return m * np.exp(-t * x)
	
	def linear(x, m, t):
		return t + x*m

	def forXS(x, a, b, c, d, e):
		return np.exp(a*np.power(x,4)+b*np.power(x,3)+c*np.power(x,2)+d*x+e)
	
	# perform the fit
	p0 = (55, .05) # start with values near those we expect
	p1 = (0.0000004936, -0.000089271, 0.0053650056, -0.2349086721, 0.4302015825)
	
	if M2fit=="exp": params1, cv1 = scipy.optimize.curve_fit(monoExp, x1, y1, p0)
	elif M2fit=="line": params1, cv1 = scipy.optimize.curve_fit(linear , x1, y1, p0)
	m1, t1 = params1
	if M1fit=="exp": params2, cv2 = scipy.optimize.curve_fit(monoExp, x2, y2, p0)
	elif M1fit=="line": params2, cv2 = scipy.optimize.curve_fit(linear , x2, y2, p0)
	m2, t2 = params2

	params3, cv3 = scipy.optimize.curve_fit(forXS , x, xs, p1)
	a, b, c, d, e = params3

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
	if M2fit=="exp": y3 = monoExp(x3, m1, t1)
	elif M2fit=="line": y3 = linear(x3, m1, t1)
	x4 = np.arange(split,80)
	if M1fit=="exp": y4 = monoExp(x4, m2, t2)
	elif M1fit=="line": y4 = linear(x4, m2, t2)
	plt.plot(x, y, '.', label="signal yields")
	if M2fit=="exp": plt.plot(x3, y3, '--', color='orange',label="Y = %fe^(-%fx)"%(m1,t1))
	elif M2fit=="line": plt.plot(x3, y3, '--', color='orange',label="Y = %fx + %f"%(m1,t1))
	if M1fit=="exp": plt.plot(x4, y4, '--', color='blue',  label="Y = %fe^(-%fx)"%(m2,t2))
	elif M1fit=="line": plt.plot(x4, y4, '--', color='blue',  label="Y = %fx + %f"%(m2,t2))
	plt.title("Expected Signal Yields")
	plt.legend(loc='best')
	plt.xlabel("Z' Mass (GeV)")
	plt.ylabel("Event Yield")
	plt.yscale('log')
	plt.ylim(bottom=0)
	#plt.savefig("/orange/avery/nikmenendez/Output/datacards_RBE_mva_medIdPre/sig_yields.png")
	plt.savefig("%s/sig_yields.png"%(output))
	plt.clf()

	x5 = np.arange(80)
	y5 = forXS(x5, a, b, c, d, e)
	plt.plot(x, xs, '.', label="Sig XS")
	plt.plot(x5, y5, '--', label="Y = e^(%fx^4+%fx^3+%fx^2+%fx+%f)"%(a,b,c,d,e))
	plt.title("Signal Cross Section")
	plt.legend(loc='best')
	plt.xlabel("Z' Mass (GeV)")
	plt.ylabel("W->Z'munu->3munu Cross Section")
	plt.yscale('log')
	plt.ylim(bottom=0)
	plt.savefig("%s/sig_xs.png"%(output))
	plt.clf()
	
	# inspect the parameters
	#print(f"Y = {m} * e^(-{t} * x) + {b}")
	#print(f"Tau = {tauSec * 1e6} micro second")
	
	for j in range(1,len(data_M2[0])):
	
		mass = float(data_M2[0][j]) #(80-4)/76*(j-1) + 4 # (Max Mass - Low Mass)/nBins + Low Mass
		datacard = open("DataCards/datacard_M%.2f.txt"%(mass),"w")
	
		if mass<=split:
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
					sig_err = 1 + sig_xs/2
	
				#if mass in [0]:#[4,5,15,30,45,60]:
				#	n_sig = n_sig
				#else:
				#	n_sig = monoExp(mass, m, t)
	
				if mass <= split:
					if M2fit=="exp": n_sig = monoExp(mass, m1, t1)
					elif M2fit=="line": n_sig = linear(mass, m1, t1)
				else:
					if M1fit=="exp": n_sig = monoExp(mass, m2, t2)
					elif M1fit=="line": n_sig = linear(mass, m2, t2)
					
	
		datacard.write("# Simple counting experiment, with one signal and a few background processes \n")
		datacard.write("# One signal process, three background processes when using RBE \n")
		datacard.write("imax 1 number of channels\n")
		datacard.write("jmax 4 number of backgrounds\n")
		datacard.write("kmax 6 number of nuisance parameters\n")
		datacard.write("------------\n")
		datacard.write("shapes *              bin1 FAKE\n")
		datacard.write("------------\n")
		datacard.write("# we have just one channel, in which we observe %i events\n"%(n_data))
		datacard.write("bin bin1\n")
		datacard.write("observation %i\n"%(n_data))
		datacard.write("------------\n")
		datacard.write("# now we list the expected events for signal and all backgrounds in that bin\n")
		datacard.write("# the second 'process' line must have a positive number for backgrounds, and 0 for signal\n")
		datacard.write("# then we list the independent sources of uncertainties, and give their effect (syst. error)\n")
		datacard.write("# on each process and bin\n")
		datacard.write("bin             bin1  bin1  bin1  bin1  bin1\n")
		datacard.write("process         Zp    ZZ    WZ    DY    RBE\n")
		datacard.write("process          0     1     2     3     4\n")
		datacard.write("rate       %f %f %f %f %f\n"%(n_sig,n_ZZ,n_WZ,n_DY,n_fake))
		datacard.write("------------\n")
		datacard.write("lumi    lnN    1.023 1.023 1.023 1.023  -    lumi affects signal, ZZ, and WZ. lnN = lognormal\n")
		datacard.write("xs_Zp   lnN  %f  -     -     -    -     W->Zp->3mu cross section + signal efficiency + other minor ones.\n"%(sig_err))
		datacard.write("xs_ZZ   lnN      -  1.0015   -     -    -     ZZ->4mu cross section uncertainty\n")
		datacard.write("xs_WZ   lnN      -     -  1.0031   -    -     WZ->3mu cross section uncertainty\n")
		datacard.write("xs_DY   lnN      -     -     -  1.0023  -     DY->3mu cross section uncertainty\n")
		datacard.write("bg_RBE  lnN      -     -     -     -   1.30   30% uncertainty on the reducible background estimation\n")
	
		datacard.close()
	
