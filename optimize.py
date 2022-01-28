from __future__ import division
import numpy as np
import uproot
import sys
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from prettytable import PrettyTable
import pickle
import copy

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
samples = background_samples + signal_samples + ["data"]
#samples = ["WZTo3LNu","ZZTo4L","fake"] + [signal_samples[0]] + ["data"]
files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)
sig_masses = [4,5,15,30,60]

lumi = 41.4*1000
error_on_MC = False

out_dir = "to_opt"
if not os.path.exists("/orange/avery/nikmenendez/Output/Optimize/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/Output/Optimize/%s/"%(out_dir))
if not os.path.exists("/orange/avery/nikmenendez/Output/pickle/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/Output/pickle/%s/"%(out_dir))

plots = [

# 1D Plots
#[Title,save name,variable plotted,nBins,low,high,unit,plot data]
["3 Mu Invariant Mass","m3l","m3l",83,0,83,"GeV",True],
["3 Mu + MET Transverse Mass","mt","mt",100,0,250,"GeV",True],
["Lower Mass diMu Pair","mass2","M2",160,0,80,"GeV",False],
["Higher Mass diMu Pair","mass1","M1",160,0,80,"GeV",False],
["Same Sign diMu Pair","sameMass","M0",160,0,80,"GeV",True],
["dR Between Lower Mass diMu","dRM2","dRM2",100,0,6,"dR",False],
["dR Between Higher Mass diMu","dRM1","dRM1",100,0,6,"dR",False],
["dR Between Same Sign diMu","dRM0","dRM0",100,0,6,"dR",True],

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
["Leading Medium ID","medIdL1","medIdL1",2,0,2,"True",True],
["Subleading Medium ID","medIdL2","medIdL2",2,0,2,"True",True],
["Trailing Medium ID","medIdL3","medIdL3",2,0,2,"True",True],
["Leading mva ID","mvaIdL1","mvaIdL1",6,0,6,"ID",True],
["Subleading mva ID","mvaIdL2","mvaIdL2",6,0,6,"ID",True],
["Trailing mva ID","mvaIdL3","mvaIdL3",6,0,6,"ID",True],

["Worst Isolation","worstIso","worstIso",60,0,.6,"pfRelIso03_all",True],
["Worst dxy","worstdxy","worstdxy",50,0,1,"cm",True],
["Worst dz","worstdz","worstdz",50,0,1,"cm",True],
["Worst 3D Impact Parameter","worstip3d","worstip3d",25,0.,0.1,"IP3D",True],
["Worst Significance of 3D Impact Parameter","worstsip3d","worstsip3d",100,0.,10.,"SIP3D",True],
["Worst Medium ID","worstmedId","worstmedId",2,0,2,"True",True],
["Worst mva ID","worstmvaId","worstmvaId",6,0,6,"ID",True],

["Transverse Missing Energy","met","met",50,0,250,"GeV",True],
["Transver Missing Energy Phi","met_phi","met_phi",40,-4,4,"phi",True],
["dR Between Leading and Subleading","dR12","dR12",100,0,6,"dR",True],
["dR Between Leading and Trailing","dR13","dR13",100,0,6,"dR",True],
["dR Between Subleading and Trailing","dR23","dR23",100,0,6,"dR",True],
["Number of b Jets","nbJets","nbJets",2,0,2,"n",True],
["Number of Jets","nJets","nJets",12,0,12,"n",True],

]

cuts = [

#[Title,save name,variable plotted,nBins,low,high,unit,less than]
["Worst Isolation","worstIso","worstIso",60,0,.6,"pfRelIso03_all",True],
["Worst dxy","worstdxy","worstdxy",50,0,1,"cm",True],
["Worst dz","worstdz","worstdz",50,0,1,"cm",True],
["Worst 3D Impact Parameter","worstip3d","worstip3d",25,0.,0.1,"IP3D",True],
["Worst Significance of 3D Impact Parameter","worstsip3d","worstsip3d",100,0.,10.,"SIP3D",True],
["Worst Medium ID","worstmedId","worstmedId",2,0,2,"True",True],
#["Worst mva ID","worstmvaId","worstmvaId",6,0,6,"ID",True],

["3 Mu Invariant Mass","m3l","m3l",83,0,83,"GeV",True],
["3 Mu + MET Transverse Mass","mt","mt",100,0,250,"GeV",True],

["Leading pT","pTL1","pTL1",100,0,100,"GeV",True],
["Subleading pT","pTL2","pTL2",80,0,80,"GeV",True],
["Trailing pT","pTL3","pTL3",50,0,50,"GeV",True],

["Transverse Missing Energy","met","met",50,0,250,"GeV",True],
#["Transver Missing Energy Phi","met_phi","met_phi",40,-4,4,"phi",True],
["dR Between Leading and Subleading","dR12","dR12",100,0,6,"dR",True],
["dR Between Leading and Trailing","dR13","dR13",100,0,6,"dR",True],
["dR Between Subleading and Trailing","dR23","dR23",100,0,6,"dR",True],
#["Number of b Jets","nbJets","nbJets",2,0,2,"n",True],
["Number of Jets","nJets","nJets",12,0,12,"n",True],

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
	data["selection"], effs[samples[i]] = skim_opt(data,samples[i])
	if sType == "MC":
		data["weight_arr"] = data["weight"]*data["genWeight"]*data["pileupWeight"]
	else:
		data["weight_arr"] = np.ones(len(data["genWeight"]))

	selected = data
	selection = selected["selection"]
	for key in selected:
		if key=="weight" or key=="sType": continue
		selected[key] = selected[key][selection]

	# Save resulting data
	if sType == "MC":
		if not bkg:
			bkg = selected
		else:
			for key in selected:
				bkg[key] = np.append(bkg[key],selected[key])
	elif sType == "sig":
		sig[samples[i]] = selected

	with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
		pickle.dump(data, handle)

#tot_bkg = np.sum(bkg["weight_arr"])
#tot_sig = np.sum(sig["Wto3l_M4"]["weight_arr"])
#og_ratio = tot_sig/np.sqrt(tot_bkg)
#print("Total number of bkg events: %.2f"%(tot_bkg))
#print("Total number of sig events: %.2f"%(tot_sig))
#print("Original ratio = %.2f"%(og_ratio))

print("")
print("Optimizing cuts for each signal mass")
best_ratio, best_cut = {}, {}
for m in tqdm(sig_masses):
	for c in tqdm(cuts,leave=False):
		best_cut["%i_%s<"%(m,c[1])], best_cut["%i_%s>"%(m,c[1])], = ROC(bkg,sig["Wto3l_M%i"%(m)],c,"Wto3l_M%i"%(m),plots,m)

		effs2 = copy.deepcopy(effs)
		for i in range(len(samples)):
			with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
				data[samples[i]] = pickle.load(handle)

			selection2 = (data[samples[i]][c[2]] <= best_cut["%i_%s<"%(m,c[1])]) * data[samples[i]]["selection"]
			effs2[samples[i]]["%s < %.2f"%(c[0],best_cut["%i_%s<"%(m,c[1])])] = np.count_nonzero(selection2)/np.count_nonzero(data[samples[i]]["selection"])*100
			data[samples[i]]["selection"] = selection2

		for p in tqdm(plots,leave=False):
			outy = "Optimize/Wto3l_M%i/%s</"%(m,c[1])
			plot(data,p,samples,error_on_MC,outy)

		effs3 = copy.deepcopy(effs)
		for i in range(len(samples)):
			with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
				data[samples[i]] = pickle.load(handle)

			selection3 = (data[samples[i]][c[2]] >= best_cut["%i_%s>"%(m,c[1])]) * data[samples[i]]["selection"]
			effs3[samples[i]]["%s > %.2f"%(c[0],best_cut["%i_%s>"%(m,c[1])])] = np.count_nonzero(selection3)/np.count_nonzero(data[samples[i]]["selection"])*100
			data[samples[i]]["selection"] = selection3
			
		for p in tqdm(plots,leave=False):
			outy = "Optimize/Wto3l_M%i/%s>/"%(m,c[1])
			plot(data,p,samples,error_on_MC,outy)
		
		cuts_tab = ["Sample"]
		for key in effs2[samples[0]]:
			cuts_tab.append(key)
		x = PrettyTable(cuts_tab)
		for key in effs2:
			row = [key]
			for key2 in effs2[key]:
				row.append("%.2f%%"%(effs2[key][key2]))
			x.add_row(row)
		table = open("/orange/avery/nikmenendez/Output/Optimize/Wto3l_M%i/%s</Efficiency_Table.txt"%(m,c[1]),"w")
		table.write(x.get_string())
		table.close()

		cuts_tab = ["Sample"]
		for key in effs3[samples[0]]:
			cuts_tab.append(key)
		x = PrettyTable(cuts_tab)
		for key in effs3:
			row = [key]
			for key2 in effs3[key]:
				row.append("%.2f%%"%(effs3[key][key2]))
			x.add_row(row)
		table = open("/orange/avery/nikmenendez/Output/Optimize/Wto3l_M%i/%s>/Efficiency_Table.txt"%(m,c[1]),"w")
		table.write(x.get_string())
		table.close()

print("Plotting Optimal Cuts Across Signal Masses")

for c in tqdm(cuts):
	opt_cut_lt, opt_cut_gt = np.zeros(len(sig_masses)), np.zeros(len(sig_masses))
	for i in range(len(sig_masses)):
		opt_cut_lt[i] = best_cut["%i_%s<"%(sig_masses[i],c[1])]
		opt_cut_gt[i] = best_cut["%i_%s>"%(sig_masses[i],c[1])]

	plt.plot(sig_masses,opt_cut_lt)
	plt.scatter(sig_masses,opt_cut_lt)
	plt.xlabel("Signal Mass (GeV)")
	plt.ylabel("%s (%s)"%(c[0],c[6]))
	plt.title("Optimal Cut for <= %s per Signal Mass"%(c[0]))
	plt.savefig("/orange/avery/nikmenendez/Output/Optimize/to_opt/%s<.png"%(c[1]))
	plt.clf()

	plt.plot(sig_masses,opt_cut_gt)
	plt.scatter(sig_masses,opt_cut_gt)
	plt.xlabel("Signal Mass (GeV)")
	plt.ylabel("%s (%s)"%(c[0],c[6]))
	plt.title("Optimal Cut for >= %s per Signal Mass"%(c[0]))
	plt.savefig("/orange/avery/nikmenendez/Output/Optimize/to_opt/%s>.png"%(c[1]))
	plt.clf()

print('\a')
print("Uploading plots to web")
import subprocess
subprocess.run(["scp","-r","/orange/avery/nikmenendez/Output/Optimize/","nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/Optimizer/"])
