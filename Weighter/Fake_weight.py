import numpy as np

def Fake_weight(data,s):

	if "fake" not in s:
		return [1] * len(data["etaL3"])

	leps = ["L1","L2","L3"]

	fw_final = np.zeros(len(data["etaL3"]))
	for l in leps:
		pt_bins = [5, 10, 15, 20, 30, 60]
		fwb = [0.57389336, 0.41465619, 0.23034944, 0.2342524, 0.45921181]
		fwe = [0.79351561, 0.68872168, 0.51601627, 0.19356343, -0.08037819]

		#fwb = [0.36463294, 0.29311446, 0.18722278, 0.18979294, 0.31469853]
		#fwe = [0.44243585, 0.40783611, 0.34037647, 0.16217272, -0.08740353]

		barrel = np.abs(data["eta%s"%(l)]) <= 1.4
		endcap = np.abs(data["eta%s"%(l)]) >= 1.4

		pTbin = [0]*len(fwb)
		for i in range(len(pTbin)):
			pTbin[i] = (data["pT%s"%(l)] >= pt_bins[i]) & (data["pT%s"%(l)] < pt_bins[i+1]) & (data["Iso%s"%(l)] > 0.1)

		fwb_final, fwe_final = 0,0
		for i in range(len(fwb)):
			fwb_final += pTbin[i]*fwb[i]
			fwe_final += pTbin[i]*fwe[i]
		fwb_final *= barrel
		fwe_final *= endcap

		fw_final += fwb_final + fwe_final

	return fw_final
