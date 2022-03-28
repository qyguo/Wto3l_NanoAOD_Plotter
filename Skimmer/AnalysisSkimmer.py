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
	
	selection = data['nMuons'] > -1

	selection, eff["di-e Mass >= 4.0"] 	= cut((data["M1"] >= 4.0), selection)
	selection, eff["M1 Upsilon Veto"]	= cut((data["M1"] < 9.0) | (data["M1"] > 11.), selection)
	#selection, eff["M1 J/Psi Veto"]		= cut((data["M1"] < 2.9) | (data["M1"] > 3.9), selection)
	selection, eff["Leading e pT > 25"] = cut((data["pTL1"]>25), selection)
	selection, eff["Subleading e pT > 15"] = cut((data["pTL2"]>15), selection)

	selection, eff["No b Jets"]			= cut((data["nbJets"]==0), selection)
	selection, eff[">=1 Good Muon"]		= cut((data["nGoodMuons"]>=1), selection)
	selection, eff["medId True"]		= cut((data['medIdL3'] == 1), selection)
	selection, eff["Isolation < 5.0"]	= cut((data["IsoL3"]<5.0), selection)
	selection, eff["SIP3D <= 3.2"]		= cut((data["sip3dL3"]<=3.2), selection)

	selection, eff["MET < 40"]          = cut((data["met"]<40), selection)
	selection, eff["Only 3 leptons"]	= cut((data["nLeptons"]==3), selection)

	selection, eff["M1 Around Z"]		= cut((data["M1"]>(91-10))&(data["M1"]<(91+10)),selection)

	#selection, eff["Iso Cut"] = cut((data["IsoL3"]>0.33), selection)

	if np.count_nonzero(selection)!=0:
		eff["Overall"] = np.count_nonzero(selection)/len(data['nMuons'])*100
	else:
		eff["Overall"] = 0

	return selection, eff

def skim_val(data):
	
	eff = {}
	
	selection = data['nMuons'] > -1

	selection, eff["di-e Mass >= 4"] 	= cut((data["M1"] >= 4), selection)
	selection, eff["M1 Upsilon Veto"]	= cut((data["M1"] < 9.0) | (data["M1"] > 11.), selection)
	selection, eff["M1 J/Psi Veto"]		= cut((data["M1"] < 2.9) | (data["M1"] > 3.9), selection)
	selection, eff["Leading e pT > 25"] = cut((data["pTL1"]>25), selection)
	selection, eff["Subleading e pT > 15"] = cut((data["pTL2"]>15), selection)

	selection, eff["No b Jets"]			= cut((data["nbJets"]==0), selection)
	selection, eff[">=1 Good Muon"]		= cut((data["nGoodMuons"]>=1), selection)
	selection, eff["medId True"]		= cut((data['medIdL3'] == 1), selection)
	selection, eff["Isolation < 5.0"]	= cut((data["IsoL3"]<5.0), selection)
	selection, eff["SIP3D <= 3.2"]		= cut((data["sip3dL3"]<=3.2), selection)

	selection, eff["MET < 40"]          = cut((data["met"]<40), selection)
	selection, eff["Only 3 leptons"]    = cut((data["nLeptons"]==3), selection)

	selection, eff["M1 Not Around Z"]	= cut(~((data["M1"]>(91-10))&(data["M1"]<(91+10))),selection)

	return selection, eff

def skim_flip(data,eff,s):

	iso = 0.3
	
	selection = data['selection']
	
	fail = selection * data["IsoL3"]>iso
	if "fake" in s:
		selection, eff["Iso Cut"] = cut((data["IsoL3"]>iso), selection)
	else:
		selection, eff["Iso Cut"] = cut((data["IsoL3"]<iso), selection)

	if np.count_nonzero(selection)!=0:
		eff["Overall"] = np.count_nonzero(selection)/len(data['nMuons'])*100
	else:
		eff["Overall"] = 0

	return selection, eff, fail
