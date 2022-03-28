import numpy as np

np.seterr(all='ignore')

def cut(data,selection):

	selection2 = data * selection
	if np.count_nonzero(selection)!=0:
		eff = np.count_nonzero(selection2)/np.count_nonzero(selection)*100
	else:
		eff = 0
	return selection2, eff

def fake_skim(data):

	selection = data['selection']

	selection_pass = selection*(data["IsoL3"]<0.3)
	selection_fail = selection*(data["IsoL3"]>0.3)

	return selection_pass, selection_fail
