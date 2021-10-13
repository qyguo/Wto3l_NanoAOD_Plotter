from __future__ import division
import numpy as np
import uproot
import sys
from tqdm import tqdm
import uproot_methods
import matplotlib.pyplot as plt
from Dataset.Signal import Wto3l

input_dir = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/signal_sel/Eff/"
masses = [4,5,10,15,30,60]
masses = [4]
xs = {"ZpM4": 7.474}
sumW = {"ZpM4": 100000}
lumi = 41.4*1000

for m in masses:
	weight = (xs["ZpM%i"%(m)]*.01)/sumW["ZpM%i"%(m)]*lumi
	print(weight)
	file = uproot.open(input_dir+"Wto3l_M%s.root"%(str(m)))
	events = file["passedEvents"]

	vars_in = ["pTL1","pTL2","pTL3","etaL1","etaL2","etaL3","phiL1","phiL2","phiL3","massL1","massL2","massL3","idL1","idL2","idL3","dR12","dR13","dR23","m3l","IsoL1","IsoL2","IsoL3","medIdL1","medIdL2","medIdL3"]
	data = events.arrays(vars_in)

	Lep1 = uproot_methods.classes.TLorentzVector.PtEtaPhiMassLorentzVectorArray(data[b'pTL1'],data[b'etaL1'],data[b'phiL1'],data[b'massL1'])
	Lep2 = uproot_methods.classes.TLorentzVector.PtEtaPhiMassLorentzVectorArray(data[b'pTL2'],data[b'etaL2'],data[b'phiL2'],data[b'massL2'])
	Lep3 = uproot_methods.classes.TLorentzVector.PtEtaPhiMassLorentzVectorArray(data[b'pTL3'],data[b'etaL3'],data[b'phiL3'],data[b'massL3'])

	# Define 3 possible Zp combinations
	P1 = Lep1 + Lep2
	P2 = Lep1 + Lep3
	P3 = Lep2 + Lep3
	
	# Define 3 groups of possible combinations of muons
	data["p1"] = data[b'idL1']!=data[b'idL2']
	data["p2"] = data[b'idL1']!=data[b'idL3']
	data["p3"] = data[b'idL2']!=data[b'idL3']

	# --------- Define Mass1 as (not) the highest pT muon + highest pT anti-muon -------------------------------------
	M0 = (P1).mass*np.logical_not(data["p1"]) + (P2).mass*np.logical_not(data["p2"]) + (P3).mass*np.logical_not(data["p3"])
	M1 = (P3).mass*data["p3"] + (P2).mass*(data["p2"] & np.logical_not(data["p3"]))
	M2 = (P1).mass*data["p1"] + (P2).mass*(data["p2"] & np.logical_not(data["p1"]))
	data["dRM1"] = data[b'dR12']*data["p1"] + data[b'dR13']*(data["p2"] & np.logical_not(data["p1"]))
	data["dRM2"] = data[b'dR23']*data["p3"] + data[b'dR13']*(data["p2"] & np.logical_not(data["p3"]))
	data["M0"] = M0
	data["M1"] = np.fmax(M1,M2) # pick higher mass possible pair
	data["M2"] = np.fmin(M1,M2) # pick lowest mass possible pair
	# ----------------------------------------------------------------------------------------------------------------

	# Define cuts
	selection = data["M1"] > 1.1	
	selection *= data["M2"] > 1.1	
	selection *= (data["M1"] < 9.) | (data["M1"] > 11.)
	selection *= (data["M2"] < 9.) | (data["M2"] > 11.)
	selection *= (data["M1"] > 3.9) | (data["M1"] < 2.9)
	selection *= (data["M2"] > 3.9) | (data["M2"] < 2.9)
	selection *= data[b'pTL1'] > 12	
	selection *= data[b'pTL2'] > 10
	selection *= data[b'pTL3'] > 5	
	selection *= (data[b'IsoL1'] < 0.1)  & (data[b'IsoL2'] < 0.1)  & (data[b'IsoL3'] < 0.1)
	selection *= (data[b'medIdL1'] == 1) & (data[b'medIdL2'] == 1) & (data[b'medIdL3'] == 1)

	xlow = m - round(m*.5)
	xhigh = m + round(m*.5)
	xsplit = round(xhigh-xlow)*10

	if m<30:
		binsx=np.linspace(0,70,140)
		binsy=np.linspace(xlow,xhigh,xsplit)
	elif m>30:
		binsy=np.linspace(0,70,140)
		binsx=np.linspace(xlow,xhigh,xsplit)
	else:
		binsx=np.linspace(0,70,140)
		binsy=np.linspace(0,70,140)

	plt.hist2d(data["M1"][selection],data["M2"][selection],bins=[binsx,binsy],cmap=plt.cm.nipy_spectral)
	plt.xlabel("M1 (GeV)")
	plt.ylabel("M2 (GeV)")
	plt.title("M1 vs. M2 for Zp M%i"%(m))
	plt.colorbar()
	#plt.savefig("output/2dPlots/M1vsM2_ZpM%i.png"%(m))
	plt.clf()

	plt.hist2d(data["dRM1"][selection],data["dRM2"][selection],bins=40,cmap=plt.cm.nipy_spectral)
	plt.xlabel("dR Between M1 Muons")
	plt.ylabel("dR Between M2 Muons")
	plt.title("dRM1 vs. dRM2 for Zp M%i"%(m))
	plt.colorbar()
	#plt.savefig("output/2dPlots/dR_ZpM%i.png"%(m))
	plt.clf()

	y,binEdges = np.histogram(data[b"m3l"][selection],bins=83,range=(0,83))
	error = np.sqrt(y)*weight
	weight_arr = np.ones(len(data[b"m3l"][selection]))*weight
	y,binEdges = np.histogram(data[b"m3l"][selection],bins=83,range=(0,83),weights=weight_arr)
	bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
	plt.errorbar(bincenters,y,yerr=error,drawstyle='steps-mid',label='ZpM%i: %.2f'%(m,np.sum(y)))
	plt.xlabel("3 Muon Invariant Mass")
	plt.ylabel("Number of Events")
	plt.title("3 Muon Invariant Mass for ZpM%i"%(m))
	plt.legend(loc='best')
	plt.show()
