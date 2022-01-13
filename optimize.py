from __future__ import division
import numpy as np
import uproot
import sys
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from prettytable import PrettyTable

from Utils.combXS import *
from Datasets.Signal.Wto3l import *
from Datasets.Run2017.Data import *
from Datasets.Run2017.Background import *
from Skimmer.AnalysisSkimmer import *
from Skimmer.ZSelector import *
from Plotter.Plot import *
from Plotter.ROC import *
from Weighter.Fake_weight import *

#Define parameters from plotting
samples = background_samples + signal_samples
#samples = ["WZTo3LNu","ZZTo4L","fake"] + [signal_samples[0]] + ["data"]
files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)

lumi = 41.4*1000
error_on_MC = False

out_dir = "Unweighted_Sig"
if not os.path.exists("/home/nikmenendez/Output/ROC/%s/"%(out_dir)): os.makedirs("/home/nikmenendez/Output/ROC/%s/"%(out_dir))

plots = [

# 1D Plots
#[Title,save name,variable plotted,nBins,low,high,unit,plot data]
#["3 Mu Invariant Mass","m3l","m3l",100,0,200,"GeV",True],
["3 Mu + MET Transverse Mass","mt<","mt",100,0,250,"GeV",True],
["3 Mu + MET Transverse Mass","mt>","mt",100,0,250,"GeV",False],
#["Lower Mass diMu Pair","mass2","M2",100,0,200,"GeV",True],
#["Higher Mass diMu Pair","mass1","M1",100,0,200,"GeV",True],
["Same Sign diMu Pair","sameMass<","M0",200,0,200,"GeV",True],
["Same Sign diMu Pair","sameMass>","M0",200,0,200,"GeV",False],
#["Leading pT","pTL1","pTL1",100,0,100,"GeV",True],
#["Subleading pT","pTL2","pTL2",80,0,80,"GeV",True],
#["Trailing pT","pTL3","pTL3",50,0,50,"GeV",True],
#["Leading eta","etaL1","etaL1",60,-3.,3.,"eta",True],
#["Subleading eta","etaL2","etaL2",60,-3.,3.,"eta",True],
#["Trailing eta","etaL3","etaL3",60,-3.,3.,"eta",True],
#["Leading phi","phiL1","phiL1",40,-4.,4.,"phi",True],
#["Subleading phi","phiL2","phiL2",40,-4.,4.,"phi",True],
#["Trailing phi","phiL3","phiL3",40,-4.,4.,"phi",True],
["Leading Isolation","IsoL1","IsoL1",50,0.,0.6,"pfRelIso03_all",True],
["Subleading Isolation","IsoL2","IsoL2",50,0.,0.6,"pfRelIso03_all",True],
["Trailing Isolation","IsoL3","IsoL3",50,0.,0.6,"pfRelIso03_all",True],
["Leading 3D Impact Parameter","ip3dL1","ip3dL1",25,0.,0.05,"IP3D",True],
["Subleading 3D Impact Parameter","ip3dL2","ip3dL2",25,0.,0.05,"IP3D",True],
["Trailing 3D Impact Parameter","ip3dL3","ip3dL3",25,0.,0.05,"IP3D",True],
["Leading Significance of 3D Impact Parameter","sip3dL1","sip3dL1",40,0.,4.,"SIP3D",True],
["Subleading Significance of 3D Impact Parameter","sip3dL2","sip3dL2",40,0.,4.,"SIP3D",True],
["Trailing Significance of 3D Impact Parameter","sip3dL3","sip3dL3",40,0.,4.,"SIP3D",True],
["Transverse Missing Energy","met<","met",50,0,250,"GeV",True],
["Transverse Missing Energy","met>","met",50,0,250,"GeV",False],
#["Transvere Missing Energy Phi","met_phi","met_phi",40,-4,4,"phi",True],
["dR Between Leading and Subleading","dR12<","dR12",100,0,6,"dR",True],
["dR Between Leading and Trailing","dR13<","dR13",100,0,6,"dR",True],
#["dR Between Subleading and Trailing","dR23<","dR23",100,0,6,"dR",True],
["dR Between Leading and Subleading","dR12>","dR12",100,0,6,"dR",False],
["dR Between Leading and Trailing","dR13>","dR13",100,0,6,"dR",False],
#["dR Between Subleading and Trailing","dR23>","dR23",100,0,6,"dR",False],
#["Number of b Jets","nbJets","nbJets",2,0,2,"n",True],

# 2D Plots
#To be incorporated

]

xs, sumW = combXS(xs_sig,sumW_sig,xs_bkg,sumW_bkg)
effs = {}
sig, bkg = {}, {}
for i in range(len(samples)):
	if ("data" in samples[i]) or ("fake" in samples[i]):
		weight = xs[samples[i]]/sumW[samples[i]]
	else:
		weight = xs[samples[i]]/sumW[samples[i]]*lumi
	if "Wto3l" in samples[i]: sType = "sig"
	elif "data" in samples[i]: sType = "data"
	else: sType = "MC"	

	file = uproot.open(files[samples[i]])
	events = file["passedEvents"]

	vars_in = signal_vars
	temp = events.arrays(vars_in)

	data = {}
	for key in temp: data[key.decode("utf-8")] = temp[key]
	del temp
	data["weight"] = weight
	data["sType"] = sType
	if not (("data" in samples[i]) or ("fake" in samples[i])):
		data["pileupWeight"] = data["pileupWeight"]/32
	print("Reading in %s with %i events"%(samples[i],len(data["nMuons"])))


	# Select other variables
	data = select(data)

	# Perform Cuts
	selection = skim_opt(data,samples[i])
	#data["weight_arr"] = data["weight"]*data["genWeight"]*data["pileupWeight"]
	if sType == "MC":
		data["weight_arr"] = data["weight"]*data["genWeight"]*data["pileupWeight"]
	else:
		data["weight_arr"] = np.ones(len(data["genWeight"]))

	for key in data:
		if key=="weight" or key=="sType": continue
		data[key] = data[key][selection]

	# Save resulting data
	if sType == "MC":
		if not bkg:
			bkg = data
		else:
			for key in data:
				bkg[key] = np.append(bkg[key],data[key])
	elif sType == "sig":
		if not sig:
			sig = data
		else:
			for key in data:
				sig[key] = np.append(sig[key],data[key])

tot_bkg = np.sum(bkg["weight_arr"])
tot_sig = np.sum(sig["weight_arr"])
og_ratio = tot_sig/np.sqrt(tot_bkg)
print("Total number of bkg events: %.2f"%(tot_bkg))
print("Total number of sig events: %.2f"%(tot_sig))
print("Original ratio = %.2f"%(og_ratio))

best_ratio, best_cut = {}, {}
for p in tqdm(plots):
	best_ratio[p[1]], best_cut[p[1]] = ROC(bkg,sig,p,out_dir)

for p in plots:
	improvement = best_ratio[p[1]]/og_ratio
	if improvement >= 1.01:
		if p[7]: print("Improvement of %.2fx with %s < %.2f"%(improvement,p[2],best_cut[p[1]]))
		else:    print("Improvement of %.2fx with %s > %.2f"%(improvement,p[2],best_cut[p[1]]))

print('\a')
print("Uploading plots to web")
import subprocess
subprocess.run(["scp","-r","/home/nikmenendez/Output/ROC/%s/"%(out_dir),"nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/ROC_Curves/"])
