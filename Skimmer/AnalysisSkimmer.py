import numpy as np

np.seterr(all='ignore')

def cut(data,selection):

	selection2 = data * selection
	if np.count_nonzero(selection)!=0:
		eff = np.count_nonzero(selection2)/np.count_nonzero(selection)*100
	else:
		eff = 0
	return selection2, eff

def skim(data):
	
	eff = {}
	
	iso_pre = 2.0
	iso_cut = 0.3
	Z_diff = 7

	selection = data['nMuons'] > -1

	selection, eff["di-e Mass >= 4.0"] 	= cut((data["M1"] >= 4.0), selection)
	selection, eff["M1 Upsilon Veto"]	= cut((data["M1"] < 9.0) | (data["M1"] > 11.), selection)
	selection, eff["Leading e pT > 25"] = cut((data["pTL1"]>25), selection)
	selection, eff["Subleading e pT > 15"] = cut((data["pTL2"]>15), selection)

	selection, eff["No b Jets"]			= cut((data["nbJets"]==0), selection)
	selection, eff[">=1 Good Muon"]		= cut((data["nGoodMuons"]>=1), selection)
	selection, eff["MET < 25"]          = cut((data["met"]<25), selection)
	selection, eff["Only 3 leptons"]	= cut((data["nLeptons"]==3), selection)
	selection, eff["e/mu sep"]		 	= cut(((data["dR13"]>0.1)&(data["dR23"]>0.1)), selection)
	selection, eff["M1 Around Z"]		= cut((data["M1"]>(91-Z_diff))&(data["M1"]<(91+Z_diff)),selection)

	# General Tight Cuts
	#selection, eff["SIP3D <= 3.2"]		= cut((data["sip3dL3"]<=3.2), selection)
	#selection, eff["dxy <= 0.02"]		= cut((data["dxyL3"]<=0.02), selection)
	#selection, eff["dz <= 0.02"]		= cut((data["dzL3"]<=0.02), selection)

	# General Loose Cuts
	selection, eff["SIP3D <= 4.0"]		= cut((data["sip3dL3"]<=4.0), selection)
	selection, eff["dxy <= 0.05"]		= cut((data["dxyL3"]<=0.05), selection)
	selection, eff["dz <= 0.1"]			= cut((data["dzL3"]<=0.1), selection)

	#selection, eff["muPt < 15"]			= cut((data["pTL3"]<15), selection)

	# For Iso Selection
	##selection, eff["Isolation < %.1f"%(iso_pre)]	= cut((data["IsoL3"]<iso_pre), selection)
	##selection, eff["SIP3D <= 10"]		= cut((data["sip3dL3"]<=10), selection)
	#selection, eff["medId True"]					= cut((data['medIdL3'] == 1), selection)
	##passes = (data["IsoL3"]<iso_cut)*selection
	##fail = (data["IsoL3"]>iso_cut)*selection
	#passes = ((data["IsoL3"]<iso_cut)*selection) & ((data["sip3dL3"]<=4)*selection)
	#fail = ((data["IsoL3"]>iso_cut)*selection) | ((data["sip3dL3"]>4)*selection)
	
	# Checking
	#selection, eff["softId"]			= cut((data["softIdL3"]==1), selection)
	#selection, eff["softMvaId"]			= cut((data["softMvaIdL3"]==1), selection)
	#selection, eff["highPtId"]			= cut((data["highPtIdL3"]==2), selection)
	#selection, eff["allId"]	= cut(((data["looseIdL3"]==1)|(data["softIdL3"]==1)|(data["softMvaIdL3"]==1)|(data["highPtIdL3"]>0)), selection)

	# For MVA Selection
	#selection, eff["Isolation < 0.3"]	= cut((data["IsoL3"]<0.3), selection)
	#selection, eff["medId True"]		= cut((data['medIdL3'] == 1), selection)
	selection, eff["looseId True"]		= cut((data['looseIdL3'] == 1), selection)
	#selection, eff["mvaId loose"]		= cut(data["mvaIdL3"]>0, selection)
	passes = ((data["mvaIdL3"]>1)&(data["IsoL3"]<0.3))*selection
	fail =   ((data["mvaIdL3"]<2)|(data["IsoL3"]>0.3))*selection
	#selection, eff["notTight"] 			= cut(((data["mvaIdL3"]<2)|(data["IsoL3"]>0.3)), selection)
	#selection, eff["Tight"]		 			= cut(((data["mvaIdL3"]>1)&(data["IsoL3"]<0.3)), selection)
	#selection, eff["mvaId med"]			= cut(data["mvaIdL3"]>1, selection)

	if np.count_nonzero(selection)!=0:
		eff["Overall"] = np.count_nonzero(selection)/len(data['nMuons'])*100
	else:
		eff["Overall"] = 0

	return selection, eff, fail, passes

def skim_val(data):
	
	eff = {}
	
	selection = data['nMuons'] > -1

	selection, eff["di-e Mass >= 4.0"] 	= cut((data["M1"] >= 4.0), selection)
	selection, eff["M1 Upsilon Veto"]	= cut((data["M1"] < 9.0) | (data["M1"] > 11.), selection)
	selection, eff["Leading e pT > 25"] = cut((data["pTL1"]>25), selection)
	selection, eff["Subleading e pT > 15"] = cut((data["pTL2"]>15), selection)

	selection, eff["No b Jets"]			= cut((data["nbJets"]==0), selection)
	selection, eff[">=1 Good Muon"]		= cut((data["nGoodMuons"]>=1), selection)
	selection, eff["MET < 40"]          = cut((data["met"]<40), selection)
	selection, eff["Only 3 leptons"]	= cut((data["nLeptons"]==3), selection)
	selection, eff["M1 Not Around Z"]	= cut(~((data["M1"]>(91-10))&(data["M1"]<(91+10))),selection)

	# General Tight Cuts
	#selection, eff["SIP3D <= 3.2"]		= cut((data["sip3dL3"]<=3.2), selection)
	#selection, eff["dxy <= 0.02"]		= cut((data["dxyL3"]<=0.02), selection)
	#selection, eff["dz <= 0.02"]		= cut((data["dzL3"]<=0.02), selection)

	# General Loose Cuts
	selection, eff["SIP3D <= 4.0"]		= cut((data["sip3dL3"]<=4.0), selection)
	selection, eff["dxy <= 0.05"]		= cut((data["dxyL3"]<=0.05), selection)
	selection, eff["dz <= 0.1"]			= cut((data["dzL3"]<=0.1), selection)

	# For Iso Selection
	##selection, eff["Isolation < 2.0"]	= cut((data["IsoL3"]<2.0), selection)
	#selection, eff["medId True"]		= cut((data['medIdL3'] == 1), selection)
	
	# For MVA Selection
	selection, eff["Isolation < 0.3"]	= cut((data["IsoL3"]<0.3), selection)
	#selection, eff["medId True"]		= cut((data['medIdL3'] == 1), selection)
	#selection, eff["mvaId loose"]		= cut(data["mvaIdL3"]>0, selection)
	#selection, eff["looseId True"]		= cut((data['looseIdL3'] == 1), selection)

	return selection, eff

def skim_flip(data,eff,s):

	iso = 0.3
	mva = 1
	
	selection = data['selection']
	
	#fail = selection * data["IsoL3"]>iso
	#if "fake" in s:
	#	selection, eff["Iso Cut"] = cut((data["IsoL3"]>iso), selection)
	#else:
	#	selection, eff["Iso Cut"] = cut((data["IsoL3"]<iso), selection)

	fail = selection * ((data["mvaIdL3"]<=mva)|(data["IsoL3"]>iso))
	if "fake" in s:
		selection, eff["med mvaId"] = cut((data["mvaIdL3"]<=mva), selection)
		selection, eff["Iso Cut"] = cut((data["IsoL3"]>iso), selection)
	else:
		selection, eff["med mvaId"] = cut((data["mvaIdL3"]>mva), selection)
		selection, eff["Iso Cut"] = cut((data["IsoL3"]<iso), selection)

	#fail = (selection*(data["IsoL3"]>iso)) | (selection*(data["sip3dL3"]>4))
	#if "fake" in s:
	#	selection, eff["Iso Cut"] = cut((data["IsoL3"]>iso), selection)
	#	selection, eff["Sip Cut"] = cut((data["sip3dL3"]>4), selection)
	#else:
	#	selection, eff["Iso Cut"] = cut((data["IsoL3"]<iso), selection)
	#	selection, eff["Sip Cut"] = cut((data["sip3dL3"]<=4), selection)

	if np.count_nonzero(selection)!=0:
		eff["Overall"] = np.count_nonzero(selection)/len(data['nMuons'])*100
	else:
		eff["Overall"] = 0

	return selection, eff, fail
