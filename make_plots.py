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

samples = background_samples + [signal_samples[0]] + data_samples#[signal_samples[0]]
files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)

lumi = 41.4*1000

out_dir = "Output/testing"
if not os.path.exists(out_dir): os.makedirs(out_dir)
if not os.path.exists("%s/pickle"%(out_dir)): os.makedirs("%s/pickle"%(out_dir))

plots = [

# 1D Plots
#[Title,save name,variable plotted,nBins,low,high,unit,plot data]
["3 Mu Invariant Mass","m3l","m3l",83,0,83,"GeV",True],
["3 Mu + MET Transverse Mass","mt","mt",200,0,200,"GeV",True],
["Lower Mass diMu Pair","mass2","M2",160,0,80,"GeV",False],
["Higher Mass diMu Pair","mass1","M1",160,0,80,"GeV",False],
["Leading pT","pTL1","pTL1",100,0,100,"GeV",True],
["Subleading pT","pTL2","pTL2",100,0,100,"GeV",True],
["Trailing pT","pTL3","pTL3",100,0,100,"GeV",True],
["Leading eta","etaL1","etaL1",60,-3.,3.,"eta",True],
["Subleading eta","etaL2","etaL2",60,-3.,3.,"eta",True],
["Trailing eta","etaL3","etaL3",60,-3.,3.,"eta",True],
["Leading phi","phiL1","phiL1",40,-4.,4.,"phi",True],
["Subleading phi","phiL2","phiL2",40,-4.,4.,"phi",True],
["Trailing phi","phiL3","phiL3",40,-4.,4.,"phi",True],
["Leading Isolation","IsoL1","IsoL1",100,0.,0.2,"pfRelIso03_all",True],
["Subleading Isolation","IsoL2","IsoL2",100,0.,0.2,"pfRelIso03_all",True],
["Trailing Isolation","IsoL3","IsoL3",100,0.,0.2,"pfRelIso03_all",True],
["Leading 3D Impact Parameter","ip3dL1","ip3dL1",100,0.,0.2,"IP3D",True],
["Subleading 3D Impact Parameter","ip3dL2","ip3dL2",100,0.,0.2,"IP3D",True],
["Trailing 3D Impact Parameter","ip3dL3","ip3dL3",100,0.,0.2,"IP3D",True],
["Leading Significance of 3D Impact Parameter","sip3dL1","sip3dL1",100,0.,10.,"SIP3D",True],
["Subleading Significance of 3D Impact Parameter","sip3dL2","sip3dL2",100,0.,10.,"SIP3D",True],
["Trailing Significance of 3D Impact Parameter","sip3dL3","sip3dL3",100,0.,10.,"SIP3D",True],
["Transverse Missing Energy","met","met",50,0,250,"GeV",True],
["Transver Missing Energy Phi","met_phi","met_phi",40,-4,4,"phi",True],
["dR Between Leading and Subleading","dR12","dR12",100,0,6,"dR",True],
["dR Between Leading and Trailing","dR13","dR13",100,0,6,"dR",True],
["dR Between Subleading and Trailing","dR23","dR23",100,0,6,"dR",True],

# 2D Plots
#To be incorporated

]

xs, sumW = combXS(xs_sig,sumW_sig,xs_bkg,sumW_bkg)
effs = {}
for i in range(len(samples)):
	if "data" not in samples[i]:
		weight = xs[samples[i]]/sumW[samples[i]]*lumi
	else:
		weight = xs[samples[i]]/sumW[samples[i]]
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
	print("Processing %s with %i events"%(samples[i],len(data["nMuons"])))


	# Select other variables
	data = select(data)

	# Perform Cuts
	data["selection"],effs[samples[i]] = skim(data)

	# Save resulting data
	with open("%s/pickle/%s.p"%(out_dir,samples[i]),'wb') as handle:
		pickle.dump(data, handle)

print("Saving all data in pickle files")
data = {}
for i in range(len(samples)):
	with open("%s/pickle/%s.p"%(out_dir,samples[i]),'rb') as handle:
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
table = open("%s/Efficiency_Table.txt"%(out_dir),"w")
table.write(x.get_string())
table.close()
print(x)


# Make Plots
print("Generating Plots")
for p in tqdm(plots):
	plot(data,p,samples,False,out_dir)
