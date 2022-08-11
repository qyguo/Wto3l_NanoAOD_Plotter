#input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/signal_sel/Eff/"
input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/signal_sel/UL/"
#masses = [4,5,15,30,45,60]

#masses = [5,15,30,40,45,60,70]
#xs_sig = {	"Wto3l_M4":  7.474,
#		"Wto3l_M5":  5.453,
#		"Wto3l_M15": 1.0042,
#		"Wto3l_M30": 0.17985,
##		"Wto3l_M30_New": 0.19361,
#		"Wto3l_M40": 0.06842,
#		"Wto3l_M45": 0.02502214,
#		"Wto3l_M60": 0.0021799,
#		"Wto3l_M70": 0.0008662,}
##xs_sig = {	"Wto3l_M4":  10,
##		"Wto3l_M5":  50,
##		"Wto3l_M15": 10,
##		"Wto3l_M30": 10,
###		"Wto3l_M30_New": 10,
##		"Wto3l_M45": 10,
##		"Wto3l_M60": 10,}
###		"Wto3l_M1": 10}
#sumW_sig = {"Wto3l_M4":  100000,
#		"Wto3l_M5":  500000,
#		"Wto3l_M15": 100000,
#		"Wto3l_M30": 100000,
#		"Wto3l_M45":  99000,
#		"Wto3l_M40": 186362,
#		"Wto3l_M60": 100000,
#		"Wto3l_M70": 184381,}
##		"Wto3l_M1":  100000}

masses = [5, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
xs_sig_new = {	"m5":  3.255,     "p5":  4.17,
				"m15": 0.6864,    "p15": 0.8659,
				"m20": 0.3746,    "p20": 0.4600,
				"m25": 0.2046,    "p25": 0.2491,
				"m30": 0.1117,    "p30": 0.1367,
				"m35": 0.06028,   "p35": 0.07311,
				"m40": 0.03098,   "p40": 0.03744,
				"m45": 0.01537,   "p45": 0.01843,
				"m50": 0.007179,  "p50": 0.008727,
				"m55": 0.003207,  "p55": 0.003846,
				"m60": 0.001322,  "p60": 0.001692,
				"m65": 0.0005871, "p65": 0.0008043,
				"m70": 0.0003560, "p70": 0.0005102,
				"m75": 0.0002392, "p75": 0.0003758,
			 }
xs_err_new = {	"m5":  0.03366,   "p5": 0.02822,
				"m15": 0.005174,  "p15": 0.007221,
				"m20": 0.002926,  "p20": 0.002311,
				"m25": 0.001514,  "p25": 0.001323,
				"m30": 0.0008127, "p30": 0.000725,
				"m35": 0.0004161, "p35": 0.0004555,
				"m40": 0.0002478, "p40": 0.0001901,
				"m45": 0.0001217, "p45": 0.0001513,
				"m50": 5.679e-05, "p50": 7.805e-05,
				"m55": 3.839e-05, "p55": 3.117e-05,
				"m60": 1.064e-05, "p60": 2.192e-05,
				"m65": 5.764e-06, "p65": 1.472e-05,
				"m70": 1.504e-06, "p70": 4.247e-06,
				"m75": 8.201e-07, "p75": 1.413e-06,
			 }
xs_sig = {}
xs_err = {}
sumW_sig = {}
for m in masses:
	xs_sig["Wto3l_M%i"%(m)] = xs_sig_new["m%i"%(m)] + xs_sig_new["p%i"%(m)]
	xs_err["Wto3l_M%i"%(m)] = (xs_err_new["m%i"%(m)] + xs_err_new["p%i"%(m)])#/xs_sig["Wto3l_M%i"%(m)]

def read_sumW(sumW_file):
	file_sumW = open(sumW_file)
	sumW = float(file_sumW.read())
	file_sumW.close
	return sumW

signal_samples = []
signal_files = {}
for m in masses:
	signal_samples.append("Wto3l_M%i"%(m))
	signal_files["Wto3l_M%i"%(m)] = "%sWto3l_M%i.root"%(input_dir,m)
	#xs_sig["Wto3l_M%i"%(m)] *= 0.01
	xs_sig["Wto3l_M%i"%(m)] *= 1.3
	xs_err["Wto3l_M%i"%(m)] *= 1.3
	sumW_sig["Wto3l_M%i"%(m)] = read_sumW("%ssumW/Wto3l_M%i.txt"%(input_dir,m))
#signal_samples.append("Wto3l_M30_New")
#signal_files["Wto3l_M30_New"] = "%sWto3l_M30_New.root"%(input_dir)
#xs_sig["Wto3l_M30_New"] *= 0.01
#sumW_sig["Wto3l_M30_New"] = read_sumW("%ssumW/Wto3l_M30_New.txt"%(input_dir))

signal_vars = [
"genWeight",
"pileupWeight",
"nMuons",
"nGoodMuons",
"nbJets",
"nJets",
"idL1",
"idL2",
"idL3",
"pTL1",
"pTL2",
"pTL3",
"etaL1",
"etaL2",
"etaL3",
"phiL1",
"phiL2",
"phiL3",
"massL1",
"massL2",
"massL3",
"dxyL1",
"dxyL2",
"dxyL3",
"dzL1",
"dzL2",
"dzL3",
"IsoL1",
"IsoL2",
"IsoL3",
"ip3dL1",
"ip3dL2",
"ip3dL3",
"sip3dL1",
"sip3dL2",
"sip3dL3",
"tightIdL1",
"tightIdL2",
"tightIdL3",
"looseIdL1",
"looseIdL2",
"looseIdL3",
"medIdL1",
"medIdL2",
"medIdL3",
"mvaIdL1",
"mvaIdL2",
"mvaIdL3",
"sourceL1",
"sourceL2",
"sourceL3",
"met",
"met_phi",
"dR12",
"dR13",
"dR23",
"m3l",
"m4l",
"mt",
"passedDiMu1",
"passedDiMu2",
"passedTriMu",
"idL4",
"pTL4",
"etaL4",
"phiL4",
"massL4",
"dxyL4",
"dzL4",
"IsoL4",
"ip3dL4",
"sip3dL4",
"tightIdL4",
"medIdL4",
"mvaIdL4",
"softIdL1",
"softIdL2",
"softIdL3",
"softIdL4",
"inAcceptance",
#"gen_dPtL1",
#"gen_dPtL2",
#"gen_dPtL3",
#"gen_dRL1",
#"gen_dRL2",
#"gen_dRL3",
]
