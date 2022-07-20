#input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/signal_sel/Eff/"
input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/signal_sel/UL/"
#masses = [4,5,15,30,45,60]
masses = [5,15,30,45,60]
xs_sig = {	"Wto3l_M4":  7.474,
		"Wto3l_M5":  5.453,
		"Wto3l_M15": 1.0042,
		"Wto3l_M30": 0.17985,
#		"Wto3l_M30_New": 0.19361,
		"Wto3l_M45": 0.02502214,
		"Wto3l_M60": 0.0021799,}
#xs_sig = {	"Wto3l_M4":  10,
#		"Wto3l_M5":  50,
#		"Wto3l_M15": 10,
#		"Wto3l_M30": 10,
##		"Wto3l_M30_New": 10,
#		"Wto3l_M45": 10,
#		"Wto3l_M60": 10,}
##		"Wto3l_M1": 10}
sumW_sig = {"Wto3l_M4":  100000,
		"Wto3l_M5":  500000,
		"Wto3l_M15": 100000,
		"Wto3l_M30": 100000,
		"Wto3l_M45":  99000,
		"Wto3l_M60": 100000,}
#		"Wto3l_M1":  100000}

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
"gen_dPtL1",
"gen_dPtL2",
"gen_dPtL3",
"gen_dRL1",
"gen_dRL2",
"gen_dRL3",
]
