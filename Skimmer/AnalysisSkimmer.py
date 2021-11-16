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

	selection, eff["diMu Mass > 1.1"] 	= cut((data["M1"] > 1.1), selection)
	selection, eff["M1 Upsilon Veto"]	= cut((data["M1"] < 9.0) | (data["M1"] > 11.), selection)
	selection, eff["M1 J/Psi Veto"]		= cut((data["M1"] < 2.9) | (data["M1"] > 3.9), selection)
	selection, eff["Leading e pT > 25"] = cut((data["pTL1"]>25), selection)
	selection, eff["Subleading e pT > 15"] = cut((data["pTL2"]>15), selection)

	selection, eff["No b Jets"]			= cut((data["nbJets"]==0), selection)
	selection, eff["1 Good Muon"]		= cut((data["nGoodMuons"]==1), selection)
	selection, eff["medId True"]		= cut((data['medIdL3'] == 1), selection)
	selection, eff["Isolation < 0.6"]	= cut((data["IsoL3"]<0.6), selection)
	selection, eff["SIP3D < 4"]			= cut((data["sip3dL3"]<4), selection)

	selection, eff["MET < 30"]          = cut((data["met"]<30), selection)

	selection, eff["M1 Around Z"]		= cut((data["M1"]>(91-15))&(data["M1"]<(91+15)),selection)

	if np.count_nonzero(selection)!=0:
		eff["Overall"] = np.count_nonzero(selection)/len(data['nMuons'])*100
	else:
		eff["Overall"] = 0

	return selection, eff

def skim_val(data):
	
	eff = {}
	
	selection = data['nMuons'] > -1

	selection, eff["diMu Mass > 1.1"] 	= cut((data["M1"] > 1.1), selection)
	selection, eff["M1 Upsilon Veto"]	= cut((data["M1"] < 9.0) | (data["M1"] > 11.), selection)
	selection, eff["M1 J/Psi Veto"]		= cut((data["M1"] < 2.9) | (data["M1"] > 3.9), selection)
	selection, eff["Leading e pT > 25"] = cut((data["pTL1"]>25), selection)
	selection, eff["Subleading e pT > 15"] = cut((data["pTL2"]>15), selection)

	selection, eff["No b Jets"]			= cut((data["nbJets"]==0), selection)
	selection, eff["1 Good Muon"]		= cut((data["nGoodMuons"]==1), selection)
	selection, eff["medId True"]		= cut((data['medIdL3'] == 1), selection)
	selection, eff["Isolation < 0.6"]	= cut((data["IsoL3"]<0.6), selection)
	selection, eff["SIP3D < 4"]			= cut((data["sip3dL3"]<4), selection)

	selection, eff["MET < 30"]          = cut((data["met"]<30), selection)

	selection, eff["M1 Not Around Z"]	= cut(~((data["M1"]>(91-15))&(data["M1"]<(91+15))),selection)

	return selection, eff

def skim_flip(data,eff,s):

	iso = 0.1
	
	selection = data['selection']
	
	if "fake" in s:
		selection, eff["Iso Cut"] = cut((data["IsoL3"]>iso), selection)
	else:
		selection, eff["Iso Cut"] = cut((data["IsoL3"]<iso), selection)

	if np.count_nonzero(selection)!=0:
		eff["Overall"] = np.count_nonzero(selection)/len(data['nMuons'])*100
	else:
		eff["Overall"] = 0

	return selection, eff
