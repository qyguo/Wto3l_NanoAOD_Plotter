import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def fake_calc(data,s,nbins,out):

	#nbins=[5,10,15,20,30,60]
	if len(nbins)<2:
		y_pass, y_fail = np.zeros(nbins), np.zeros(nbins)
		err_pass, err_fail = np.zeros(nbins), np.zeros(nbins)
	else:
		y_pass, y_fail = np.zeros(len(nbins)-1), np.zeros(len(nbins)-1)
		err_pass, err_fail = np.zeros(len(nbins)-1), np.zeros(len(nbins)-1)
	s_for_fake = ["ZZTo4L","WZTo3LNu","DYJetsToLL_M0To1","data"]
	for i in range(len(s)):
		if s[i] not in s_for_fake: continue
		sam = data[s[i]]

		passes = sam["selection_pass"]*(np.abs(sam["etaL3"])<1.2)
		failes = sam["selection_fail"]*(np.abs(sam["etaL3"])<1.2)

		pass_pt = sam["pTL3"][passes]
		fail_pt = sam["pTL3"][failes]

		#Calculate Weights
		#weight_arr_pass = sam["weight"]*sam["genWeight"][passes]*sam["pileupWeight"][passes]
		#weight_arr_fail = sam["weight"]*sam["genWeight"][failes]*sam["pileupWeight"][failes]
		weight_arr_pass = sam["weight"][passes]*sam["genWeight"][passes]*sam["pileupWeight"][passes]
		weight_arr_fail = sam["weight"][failes]*sam["genWeight"][failes]*sam["pileupWeight"][failes]

		#Calculate Errors
		#t_pass,binEdges = np.histogram(pass_pt,bins=nbins,range=(nbins[0],nbins[-1]))
		#t_fail,binEdges = np.histogram(fail_pt,bins=nbins,range=(nbins[0],nbins[-1]))
		#er_pass = np.sqrt(np.abs(t_pass))*sam["weight"]
		#er_fail = np.sqrt(np.abs(t_fail))*sam["weight"]
		#er_totl = np.sqrt(np.abs(t_pass)+np.abs(t_fail))*sam["weight"]

		t_pass,binEdges_pass = np.histogram(pass_pt,bins=nbins,range=(nbins[0],nbins[-1]),weights=weight_arr_pass)
		t_fail,binEdges_fail = np.histogram(fail_pt,bins=nbins,range=(nbins[0],nbins[-1]),weights=weight_arr_fail)
		er_pass = np.sqrt(np.histogram(pass_pt,bins=nbins,range=(nbins[0],nbins[-1]),weights=weight_arr_pass**2)[0])
		er_fail = np.sqrt(np.histogram(fail_pt,bins=nbins,range=(nbins[0],nbins[-1]),weights=weight_arr_fail**2)[0])
		
		if s[i]=="data":
			y_pass += t_pass
			y_fail += t_fail
		else:
			y_pass -= t_pass
			y_fail -= t_fail
		err_pass += er_pass
		err_fail += er_fail
		#err_totl += er_totl

	ratio1_b = y_pass/(y_pass+y_fail)
	err1_b = ratio1_b*(err_pass/y_pass + (err_pass+err_fail)/(y_pass+y_fail))
	#err1_b = ratio1_b*(err_pass/y_pass + (err_totl)/(y_totl))

	#ratio2_b = ratio1_b/(1-ratio1_b)
	ratio2_b = y_pass/y_fail
	#err2_b = ratio2_b*(2*(err1_b/ratio1_b))
	err2_b = ratio2_b*(err_pass/y_pass + err_fail/y_fail)

	del y_pass, y_fail, err_pass, err_fail

	#nbins=[5,10,15,20,30,60]
	if len(nbins)<2:
		y_pass, y_fail = np.zeros(nbins), np.zeros(nbins)
		err_pass, err_fail = np.zeros(nbins), np.zeros(nbins)
	else:
		y_pass, y_fail = np.zeros(len(nbins)-1), np.zeros(len(nbins)-1)
		err_pass, err_fail = np.zeros(len(nbins)-1), np.zeros(len(nbins)-1)
	s_for_fake = ["ZZTo4L","WZTo3LNu","DYJetsToLL_M0To1","data"]
	for i in range(len(s)):
		if s[i] not in s_for_fake: continue
		sam = data[s[i]]

		passes = sam["selection_pass"]*(np.abs(sam["etaL3"])>1.2)
		failes = sam["selection_fail"]*(np.abs(sam["etaL3"])>1.2)

		pass_pt = sam["pTL3"][passes]
		fail_pt = sam["pTL3"][failes]

		#Calculate Weights
		#weight_arr_pass = sam["weight"]*sam["genWeight"][passes]*sam["pileupWeight"][passes]
		#weight_arr_fail = sam["weight"]*sam["genWeight"][failes]*sam["pileupWeight"][failes]
		weight_arr_pass = sam["weight"][passes]*sam["genWeight"][passes]*sam["pileupWeight"][passes]
		weight_arr_fail = sam["weight"][failes]*sam["genWeight"][failes]*sam["pileupWeight"][failes]

		#Calculate Errors
		#t_pass,binEdges = np.histogram(pass_pt,bins=nbins,range=(nbins[0],nbins[-1]))
		#t_fail,binEdges = np.histogram(fail_pt,bins=nbins,range=(nbins[0],nbins[-1]))
		#er_pass = np.sqrt(np.abs(t_pass))*sam["weight"]
		#er_fail = np.sqrt(np.abs(t_fail))*sam["weight"]

		t_pass,binEdges_pass = np.histogram(pass_pt,bins=nbins,range=(nbins[0],nbins[-1]),weights=weight_arr_pass)
		t_fail,binEdges_fail = np.histogram(fail_pt,bins=nbins,range=(nbins[0],nbins[-1]),weights=weight_arr_fail)
		er_pass = np.sqrt(np.histogram(pass_pt,bins=nbins,range=(nbins[0],nbins[-1]),weights=weight_arr_pass**2)[0])
		er_fail = np.sqrt(np.histogram(fail_pt,bins=nbins,range=(nbins[0],nbins[-1]),weights=weight_arr_fail**2)[0])

		if s[i]=="data":
			y_pass += t_pass
			y_fail += t_fail
		else:
			y_pass -= t_pass
			y_fail -= t_fail
		err_pass += er_pass
		err_fail += er_fail

	ratio1_e = y_pass/(y_pass+y_fail)
	err1_e = ratio1_e*(err_pass/y_pass + (err_pass+err_fail)/(y_pass+y_fail))

	#ratio2_e = ratio1_e/(1-ratio1_e)
	ratio2_e = y_pass/y_fail
	#err2_e = ratio2_e*(2*(err1_e/ratio1_e))
	err2_e = ratio2_e*(err_pass/y_pass + err_fail/y_fail)

	errx = np.zeros(len(ratio1_e))
	for i in range(len(ratio1_e)):
		errx[i] = (nbins[i+1]-nbins[i])/2

	bincenters = 0.5*(binEdges_pass[1:]+binEdges_pass[:-1])
	plt.errorbar(bincenters,ratio1_b,yerr=err1_b,xerr=errx,marker='o',ls='',label='barrel')
	plt.errorbar(bincenters,ratio1_e,yerr=err1_e,xerr=errx,marker='o',ls='',label='endcap')
	plt.ylim(bottom=0,top=.4)
	#plt.xlim(left=nbins[0],right=nbins[-1])
	plt.xlim(left=0,right=nbins[-1])
	plt.title("Fake Rate")
	plt.xlabel("Muon pT (GeV)")
	plt.ylabel("pass/total")
	plt.legend(loc='best')
	plt.savefig("/orange/avery/nikmenendez/Output/%s/%s.png"%(out,"FakeRate_fail_total"))
	plt.clf()

	bincenters = 0.5*(binEdges_pass[1:]+binEdges_pass[:-1])
	plt.errorbar(bincenters,ratio2_b,yerr=err2_b,xerr=errx,marker='o',ls='',label='barrel')
	plt.errorbar(bincenters,ratio2_e,yerr=err2_e,xerr=errx,marker='o',ls='',label='endcap')
	plt.ylim(bottom=0,top=.4)
	#plt.xlim(left=nbins[0],right=nbins[-1])
	plt.xlim(left=0,right=nbins[-1])
	plt.title("Fake Weight")
	plt.xlabel("Muon pT (GeV)")
	plt.ylabel("f/(1-f)")
	plt.legend(loc='best')
	plt.savefig("/orange/avery/nikmenendez/Output/%s/%s.png"%(out,"FakeRate_pass_fail"))
	plt.clf()


	return ratio2_b, ratio2_e
