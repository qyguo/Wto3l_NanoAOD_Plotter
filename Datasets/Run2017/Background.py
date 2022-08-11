#input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/signal_sel/Eff/"
input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/signal_sel/UL/"
#input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/Eff/"
xs_bkg = {}
sumW_bkg = {}

background_samples = []
background_files = {}

def read_sumW(sumW_file):
	file_sumW = open(sumW_file)
	sumW = float(file_sumW.read())
	file_sumW.close
	return sumW


sam = "DYJetsToLL_M1To10"
#background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 2037.0
#sumW_bkg[sam] = 24227000.0
sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam))

sam = "DYJetsToLL_M10To50"
#background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 18610.0
#sumW_bkg[sam] = 68480179.0 #78994955.0
sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam))

sam = "DYJetsToLL_M50"
#background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 6077.22
#sumW_bkg[sam] = 201650476.0 #3782668437151.0
sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam))

sam = "DYJetsToLL_M0To1"
#background_samples.append(sam)
background_files[sam] = "%sDYJetsToLL_M50_M0To1.root"%(input_dir)
xs_bkg[sam] = 6077.22
#sumW_bkg[sam] = 201650476.0 #3782668437151.0
sumW_bkg[sam] = read_sumW("%ssumW/DYJetsToLL_M50_M0To1.txt"%(input_dir))

sam = "TTJets_DiLept"
#background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 54.23
#sumW_bkg[sam] = 10018000.0 #28349068.0
sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam))

sam = "WZTo3LNu"
#background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 5.052
#sumW_bkg[sam] = 87559049.0 #94563223.0
sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam))

#sam = "ZZTo4L"
##background_samples.append(sam)
#background_files[sam] = "%s%s.root"%(input_dir,sam)
#xs_bkg[sam] = 1.369
##sumW_bkg[sam] = 131669254.0 #55658966.0
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam))

sam = "ZZTo4L"
#background_samples.append(sam)
background_files[sam] = "%s%s_M1Toinf.root"%(input_dir,sam)
xs_bkg[sam] = 13.74
#sumW_bkg[sam] = 131669254.0 #55658966.0
sumW_bkg[sam] = read_sumW("%ssumW/%s_M1Toinf.txt"%(input_dir,sam))

sam = "WJetsToLNu"
#background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 61526.7
#sumW_bkg[sam] = 1030816975.0 #77631180.0
sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam))

sam = "WWTo2L2Nu"
#background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 12.178
#sumW_bkg[sam] = 78687950.0 #22155848.0
sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam))

background_samples = ["ZZTo4L","WZTo3LNu","TTJets_DiLept","DYJetsToLL_M50","DYJetsToLL_M10To50","DYJetsToLL_M1To10","WJetsToLNu","WWTo2L2Nu","DYJetsToLL_M0To1"]
#background_samples = ["ZZTo4L_M1Toinf","WZTo3LNu","TTJets_DiLept","DYJetsToLL_M50","DYJetsToLL_M10To50","DYJetsToLL_M1To10","WJetsToLNu","WWTo2L2Nu"]

background_vars = [
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
#"photon_mass",
]
