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

#[Title,save name,variable plotted,nBins,low,high,unit,plot data]
["3 Mu Invariant Mass","m3l","m3l",83,0,83,"GeV",True],
["Lower Mass diMu Pair","mass2","M2",160,0,80,"GeV",False],

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
print(x)


# Make Plots
print("Generating Plots")
for p in tqdm(plots):
	plot(data,p,samples,False,out_dir)
