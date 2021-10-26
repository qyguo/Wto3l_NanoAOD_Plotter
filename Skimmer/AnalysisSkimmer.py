import numpy as np

np.seterr(all='ignore')

def cut(data,selection):

	selection2 = data * selection
	eff = np.count_nonzero(selection2)/np.count_nonzero(selection)*100
	return selection2, eff

def skim(data):
	
	eff = {}
	
	selection = data['nMuons'] > 0

	selection, eff["diMu Mass > 1.1"] 	= cut((data["M1"] > 1.1) & (data["M2"] > 1.1), selection)
	selection, eff["M1 Upsilon Veto"]	= cut((data["M1"] < 9.0) | (data["M1"] > 11.), selection)
	selection, eff["M2 Upsilon Veto"]	= cut((data["M2"] < 9.0) | (data["M2"] > 11.), selection)
	selection, eff["M1 J/Psi Veto"]		= cut((data["M1"] < 2.9) | (data["M1"] > 3.9), selection)
	selection, eff["M2 J/Psi Veto"]		= cut((data["M2"] < 2.9) | (data["M2"] > 3.9), selection)
	seleciton, eff["pTL1 > 12"]		 	= cut(data['pTL1'] > 12, selection)
	selection, eff["pTL2 > 10"]			= cut(data['pTL2'] > 10, selection)
	selection, eff["pTL3 > 5"]			= cut(data['pTL3'] > 5 , selection)
	selection, eff["Iso < 0.1"]			= cut((data['IsoL1'] < 0.1)  & (data['IsoL2'] < 0.1)  & (data['IsoL3'] < 0.1), selection)
	selection, eff["medId True"]		= cut((data['medIdL1'] == 1) & (data['medIdL2'] == 1) & (data['medIdL3'] == 1), selection)
	
	#fail_Iso = (data['IsoL1'] > 0.1).astype(int)  + (data['IsoL2'] > 0.1).astype(int)  + (data['IsoL3'] > 0.1).astype(int)
	#selection, eff["One Iso > 0.1"]		= cut(fail_Iso==2, selection)

	#fail_Med = (data['medIdL1'] != 1).astype(int) + (data['medIdL2'] != 1).astype(int) + (data['medIdL3'] != 1).astype(int)
	#selection, eff["One MedId False"]	= cut(fail_Med==1, selection)

	#fail_Eth = ((data['IsoL1']>0.1)|(data['medIdL1']!=1)).astype(int)  + ((data['IsoL2']>0.1)|(data['medIdL2']!=1)).astype(int)  + ((data['IsoL3']>0.1)|(data['medIdL3']!=1)).astype(int)
	#selection, eff["One Fail Iso or MedId"] = cut(fail_Eth==2, selection)

	return selection, eff
