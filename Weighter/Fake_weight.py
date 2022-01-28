import numpy as np

def Fake_weight(data,s):

	leps = ["L1","L2","L3"]

	fw_final = np.ones(len(data["etaL3"]))
	#fw_final = np.zeros(len(data["etaL3"]))
	for l in leps:
		pt_bins = [5, 10, 15, 20, 30, 60]
		
		# Pileup 32
		#fwb = [0.54823178, 0.40137622, 0.16208735, 0.15421977, -0.36649778]
		#fwe = [0.79422282, 0.70340139, 0.68224924, 0.26550132, 1.18573958]

		# New Opt

		# Iso < 0.33 no fakeable
		#fwb = [0.3818576,  0.30205858, 0.20044748, 0.09918942, 0.00089526]
		#fwe = [0.66057115, 0.44614925, 0.61636559, 0.46715739, 0.39066091]

		# Iso < 0.30 fakeable Iso < 2.0
		fwb = [0.58944659, 0.44408208, 0.28621675, 0.13542638, -0.04005552]
		fwe = [0.91451714, 0.56766588, 0.75055791, 0.64323178, 0.47956011]

		barrel = np.abs(data["eta%s"%(l)]) <= 1.4
		endcap = np.abs(data["eta%s"%(l)]) >= 1.4

		pTbin = [0]*len(fwb)
		for i in range(len(pTbin)):
			pTbin[i] = (data["pT%s"%(l)] >= pt_bins[i]) & (data["pT%s"%(l)] < pt_bins[i+1]) & (data["Iso%s"%(l)] > 0.3)

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
