import numpy as np

def Fake_weight(data,s):

	leps = ["L1","L2","L3"]

	fw_final = np.ones(len(data["etaL3"]))
	#fw_final = np.zeros(len(data["etaL3"]))
	for l in leps:
		pt_bins = [5, 10, 15, 20, 30, 60]
		
		# Pileup 32
		fwb = [0.54823178, 0.40137622, 0.16208735, 0.15421977, -0.36649778]
		fwe = [0.79422282, 0.70340139, 0.68224924, 0.26550132, 1.18573958]

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

		fw = fwb_final + fwe_final
		for i in range(len(fw)):
			if fw[i]==0: fw[i]=1
		fw_final *= fw
		#fw_final += fw

	return fw_final
