import numpy as np

np.seterr(all='ignore')

def cut(data,selection):

	selection2 = data * selection
	if np.count_nonzero(selection)!=0:
		eff = np.count_nonzero(selection2)/np.count_nonzero(selection)*100
	else:
		eff = 0
	return selection2, eff

def skim(data,s):
	
	eff = {}
	iso_check = 999.0
	
	selection = data['nMuons'] > -1

	#selection, eff["diMu Mass > 1.1"] 	= cut((data["M1"] > 1.1) & (data["M2"] > 1.1), selection)
	selection, eff["diMu Mass > 4.0"] 	= cut((data["M1"] >= 4.0) & (data["M2"] >= 4.0), selection)
	selection, eff["M1 Upsilon Veto"]	= cut((data["M1"] < 9.0) | (data["M1"] > 11.), selection)
	selection, eff["M2 Upsilon Veto"]	= cut((data["M2"] < 9.0) | (data["M2"] > 11.), selection)
	#selection, eff["M1 J/Psi Veto"]		= cut((data["M1"] < 2.9) | (data["M1"] > 3.9), selection)
	#selection, eff["M2 J/Psi Veto"]		= cut((data["M2"] < 2.9) | (data["M2"] > 3.9), selection)
	#seleciton, eff["pTL1 > 12"]		 	= cut(data['pTL1'] > 12, selection)
	#selection, eff["pTL2 > 10"]			= cut(data['pTL2'] > 10, selection)
	#selection, eff["pTL3 > 5"]			= cut(data['pTL3'] > 5 , selection)
	#selection, eff["Iso < 0.6"]			= cut((data['IsoL1'] < 0.6)  & (data['IsoL2'] < 0.6)  & (data['IsoL3'] < 0.6), selection)
	#selection, eff["medId True"]		= cut((data['medIdL1'] == 1) & (data['medIdL2'] == 1) & (data['medIdL3'] == 1), selection)

	selection, eff["m3l < 83 GeV"]		= cut((data["m3l"] < 83), selection)

	fail_Iso = (data['IsoL1'] > iso_check).astype(int)  + (data['IsoL2'] > iso_check).astype(int)  + (data['IsoL3'] > iso_check).astype(int)

	fail = (fail_Iso==1) * selection
	fail2= (fail_Iso==2) * selection
	if "fake" in s:
		#selection, eff["Iso Cut"]		= cut((fail_Iso==1) | (fail_Iso==2), selection)
		selection, eff["Iso Cut"]		= cut((fail_Iso==1), selection)
	else:
		selection, eff["Iso Cut"]		= cut(fail_Iso==0, selection)

	if np.count_nonzero(selection)!=0:
		eff["Overall"] = np.count_nonzero(selection)/len(data['nMuons'])*100
	else:
		eff["Overall"] = 0

	return selection, eff, fail, fail2

def skim_opt(data,s):

	eff = {}

	selection = data['nMuons'] > -1

	selection, eff["diMu Mass > 1.1"] 	= cut((data["M1"] > 1.1) & (data["M2"] > 1.1), selection)
	selection, eff["M1 Upsilon Veto"]	= cut((data["M1"] < 9.0) | (data["M1"] > 11.), selection)
	selection, eff["M2 Upsilon Veto"]	= cut((data["M2"] < 9.0) | (data["M2"] > 11.), selection)
	selection, eff["M1 J/Psi Veto"]		= cut((data["M1"] < 2.9) | (data["M1"] > 3.9), selection)
	selection, eff["M2 J/Psi Veto"]		= cut((data["M2"] < 2.9) | (data["M2"] > 3.9), selection)

	selection, eff["m3l < 83 GeV"]      = cut((data["m3l"] < 83), selection)
	seleciton, eff["pTL1 > 12"]		 	= cut(data['pTL1'] > 12, selection)
	selection, eff["pTL2 > 10"]			= cut(data['pTL2'] > 10, selection)
	selection, eff["pTL3 > 5"]			= cut(data['pTL3'] > 5 , selection)
	selection, eff["medId True"]        = cut((data['medIdL1'] == 1) & (data['medIdL2'] == 1) & (data['medIdL3'] == 1), selection)

	return selection
