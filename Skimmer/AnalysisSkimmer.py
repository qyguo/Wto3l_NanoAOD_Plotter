import numpy as np

np.seterr(all='ignore')

def cut(data,selection):

	selection2 = data * selection
	if np.count_nonzero(selection!=0):
		eff = np.count_nonzero(selection2)/np.count_nonzero(selection)*100
	else:
		eff = 0
	return selection2, eff

def skim(data):
	
	eff = {}
	
	selection = data['nMuons'] > 0

	selection, eff["diMu Mass > 1.1"] 	= cut((data["M1"] > 1.1), selection)
	selection, eff["M1 Upsilon Veto"]	= cut((data["M1"] < 9.0) | (data["M1"] > 11.), selection)
	selection, eff["M1 J/Psi Veto"]		= cut((data["M1"] < 2.9) | (data["M1"] > 3.9), selection)
	#selection, eff["medId True"]		= cut((data['medIdL3'] == 1), selection)
	#selection, eff["Isolation < 0.1"]	= cut((data["IsoL3"]<0.1), selection)
	#selection, eff["SIP3D < 4"]			= cut((data["sip3dL3"]<4), selection)
	selection, eff["medId, Iso, or SIP"]= cut((data['medIdL3']==0) | (data["IsoL3"]>0.1) | (data["sip3dL3"]>4), selection)

	return selection, eff
