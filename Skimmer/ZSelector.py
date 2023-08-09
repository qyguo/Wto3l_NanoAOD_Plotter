import numpy as np
import uproot3_methods
#import uproot_methods
#from ROOT import TLorentzVector

def select(data):

	Lep1 = uproot3_methods.classes.TLorentzVector.PtEtaPhiMassLorentzVectorArray(data['pTL1'],data['etaL1'],data['phiL1'],data['massL1'])
	Lep2 = uproot3_methods.classes.TLorentzVector.PtEtaPhiMassLorentzVectorArray(data['pTL2'],data['etaL2'],data['phiL2'],data['massL2'])
	Lep3 = uproot3_methods.classes.TLorentzVector.PtEtaPhiMassLorentzVectorArray(data['pTL3'],data['etaL3'],data['phiL3'],data['massL3'])

	data["m3l_pt"] = (Lep1 + Lep2 + Lep3).pt

	# Define 3 possible Zp combinations
	P1 = Lep1 + Lep2
	#P2 = Lep1 + Lep3
	#P3 = Lep2 + Lep3
	
	# Define 3 groups of possible combinations of muons
	#data["p1"] = data['idL1']!=data['idL2']
	#data["p2"] = data['idL1']!=data['idL3']
	#data["p3"] = data['idL2']!=data['idL3']
	
	# --------- Define Mass1 as (not) the highest pT muon + highest pT anti-muon -------------------------------------
	#M0 = (P1).mass*np.logical_not(data["p1"]) + (P2).mass*np.logical_not(data["p2"]) + (P3).mass*np.logical_not(data["p3"])
	#M1 = (P3).mass*data["p3"] + (P2).mass*(data["p2"] & np.logical_not(data["p3"]))
	#M2 = (P1).mass*data["p1"] + (P2).mass*(data["p2"] & np.logical_not(data["p1"]))
	#data["dRM1"] = data['dR12']*data["p1"] + data['dR13']*(data["p2"] & np.logical_not(data["p1"]))
	#data["dRM2"] = data['dR23']*data["p3"] + data['dR13']*(data["p2"] & np.logical_not(data["p3"]))
	#data["M0"] = M0
	#data["M1"] = np.fmax(M1,M2) # pick higher mass possible pair
	#data["M2"] = np.fmin(M1,M2) # pick lowest mass possible pair
	# ----------------------------------------------------------------------------------------------------------------

	data["M1"] = (P1).mass
	data["M1T"] = (P1).mt

	return data
