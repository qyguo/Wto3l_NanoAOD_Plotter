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
#from Datasets.Signal.Wto3l import *
#from Datasets.Run2017.Data import *
#from Datasets.Run2017.Background import *
from Datasets.Signal.Wto3l_UL18 import *
from Datasets.Run2018.Data import *
from Datasets.Run2018.Background import *
from Skimmer.AnalysisSkimmer import *
from Skimmer.ZSelector import *
from Plotter.Plot import *
from Weighter.Fake_weight import *

import time

#Define parameters from plotting

# Signal Region
#samples = background_samples + signal_samples + ["data"]
#samples = ["ZZTo4L","WZTo3LNu","DYJetsToLL_M0To1","fake"] + signal_samples + ["data"]

# Control Region
samples = background_samples + ["data"]
#samples = ["ZZTo4L","WZTo3LNu","DYJetsToLL_M0To1","fake"] + ["data"]
#samples = ["ZZTo4L","WZTo3LNu"] + ["data"]

#samples = ["ZZTo4L","DYJetsToLL_M0To1"]

files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)

#lumi = 41.4*1000
lumi = 59.8*1000
error_on_MC = False
skip_skim=False

out_dir = "3mu_MC_D_mva_noIdPre_2P1F_UL18_DY_M1To10_old_UL17Sub2"
#if not os.path.exists("/orange/avery/nikmenendez/Output/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/Output/%s/"%(out_dir))
#if not os.path.exists("/orange/avery/nikmenendez/Output/pickle/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/Output/pickle/%s/"%(out_dir))
if not os.path.exists("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/"%(out_dir)): os.makedirs("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/"%(out_dir))
if not os.path.exists("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/pickle/%s/"%(out_dir)): os.makedirs("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/pickle/%s/"%(out_dir))

plots = [

# 1D Plots
#[Title,save name,variable plotted,nBins,low,high,unit,plot data]
#["3 Mu Invariant Mass","m3l","m3l",83,0,83,"GeV",True],
#["Low diMuon Mass","photon_mass","photon_mass",50,0,5,"GeV",False],
#["Lower Mass diMu Pair" ,"mass2","M2",76,3.5,80.5,"GeV",False],
#["Higher Mass diMu Pair","mass1","M1",76,3.5,80.5,"GeV",False],

["3 Mu pT","m3l_pt","m3l_pt",150,0,150,"GeV",True],
["3 Mu + MET Transverse Mass","mt","mt",100,0,350,"GeV",True],
["dR Between Same Sign diMu","dRM0","dRM0",100,0,6,"dR",True],

#For Signal Region
["3 Mu Invariant Mass","m3l","m3l",83,0,83,"GeV",True],
#["Lower Mass diMu Pair","mass2","M2",160,0,80,"GeV",False],
#["Higher Mass diMu Pair","mass1","M1",160,0,80,"GeV",False],
["Lower Mass diMu Pair" ,"mass2","M2",76,3.5,80.5,"GeV",False],
["Higher Mass diMu Pair","mass1","M1",76,3.5,80.5,"GeV",False],
["Same Sign diMu Pair","sameMass","M0",80,0,80,"GeV",True],
["dR Between Lower Mass diMu","dRM2","dRM2",100,0,6,"dR",False],
["dR Between Higher Mass diMu","dRM1","dRM1",100,0,6,"dR",False],

#For Control Region
#["3 Mu Invariant Mass","m3l","m3l",100,0,200,"GeV",True],
#["Lower Mass diMu Pair","mass2","M2",100,0,200,"GeV",True],
#["Higher Mass diMu Pair","mass1","M1",100,0,200,"GeV",True],
#["Same Sign diMu Pair","sameMass","M0",100,0,200,"GeV",True],
#["dR Between Lower Mass diMu","dRM2","dRM2",100,0,6,"dR",True],
#["dR Between Higher Mass diMu","dRM1","dRM1",100,0,6,"dR",True],

["Leading pT","pTL1","pTL1",100,0,100,"GeV",True],
["Subleading pT","pTL2","pTL2",80,0,80,"GeV",True],
["Trailing pT","pTL3","pTL3",50,0,50,"GeV",True],
["Leading eta","etaL1","etaL1",60,-3.,3.,"eta",True],
["Subleading eta","etaL2","etaL2",60,-3.,3.,"eta",True],
["Trailing eta","etaL3","etaL3",60,-3.,3.,"eta",True],
["Leading phi","phiL1","phiL1",40,-4.,4.,"phi",True],
["Subleading phi","phiL2","phiL2",40,-4.,4.,"phi",True],
["Trailing phi","phiL3","phiL3",40,-4.,4.,"phi",True],
["Leading Isolation","IsoL1","IsoL1",60,0.,0.6,"pfRelIso03_all",True],
["Subleading Isolation","IsoL2","IsoL2",60,0.,0.6,"pfRelIso03_all",True],
["Trailing Isolation","IsoL3","IsoL3",60,0.,0.6,"pfRelIso03_all",True],
["Leading 3D Impact Parameter","ip3dL1","ip3dL1",25,0.,0.02,"IP3D",True],
["Subleading 3D Impact Parameter","ip3dL2","ip3dL2",25,0.,0.02,"IP3D",True],
["Trailing 3D Impact Parameter","ip3dL3","ip3dL3",25,0.,0.02,"IP3D",True],
["Leading Significance of 3D Impact Parameter","sip3dL1","sip3dL1",40,0.,4.,"SIP3D",True],
["Subleading Significance of 3D Impact Parameter","sip3dL2","sip3dL2",40,0.,4.,"SIP3D",True],
["Trailing Significance of 3D Impact Parameter","sip3dL3","sip3dL3",40,0.,4.,"SIP3D",True],
["Leading dxy","dxyL1","dxyL1",50,-.02,.02,"cm",True],
["Subleading dxy","dxyL2","dxyL2",50,-.02,.02,"cm",True],
["Trailing dxy","dxyL3","dxyL3",50,-.02,.02,"cm",True],
["Leading dz","dzL1","dzL1",50,-.02,.02,"cm",True],
["Subleading dz","dzL2","dzL2",50,-.02,.02,"cm",True],
["Trailing dz","dzL3","dzL3",50,-.02,.02,"cm",True],
#["Leading Medium ID","medIdL1","medIdL1",2,0,2,"True",True],
#["Subleading Medium ID","medIdL2","medIdL2",2,0,2,"True",True],
#["Trailing Medium ID","medIdL3","medIdL3",2,0,2,"True",True],
["Leading mva ID","mvaIdL1","mvaIdL1",6,0,6,"ID",True],
["Subleading mva ID","mvaIdL2","mvaIdL2",6,0,6,"ID",True],
["Trailing mva ID","mvaIdL3","mvaIdL3",6,0,6,"ID",True],

["Leading Origin","sourceL1","sourceL1",10,-1,9,"Muon Origin",False],
["Subleading Origin","sourceL2","sourceL2",10,-1,9,"Muon Origin",False],
["Trailing Origin","sourceL3","sourceL3",10,-1,9,"Muon Origin",False],
#["Leading Gen-Matched delta pT","gen_dPtL1","gen_dPtL1",100,0,100,"GeV",False,'log'],
#["Subleading Gen-Matched delta pT","gen_dPtL2","gen_dPtL2",100,0,100,"GeV",False,'log'],
#["Trailing Gen-Matched delta pT","gen_dPtL3","gen_dPtL3",100,0,100,"GeV",False,'log'],
#["Leading Gen-Matched dR","gen_dRL1","gen_dRL1",100,0,6,"dR",False,'log'],
#["Subleading Gen-Matched dR","gen_dRL2","gen_dRL2",100,0,6,"dR",False,'log'],
#["Trailing Gen-Matched dR","gen_dRL3","gen_dRL3",100,0,6,"dR",False,'log'],


["Worst Isolation","worstIso","worstIso",60,0,.6,"pfRelIso03_all",True],
["Worst dxy","worstdxy","worstdxy",20,0,.02,"cm",True],
["Worst dz","worstdz","worstdz",20,0,0.02,"cm",True],
["Worst 3D Impact Parameter","worstip3d","worstip3d",25,0.,0.02,"IP3D",True],
["Worst Significance of 3D Impact Parameter","worstsip3d","worstsip3d",100,0.,4.,"SIP3D",True],
["Worst Medium ID","worstmedId","worstmedId",2,0,2,"True",True],
["Worst mva ID","worstmvaId","worstmvaId",6,0,6,"ID",True],
["Worst Tight ID","worsttightId","worsttightId",2,0,2,"True",True],
["Worst Soft ID","worstsoftId","worstsoftId",2,0,2,"True",True],

["Transverse Missing Energy","met","met",50,0,250,"GeV",True],
["Transver Missing Energy Phi","met_phi","met_phi",40,-4,4,"phi",True],
["dR Between Leading and Subleading","dR12","dR12",100,0,6,"dR",True],
["dR Between Leading and Trailing","dR13","dR13",100,0,6,"dR",True],
["dR Between Subleading and Trailing","dR23","dR23",100,0,6,"dR",True],
["dPhi Between Leading and Subleading","dPhi12","dPhi12",40,0,8,"dPhi",True],
["dPhi Between Leading and Trailing","dPhi13","dPhi13",40,0,8,"dPhi",True],
["dPhi Between Subleading and Trailing","dPhi23","dPhi23",40,0,8,"dPhi",True],

["Number of b Jets","nbJets","nbJets",6,0,6,"n",True],
["Number of Jets","nJets","nJets",12,0,12,"n",True],
["Number of Muons","nMuons","nMuons",6,0,6,"n",True],
["Number of Good Muons","nGoodMuons","nGoodMuons",6,0,6,"n",True],

#["Neural Network Discriminator","discriminator","discriminator",100,0,1,"",True],
#["Random Forest Class","forestguess","forestguess",2,0,2,"",True],

# 2D Plots
#To be incorporated

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
	data = events.arrays(vars_in, library="np")
	#for key in temp: data[key.decode("utf-8")] = temp[key]
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
	#data["selection"],effs[samples[i]],data["fail"],data["fail2"] = skim_opt(data,samples[i])
	#if sType == "MC":
	#	data["selection"] = ((data["sourceL1"]!=2) & (data["sourceL2"]!=2) & (data["sourceL3"]!=2))*data["selection"]

	# Get fake weight if necessary
	print("Weighting... ",end='',flush=True)
	data["fakeWeight"] = Fake_weight(data,samples[i])
	print("Avg fake weight: %.2f "%((np.average(data["fakeWeight"][data["selection"]]))),end='',flush=True)
	data["eventWeight"] = data["genWeight"]*data["pileupWeight"]*data["weight"]#*data["fakeWeight"]

	# Save resulting data
	print("Saving Results... ",end='',flush=True)
	#with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
	with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
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
	#with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
	with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
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
	#table = open("/orange/avery/nikmenendez/Output/%s/Efficiency_Table.txt"%(out_dir),"w")
	table = open("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/Efficiency_Table.txt"%(out_dir),"w")
	table.write(x.get_string())
	table.close()
	print(x)


# Make Plots
print("Generating Plots")
for p in tqdm(plots):
	if "data" in samples:
		plot(data,p,samples,error_on_MC,out_dir,True,False)
	else:
		plot(data,p,samples,error_on_MC,out_dir,False,False)
		

print('\a')
print("Uploading plots to web")
#print("scp -r /orange/avery/nikmenendez/Output/%s/ nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/UL/"%(out_dir))
#print("scp -r /publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/ qguo@lxplus.cern.ch:/eos/user/q/qguo/www/Wto3l/SR_Selection/ZpX/UL/Output/"%(out_dir))
print("scp -r qyguo@lxslc7.ihep.ac.cn://publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/ /eos/user/q/qguo/www/Wto3l/SR_Selection/ZpX/UL/Output/"%(out_dir))
print("cp /eos/user/q/qguo/www/Wto3l/SR_Selection/ZpX/UL/Output/index.php  /eos/user/q/qguo/www/Wto3l/SR_Selection/ZpX/UL/Output/%s/"%(out_dir))
#import subprocess
#subprocess.run(["scp","-r","/orange/avery/nikmenendez/Output/%s/"%(out_dir),"nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/UL/"])
