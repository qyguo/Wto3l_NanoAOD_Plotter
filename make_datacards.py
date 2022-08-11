from __future__ import division
import numpy as np
import uproot
import sys
import matplotlib.pyplot as plt
import os
import pickle
from tqdm import tqdm
from prettytable import PrettyTable

from Utils.combXS import *
from Datasets.Signal.Wto3l import *
from Datasets.Run2017.Data import *
from Datasets.Run2017.Background import *
from Skimmer.AnalysisSkimmer import *
from Skimmer.ZSelector import *
from Plotter.Plot import *
from Plotter.Card import *
from Plotter.Fit  import *
from Weighter.Fake_weight import *
from create_datacards import *

import time

#Define parameters from plotting

# Signal Region
samples = ["ZZTo4L","WZTo3LNu","DYJetsToLL_M0To1","fake"] + signal_samples + ["data"]

files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)

lumi = 41.4*1000
error_on_MC = False
skip_skim=True
if skip_skim: print("Skipping skim. Using previous skim results")

out_dir = "datacards_RBE_mva_looseIdPre_NewSig"
if not os.path.exists("/orange/avery/nikmenendez/Output/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/Output/%s/"%(out_dir))
if not os.path.exists("/orange/avery/nikmenendez/Output/pickle/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/Output/pickle/%s/"%(out_dir))

params = [
["Lower Mass diMu Pair" ,"mass2","M2",76,3.5,80.5,"GeV",True],
["Higher Mass diMu Pair","mass1","M1",76,3.5,80.5,"GeV",True],
]


plots = [

["Lower Mass diMu Pair" ,"mass2","M2",16,2.5,82.5,"GeV",False],
["Higher Mass diMu Pair","mass1","M1",16,2.5,82.5,"GeV",False],

["3 Mu pT","m3l_pt","m3l_pt",75,0,150,"GeV",True],
["3 Mu + MET Transverse Mass","mt","mt",50,0,350,"GeV",True],
["dR Between Same Sign diMu","dRM0","dRM0",50,0,6,"dR",True],

#For Signal Region
["3 Mu Invariant Mass","m3l","m3l",42,0,84,"GeV",True],
#["4 Mu Invariant Mass","m4l","m4l",50,0,200,"GeV",True],
["Same Sign diMu Pair","sameMass","M0",40,0,80,"GeV",True],
["dR Between Lower Mass diMu","dRM2","dRM2",50,0,6,"dR",False],
["dR Between Higher Mass diMu","dRM1","dRM1",50,0,6,"dR",False],

["Leading pT","pTL1","pTL1",50,0,100,"GeV",True],
["Subleading pT","pTL2","pTL2",40,0,80,"GeV",True],
["Trailing pT","pTL3","pTL3",25,0,50,"GeV",True],
["Leading eta","etaL1","etaL1",30,-3.,3.,"eta",True],
["Subleading eta","etaL2","etaL2",30,-3.,3.,"eta",True],
["Trailing eta","etaL3","etaL3",30,-3.,3.,"eta",True],
["Leading phi","phiL1","phiL1",20,-4.,4.,"phi",True],
["Subleading phi","phiL2","phiL2",20,-4.,4.,"phi",True],
["Trailing phi","phiL3","phiL3",20,-4.,4.,"phi",True],
["Leading Isolation","IsoL1","IsoL1",30,0.,0.6,"pfRelIso03_all",True],
["Subleading Isolation","IsoL2","IsoL2",30,0.,0.6,"pfRelIso03_all",True],
["Trailing Isolation","IsoL3","IsoL3",30,0.,0.6,"pfRelIso03_all",True],
["Leading 3D Impact Parameter","ip3dL1","ip3dL1",12,0.,0.02,"IP3D",True],
["Subleading 3D Impact Parameter","ip3dL2","ip3dL2",12,0.,0.02,"IP3D",True],
["Trailing 3D Impact Parameter","ip3dL3","ip3dL3",12,0.,0.02,"IP3D",True],
["Leading Significance of 3D Impact Parameter","sip3dL1","sip3dL1",20,0.,4.,"SIP3D",True],
["Subleading Significance of 3D Impact Parameter","sip3dL2","sip3dL2",20,0.,4.,"SIP3D",True],
["Trailing Significance of 3D Impact Parameter","sip3dL3","sip3dL3",20,0.,4.,"SIP3D",True],
["Leading dxy","dxyL1","dxyL1",25,-.05,.05,"cm",True],
["Subleading dxy","dxyL2","dxyL2",25,-.05,.05,"cm",True],
["Trailing dxy","dxyL3","dxyL3",25,-.05,.05,"cm",True],
["Leading dz","dzL1","dzL1",25,-.1,.1,"cm",True],
["Subleading dz","dzL2","dzL2",25,-.1,.1,"cm",True],
["Trailing dz","dzL3","dzL3",25,-.1,.1,"cm",True],
["Leading mva ID","mvaIdL1","mvaIdL1",6,0,6,"ID",True],
["Subleading mva ID","mvaIdL2","mvaIdL2",6,0,6,"ID",True],
["Trailing mva ID","mvaIdL3","mvaIdL3",6,0,6,"ID",True],

["Worst Isolation","worstIso","worstIso",30,0,.6,"pfRelIso03_all",True],
["Worst dxy","worstdxy","worstdxy",10,0,.05,"cm",True],
["Worst dz","worstdz","worstdz",10,0,0.1,"cm",True],
["Worst 3D Impact Parameter","worstip3d","worstip3d",12,0.,0.02,"IP3D",True],
["Worst Significance of 3D Impact Parameter","worstsip3d","worstsip3d",20,0.,4.,"SIP3D",True],
["Worst Medium ID","worstmedId","worstmedId",2,0,2,"True",True],
["Worst mva ID","worstmvaId","worstmvaId",6,0,6,"ID",True],
["Worst Tight ID","worsttightId","worsttightId",2,0,2,"True",True],
["Worst Soft ID","worstsoftId","worstsoftId",2,0,2,"True",True],

["Transverse Missing Energy","met","met",25,0,250,"GeV",True],
["Transver Missing Energy Phi","met_phi","met_phi",20,-4,4,"phi",True],
["dR Between Leading and Subleading","dR12","dR12",50,0,6,"dR",True],
["dR Between Leading and Trailing","dR13","dR13",50,0,6,"dR",True],
["dR Between Subleading and Trailing","dR23","dR23",50,0,6,"dR",True],
["dPhi Between Leading and Subleading","dPhi12","dPhi12",20,0,8,"dPhi",True],
["dPhi Between Leading and Trailing","dPhi13","dPhi13",20,0,8,"dPhi",True],
["dPhi Between Subleading and Trailing","dPhi23","dPhi23",20,0,8,"dPhi",True],

#["Number of b Jets","nbJets","nbJets",6,0,6,"n",True],
#["Number of Jets","nJets","nJets",12,0,12,"n",True],
#["Number of Muons","nMuons","nMuons",6,0,6,"n",True],
["Number of Good Muons","nGoodMuons","nGoodMuons",6,0,6,"n",True],
]

xs, sumW = combXS(xs_sig,sumW_sig,xs_bkg,sumW_bkg)
effs = {}
for i in range(len(samples)):
	if skip_skim: break
	tic = time.perf_counter()
	print("Processing %s... "%(samples[i]),end='',flush=True)
	if ("data" in samples[i]) or ("fake" in samples[i]):
		weight = xs[samples[i]]/sumW[samples[i]]
	else:
		weight = xs[samples[i]]/sumW[samples[i]]*lumi
	if "Wto3l" in samples[i]: sType = "sig"
	elif "data" in samples[i]: sType = "data"
	else: sType = "MC"	

	print("Reading in ",end='',flush=True)
	file = uproot.open(files[samples[i]])
	events = file["passedEvents"]

	if ("data" in samples[i]) or ("fake" in samples[i]): vars_in = data_vars
	elif sType=="sig": vars_in = signal_vars
	else: vars_in = background_vars

	temp = events.arrays(vars_in)

	data = {}
	for key in temp: data[key.decode("utf-8")] = temp[key]
	del temp
	data["weight"] = weight
	data["sType"] = sType
	if not (("data" in samples[i]) or ("fake" in samples[i])):
		data["pileupWeight"] = data["pileupWeight"]/32
	#print("Processing %s with %i events"%(samples[i],len(data["nMuons"])))
	print("%i events... "%(len(data["nMuons"])),end='',flush=True)


	# Select other variables
	print("Selecting Vars... ",end='',flush=True)
	data = select(data)
	#if "ZZ" in samples[i]:
	#	data["photon_mass"] = data["M2"]

	# Perform Cuts
	print("Skimming... ",end='',flush=True)
	data["selection"],effs[samples[i]],data["fail"],data["fail2"] = skim(data,samples[i])
	#if sType == "MC":
	#	data["selection"] = ((data["sourceL1"]!=2) & (data["sourceL2"]!=2) & (data["sourceL3"]!=2))*data["selection"]

	# Get fake weight if necessary
	print("Weighting... ",end='',flush=True)
	data["fakeWeight"] = Fake_weight(data,samples[i])
	data["eventWeight"] = data["genWeight"]*data["pileupWeight"]*data["fakeWeight"]*data["weight"]

	data["Acceptance"] = data["inAcceptance"][-1]/sumW[samples[i]]
	data["SelectionEfficiency"] = np.count_nonzero(data["selection"])/data["inAcceptance"][-1]
	#print(data["Acceptance"])
	#print(data["SelectionEfficiency"])
	#print("\nAcceptance = %.4f, Selection Efficiency = %f"%(data["Acceptance"],data["SelectionEfficiency"])) 

	# Save resulting data
	print("Saving Results... ",end='',flush=True)
	with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
		pickle.dump(data, handle)
	del data
	print("Done! ",end='',flush=True)
	toc = time.perf_counter()
	tot_time = toc-tic
	if tot_time<60:
		print("Total time was %.2f seconds"%(tot_time))
	else:
		print("Total time was %.2f minutes"%(tot_time/60))

print("Combining samples")
data = {}
for i in range(len(samples)):
	with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
		data[samples[i]] = pickle.load(handle)

if not skip_skim:
	print("Efficiencies of each cut:")
	cuts = ["Sample"]
	for key in effs[samples[0]]:
		cuts.append(key)
	x = PrettyTable(cuts)
	for key in effs:
		row = [key]
		for key2 in effs[key]:
			row.append("%.2f%%"%(effs[key][key2]))
		x.add_row(row)
	table = open("/orange/avery/nikmenendez/Output/%s/Efficiency_Table.txt"%(out_dir),"w")
	table.write(x.get_string())
	table.close()
	print(x)


# Make Plots
print("Counting Events")
for p in tqdm(params):
	if "data" in samples:
		card(data,p,samples,error_on_MC,out_dir,True,True)
	else:
		card(data,p,samples,error_on_MC,out_dir,False,True)

print("Generating Plots")
for p in tqdm(plots):
	if "data" in samples:
		plot(data,p,samples,error_on_MC,out_dir,True,False)
	else:
		plot(data,p,samples,error_on_MC,out_dir,False,False)

#print("Counting signal yields")
#SigFit(data,samples)

AccEff = {}
for s in samples:
	if "Wto3l" in s:
		AccEff[s] = [data[s]["Acceptance"],data[s]["SelectionEfficiency"]]
print("Making datacards")
create_datacards("/orange/avery/nikmenendez/Output/%s/"%(out_dir),xs_sig,xs_err,AccEff)

print("Plotting Sig Yields")
SigFit(data,samples,out_dir)

print('\a')
print("Uploading plots to web")
print("scp -r /orange/avery/nikmenendez/Output/%s/ nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/UL/"%(out_dir))
import subprocess
subprocess.run(["scp","-r","/orange/avery/nikmenendez/Output/%s/"%(out_dir),"nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/UL/"])
