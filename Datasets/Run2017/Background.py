input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/ZpX/Eff/"
xs_bkg = {}
sumW_bkg = {}

background_samples = []
background_files = {}
	
sam = "DYJetsToLL_M1To10"
background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 2037.0
sumW_bkg[sam] = 24227000.0

sam = "DYJetsToLL_M10To50"
background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 18610.0
sumW_bkg[sam] = 78994955.0

sam = "DYJetsToLL_M50"
background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 6077.22
sumW_bkg[sam] = 3782668437151.0

sam = "TTJets_DiLept"
background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 54.23
sumW_bkg[sam] = 28349068.0

sam = "WZTo3LNu"
background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 5.052
sumW_bkg[sam] = 94563223.0

sam = "ZZTo4L"
background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 1.369
sumW_bkg[sam] = 55658966.0

sam = "WJetsToLNu"
background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 61526.7
sumW_bkg[sam] = 77631180.0

sam = "WWTo2L2Nu"
background_samples.append(sam)
background_files[sam] = "%s%s.root"%(input_dir,sam)
xs_bkg[sam] = 12.178
sumW_bkg[sam] = 22155848.0


signal_vars = [
"genWeight",
"pileupWeight",
"nMuons",
"nGoodMuons",
"nbJets",
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
"maxdxy",
"maxdz",
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
]
