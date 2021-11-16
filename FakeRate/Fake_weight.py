import numpy as np

def Fake_weight(data,s,fwb,fwe,pt_bins):

	if "fake" not in s:
		return [1] * len(data["etaL3"])

	barrel = np.abs(data["etaL3"]) <= 1.4
	endcap = np.abs(data["etaL3"]) >= 1.4

	pTbin = [0]*len(fwb)
	for i in range(len(pTbin)):
		pTbin[i] = (data["pTL3"] >= pt_bins[i]) & (data["pTL3"] < pt_bins[i+1])

	fwb_final, fwe_final = 0,0
	for i in range(len(fwb)):
		fwb_final += pTbin[i]*fwb[i]
		fwe_final += pTbin[i]*fwe[i]
	fwb_final *= barrel
	fwe_final *= endcap

	fw_final = fwb_final + fwe_final

	#selection_fail = data["selection"]*(data["IsoL3"]>0.1)

	return fw_final
