#input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/signal_sel/Eff/"
##input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/signal_sel/UL/"
#input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/Eff/"
#input_dir = "/publicfs/cms/data/hzz/guoqy/Zprime/nikmenendez/skimmed/NanoAOD/2017/data/signal_sel/UL/"
input_dir = "/publicfs/cms/data/hzz/guoqy/Zprime/UL/2018/Ntuple/Data/signal_sel/UL/"

data_samples = ["data"]
#data_files = {"data": "%stotal_data_no_dupe.root"%(input_dir)}
#data_files = {"data": "%sData_UL18_DoubleMuon_MuonEG_noDuplicates.root"%(input_dir)}
data_files = {"data": "%sDoubleMuon_2018_noDuplicates.root"%(input_dir)}

data_samples.append("fake")
#data_files["fake"] = "%stotal_data_no_dupe.root"%(input_dir)
#data_files["fake"] = "%sData_UL18_DoubleMuon_MuonEG_noDuplicates.root"%(input_dir)
data_files["fake"] = "%sDoubleMuon_2018_noDuplicates.root"%(input_dir)

data_vars = [
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

