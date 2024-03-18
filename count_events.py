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

#Define parameters from plotting
samples = data_samples[:-1]
files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)

masses = [1,2,3,4,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80]

#lumi = 41.4*1000
lumi = 59.8*1000
error_on_MC = False

out_dir = "3mu_onlyVeto"
#if not os.path.exists("/home/nikmenendez/Output/%s/"%(out_dir)): os.makedirs("/home/nikmenendez/Output/%s/"%(out_dir))
#if not os.path.exists("/home/nikmenendez/Output/pickle/%s/"%(out_dir)): os.makedirs("/home/nikmenendez/Output/pickle/%s/"%(out_dir))
if not os.path.exists("/home/nikmenendez/Output/%s/"%(out_dir)): os.makedirs("/home/nikmenendez/Output/%s/"%(out_dir))
if not os.path.exists("/home/nikmenendez/Output/pickle/%s/"%(out_dir)): os.makedirs("/home/nikmenendez/Output/pickle/%s/"%(out_dir))

plots = [

# 1D Plots
#[Title,save name,variable plotted,nBins,low,high,unit,plot data]
["3 Mu Invariant Mass","m3l","m3l",83,0,83,"GeV",True],
["3 Mu + MET Transverse Mass","mt","mt",100,0,250,"GeV",True],
["Lower Mass diMu Pair","mass2","M2",160,0,80,"GeV",False],
["Higher Mass diMu Pair","mass1","M1",160,0,80,"GeV",False],
["Same Sign diMu Pair","sameMass","M0",160,0,80,"GeV",True],

["Leading pT","pTL1","pTL1",100,0,100,"GeV",True],
["Subleading pT","pTL2","pTL2",80,0,80,"GeV",True],
["Trailing pT","pTL3","pTL3",50,0,50,"GeV",True],
["Leading eta","etaL1","etaL1",60,-3.,3.,"eta",True],
["Subleading eta","etaL2","etaL2",60,-3.,3.,"eta",True],
["Trailing eta","etaL3","etaL3",60,-3.,3.,"eta",True],
["Leading phi","phiL1","phiL1",40,-4.,4.,"phi",True],
["Subleading phi","phiL2","phiL2",40,-4.,4.,"phi",True],
["Trailing phi","phiL3","phiL3",40,-4.,4.,"phi",True],
["Leading Isolation","IsoL1","IsoL1",50,0.,0.2,"pfRelIso03_all",True],
["Subleading Isolation","IsoL2","IsoL2",50,0.,0.2,"pfRelIso03_all",True],
["Trailing Isolation","IsoL3","IsoL3",50,0.,0.2,"pfRelIso03_all",True],
["Leading 3D Impact Parameter","ip3dL1","ip3dL1",25,0.,0.05,"IP3D",True],
["Subleading 3D Impact Parameter","ip3dL2","ip3dL2",25,0.,0.05,"IP3D",True],
["Trailing 3D Impact Parameter","ip3dL3","ip3dL3",25,0.,0.05,"IP3D",True],
["Leading Significance of 3D Impact Parameter","sip3dL1","sip3dL1",100,0.,10.,"SIP3D",True],
["Subleading Significance of 3D Impact Parameter","sip3dL2","sip3dL2",100,0.,10.,"SIP3D",True],
["Trailing Significance of 3D Impact Parameter","sip3dL3","sip3dL3",100,0.,10.,"SIP3D",True],
["Leading dxy","dxyL1","dxyL1",100,-1.,1.,"cm",True],
["Subleading dxy","dxyL2","dxyL2",100,-1.,1.,"cm",True],
["Trailing dxy","dxyL3","dxyL3",100,-1.,1.,"cm",True],
["Leading dz","dzL1","dzL1",100,-1.,1.,"cm",True],
["Subleading dz","dzL2","dzL2",100,-1.,1.,"cm",True],
["Trailing dz","dzL3","dzL3",100,-1.,1.,"cm",True],
["Leading medId","medIdL1","medIdL1",2,0,2,"cm",True],
["Subleading medId","medIdL2","medIdL2",2,0,2,"cm",True],
["Trailing medId","medIdL3","medIdL3",2,0,2,"cm",True],
["Leading mvaId","mvaIdL1","mvaIdL1",6,0,6,"cm",True],
["Subleading mvaId","mvaIdL2","mvaIdL2",6,0,6,"cm",True],
["Trailing mvaId","mvaIdL3","mvaIdL3",6,0,6,"cm",True],

["Transverse Missing Energy","met","met",50,0,250,"GeV",True],
["Transver Missing Energy Phi","met_phi","met_phi",40,-4,4,"phi",True],
["dR Between Leading and Subleading","dR12","dR12",100,0,6,"dR",True],
["dR Between Leading and Trailing","dR13","dR13",100,0,6,"dR",True],
["dR Between Subleading and Trailing","dR23","dR23",100,0,6,"dR",True],
["Number of b Jets","nbJets","nbJets",2,0,2,"n",True],
["Number of Jets","nJets","nJets",12,0,12,"n",True],

# 2D Plots
#To be incorporated

]

xs, sumW = combXS(xs_sig,sumW_sig,xs_bkg,sumW_bkg)
effs = {}
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
	print("Processing %s with %i events"%(samples[i],len(data["nMuons"])))


	# Select other variables
	data = select(data)

	# Perform Cuts
	data["selection"],effs[samples[i]],data["fail"],data["fail2"] = skim(data,samples[i])

	# Get fake weight if necessary
	data["fake_weight"] = Fake_weight(data,samples[i])
	if "fake" in samples[i]: 
		#data["genWeight"] = data["genWeight"]*data["fake_weight"]*data["fail2"] #For 2P1F Validation
		data["genWeight"] = data["genWeight"]*data["fake_weight"]*data["fail"] + data["genWeight"]*data["fake_weight"]*data["fail2"] #For 3P0F Validation

	# Save resulting data
	with open("/home/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
		pickle.dump(data, handle)

data = {}
for i in range(len(samples)):
	with open("/home/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
		data[samples[i]] = pickle.load(handle)

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
table = open("/home/nikmenendez/Output/%s/Efficiency_Table.txt"%(out_dir),"w")
table.write(x.get_string())
table.close()
print(x)


# Make Plots
print("Generating Plots")
for p in tqdm(plots):
	plot(data,p,samples,error_on_MC,out_dir)

print('\a')
print("Uploading plots to web")
import subprocess
subprocess.run(["scp","-r","/home/nikmenendez/Output/%s/"%(out_dir),"nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/New_Plotter/"])
