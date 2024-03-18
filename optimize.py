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
samples = background_samples + signal_samples
#samples = ["WZTo3LNu","ZZTo4L","fake"] + signal_samples
files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)
sig_masses = [4,5,15,30,45,60]

#lumi = 41.4*1000
lumi = 59.8*1000
error_on_MC = False

out_dir = "to_opt"
#if not os.path.exists("/orange/avery/nikmenendez/Output/Optimize5/"): os.makedirs("/orange/avery/nikmenendez/Output/Optimize5/")
#if not os.path.exists("/orange/avery/nikmenendez/Output/Optimize5/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/Output/Optimize5/%s/"%(out_dir))
#if not os.path.exists("/orange/avery/nikmenendez/Output/pickle/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/Output/pickle/%s/"%(out_dir))
if not os.path.exists("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/Optimize5/"): os.makedirs("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/Optimize5/")
if not os.path.exists("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/Optimize5/%s/"%(out_dir)): os.makedirs("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/Optimize5/%s/"%(out_dir))
if not os.path.exists("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/pickle/%s/"%(out_dir)): os.makedirs("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/pickle/%s/"%(out_dir))

plots = [

# 1D Plots
#[Title,save name,variable plotted,nBins,low,high,unit,plot data]
["3 Mu Invariant Mass","m3l","m3l",83,0,83,"GeV",True],
["3 Mu pT","m3l_pt","m3l_pt",200,0,200,"GeV",True],
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
["Number of b Jets","nbJets","nbJets",4,0,4,"n",True],
["Number of Jets","nJets","nJets",12,0,12,"n",True],
["Number of Muons","nMuons","nMuons",6,0,6,"n",True],
["Number of Good Muons","nGoodMuons","nGoodMuons",6,0,6,"n",True],

#["Neural Network Discriminant","discriminator","discriminator",100,0,1,"",True]

]

cuts = [

#[Title,save name,variable plotted,nBins,low,high,unit,less than]
#["Worst Isolation","worstIso","worstIso",60,0,.6,"pfRelIso03_all",True],
#["Worst dxy","worstdxy","worstdxy",50,0,1,"cm",True],
#["Worst dz","worstdz","worstdz",50,0,1,"cm",True],
#["Worst 3D Impact Parameter","worstip3d","worstip3d",25,0.,0.1,"IP3D",True],
#["Worst Significance of 3D Impact Parameter","worstsip3d","worstsip3d",100,0.,10.,"SIP3D",True],
#["Worst Medium ID","worstmedId","worstmedId",2,0,2,"True",True],
["Worst mva ID","worstmvaId","worstmvaId",6,0,6,"ID",True],
["Leading mva ID","mvaIdL1","mvaIdL1",6,0,6,"ID",True],
["Subleading mva ID","mvaIdL2","mvaIdL2",6,0,6,"ID",True],
["Trailing mva ID","mvaIdL3","mvaIdL3",6,0,6,"ID",True],

#["3 Mu Invariant Mass","m3l","m3l",83,0,83,"GeV",True],
#["3 Mu + MET Transverse Mass","mt","mt",100,0,250,"GeV",True],
#["3 Mu pT","m3l_pt","m3l_pt",200,0,200,"GeV",True],
#
#["Leading pT","pTL1","pTL1",100,0,100,"GeV",True],
#["Subleading pT","pTL2","pTL2",80,0,80,"GeV",True],
#["Trailing pT","pTL3","pTL3",50,0,50,"GeV",True],
#
#["Transverse Missing Energy","met","met",50,0,250,"GeV",True],
##["Transverse Missing Energy Phi","met_phi","met_phi",40,-4,4,"phi",True],
#["dR Between Leading and Subleading","dR12","dR12",100,0,6,"dR",True],
#["dR Between Leading and Trailing","dR13","dR13",100,0,6,"dR",True],
#["dR Between Subleading and Trailing","dR23","dR23",100,0,6,"dR",True],
#["Number of Jets","nJets","nJets",12,0,12,"n",True],
#["Number of b Jets","nbJets","nbJets",4,0,4,"n",True],
#["Number of Muons","nMuons","nMuons",6,0,6,"n",True],
#["Number of Good Muons","nGoodMuons","nGoodMuons",6,0,6,"n",True],

#["Neural Network Discriminant","discriminator","discriminator",100,0,1,"",True]

]

xs, sumW = combXS(xs_sig,sumW_sig,xs_bkg,sumW_bkg)
effs = {}
sig, bkg = {}, {}
for i in range(len(samples)):
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

	vars_in = signal_vars
	temp = events.arrays(vars_in)

	data = {}
	data = events.arrays(vars_in, library="np")
	#for key in temp: data[key.decode("utf-8")] = temp[key]
	del temp
	data["weight"] = weight
	data["sType"] = sType
	if not (("data" in samples[i]) or ("fake" in samples[i])):
		data["pileupWeight"] = data["pileupWeight"]/32
	#print("Reading in %s with %i events"%(samples[i],len(data["nMuons"])))
	print("%i events... "%(len(data["nMuons"])),end='',flush=True)


	# Select other variables
	print("Selecting Vars... ",end='',flush=True)
	data = select(data)

	# Perform Cuts
	print("Skimming... ",end='',flush=True)
	data["selection"], effs[samples[i]], data["fail"], data["fail2"] = skim_opt(data,samples[i])

	print("Weighting... ",end='',flush=True)
	data["fake_weight"] = Fake_weight(data,samples[i])
	data["eventWeight"] = data["genWeight"]*data["pileupWeight"]*data["fake_weight"]*data["weight"]
	#data["eventWeight"] = data["genWeight"]*data["pileupWeight"]*data["fakeWeight"]*data["weight"]
	if "fake" in samples[i]:
		data["genWeight"] = data["genWeight"]*data["fake_weight"]*data["fail"] + data["genWeight"]*data["fake_weight"]*data["fail2"]

	if "data" in samples[i]:
		data["weight_arr"] = np.ones(len(data["genWeight"]))
	else:
		data["weight_arr"] = data["weight"]*data["genWeight"]*data["pileupWeight"]
		

	selected = data
	selection = selected["selection"]
	for key in selected:
		if key=="weight" or key=="sType": continue
		selected[key] = selected[key][selection]

	print("Saving... ",end='',flush=True)
	# Save resulting data
	if sType != "sig":
		if not bkg:
			bkg = selected
		else:
			for key in selected:
				bkg[key] = np.append(bkg[key],selected[key])
	elif sType == "sig":
		sig[samples[i]] = selected

	#with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
	with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
		pickle.dump(data, handle)
	print("Done!")

#tot_bkg = np.sum(bkg["weight_arr"])
#tot_sig = np.sum(sig["Wto3l_M4"]["weight_arr"])
#og_ratio = tot_sig/np.sqrt(tot_bkg)
#print("Total number of bkg events: %.2f"%(tot_bkg))
#print("Total number of sig events: %.2f"%(tot_sig))
#print("Original ratio = %.2f"%(og_ratio))

print("")
print("Optimizing cuts for each signal mass")
ratios, cut_values, best_cut = {}, {}, {}
for m in tqdm(sig_masses):
	for c in tqdm(cuts,leave=False):
		best_cut["%i_%s<"%(m,c[1])], best_cut["%i_%s>"%(m,c[1])], ratios["%i_%s<"%(m,c[1])], ratios["%i_%s>"%(m,c[1])], cut_values["%i_%s<"%(m,c[1])], cut_values["%i_%s>"%(m,c[1])] = ROC(bkg,sig["Wto3l_M%i"%(m)],c,"Wto3l_M%i"%(m),plots,m)

		effs2 = copy.deepcopy(effs)
		for i in range(len(samples)):
			#with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
			with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
				data[samples[i]] = pickle.load(handle)

			selection2 = (data[samples[i]][c[2]] <= best_cut["%i_%s<"%(m,c[1])]) * data[samples[i]]["selection"]
			effs2[samples[i]]["%s < %.2f"%(c[0],best_cut["%i_%s<"%(m,c[1])])] = np.count_nonzero(selection2)/np.count_nonzero(data[samples[i]]["selection"])*100
			data[samples[i]]["selection"] = selection2

		for p in tqdm(plots,leave=False):
			outy = "Optimize5/Wto3l_M%i/%s</"%(m,c[1])
			plot(data,p,samples,error_on_MC,outy,False)

		effs3 = copy.deepcopy(effs)
		for i in range(len(samples)):
			#with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
			with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
				data[samples[i]] = pickle.load(handle)

			selection3 = (data[samples[i]][c[2]] >= best_cut["%i_%s>"%(m,c[1])]) * data[samples[i]]["selection"]
			effs3[samples[i]]["%s > %.2f"%(c[0],best_cut["%i_%s>"%(m,c[1])])] = np.count_nonzero(selection3)/np.count_nonzero(data[samples[i]]["selection"])*100
			data[samples[i]]["selection"] = selection3
			
		for p in tqdm(plots,leave=False):
			outy = "Optimize5/Wto3l_M%i/%s>/"%(m,c[1])
			plot(data,p,samples,error_on_MC,outy,False)
		
		cuts_tab = ["Sample"]
		for key in effs2[samples[0]]:
			cuts_tab.append(key)
		x = PrettyTable(cuts_tab)
		for key in effs2:
			row = [key]
			for key2 in effs2[key]:
				row.append("%.2f%%"%(effs2[key][key2]))
			x.add_row(row)
		#table = open("/orange/avery/nikmenendez/Output/Optimize5/Wto3l_M%i/%s</Efficiency_Table.txt"%(m,c[1]),"w")
		table = open("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/Optimize5/Wto3l_M%i/%s</Efficiency_Table.txt"%(m,c[1]),"w")
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
		#table = open("/orange/avery/nikmenendez/Output/Optimize5/Wto3l_M%i/%s>/Efficiency_Table.txt"%(m,c[1]),"w")
		table = open("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/Optimize5/Wto3l_M%i/%s>/Efficiency_Table.txt"%(m,c[1]),"w")
		table.write(x.get_string())
		table.close()

print("Plotting Optimal Cuts Across Signal Masses")

for c in tqdm(cuts):
	#opt_cut_lt, opt_cut_gt = np.zeros(len(sig_masses)), np.zeros(len(sig_masses))
	#for i in range(len(sig_masses)):
	#	opt_cut_lt[i] = best_cut["%i_%s<"%(sig_masses[i],c[1])]
	#	opt_cut_gt[i] = best_cut["%i_%s>"%(sig_masses[i],c[1])]

	#plt.plot(sig_masses,opt_cut_lt)
	#plt.scatter(sig_masses,opt_cut_lt)
	#plt.xlabel("Signal Mass (GeV)")
	#plt.ylabel("%s (%s)"%(c[0],c[6]))
	#plt.title("Optimal Cut for <= %s per Signal Mass"%(c[0]))
	#plt.savefig("/orange/avery/nikmenendez/Output/Optimize5/to_opt/%s<.png"%(c[1]))
	#plt.clf()

	#plt.plot(sig_masses,opt_cut_gt)
	#plt.scatter(sig_masses,opt_cut_gt)
	#plt.xlabel("Signal Mass (GeV)")
	#plt.ylabel("%s (%s)"%(c[0],c[6]))
	#plt.title("Optimal Cut for >= %s per Signal Mass"%(c[0]))
	#plt.savefig("/orange/avery/nikmenendez/Output/Optimize5/to_opt/%s>.png"%(c[1]))
	#plt.clf()

	sam_vals, cut_vals, weights = [], [], []
	for i in range(len(sig_masses)):
		for j in range(len(ratios["%i_%s<"%(sig_masses[i],c[1])])):
			sam_vals.append(sig_masses[i])
			cut_vals.append(cut_values["%i_%s<"%(sig_masses[i],c[1])][j])
			weights.append(ratios["%i_%s<"%(sig_masses[i],c[1])][j])

	sam_bins = [0]
	for i in range(len(sig_masses)):
		if i+1<len(sig_masses):
			sam_bins.append((sig_masses[i]+sig_masses[i+1])/2)
		else:
			sam_bins.append(80)

	fig, ax = plt.subplots()
	hh = ax.hist2d(sam_vals,cut_vals,bins=[sam_bins,c[3]],range=[[0,80],[c[4],c[5]]],weights=weights,cmap=plt.cm.nipy_spectral)
	fig.colorbar(hh[3])
	plt.xlabel("Signal Mass (GeV)")
	plt.ylabel("%s (%s)"%(c[0],c[6]))
	plt.title("Cut Improvements for <= %s per Signal Mass"%(c[0]))
	#plt.savefig("/orange/avery/nikmenendez/Output/Optimize5/to_opt/%s<.png"%(c[1]))
	plt.savefig("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/Optimize5/to_opt/%s<.png"%(c[1]))
	plt.clf()

	sam_vals, cut_vals, weights = [], [], []
	for i in range(len(sig_masses)):
		for j in range(len(ratios["%i_%s>"%(sig_masses[i],c[1])])):
			sam_vals.append(sig_masses[i])
			cut_vals.append(cut_values["%i_%s>"%(sig_masses[i],c[1])][j])
			weights.append(ratios["%i_%s>"%(sig_masses[i],c[1])][j])

	fig, ax = plt.subplots()
	hh = ax.hist2d(sam_vals,cut_vals,bins=[sam_bins,c[3]],range=[[0,80],[c[4],c[5]]],weights=weights,cmap=plt.cm.nipy_spectral)
	fig.colorbar(hh[3])
	plt.xlabel("Signal Mass (GeV)")
	plt.ylabel("%s (%s)"%(c[0],c[6]))
	plt.title("Cut Improvements for >= %s per Signal Mass"%(c[0]))
	#plt.savefig("/orange/avery/nikmenendez/Output/Optimize5/to_opt/%s>.png"%(c[1]))
	plt.savefig("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/Optimize5/to_opt/%s>.png"%(c[1]))
	plt.clf()


print('\a')
print("Uploading plots to web")
#print("scp -r /publicfs/cms/data/hzz/guoqy/Zprime/results/Output/Optimize5/%s/ qguo@lxplus.cern.ch:/eos/user/q/qguo/www/Wto3l/SR_Selection/Optimize5/"%(out_dir))
print("scp -r qyguo@lxslc7.ihep.ac.cn://publicfs/cms/data/hzz/guoqy/Zprime/results/Output/Optimize5/%s/ /eos/user/q/qguo/www/Wto3l/SR_Selection/Optimize5/"%(out_dir))
print("cp /eos/user/q/qguo/www/Wto3l/SR_Selection/ZpX/UL/Output/index.php  /eos/user/q/qguo/www/Wto3l/SR_Selection/Optimize5/%s/"%(out_dir))
#import subprocess
#subprocess.run(["scp","-r","/orange/avery/nikmenendez/Output/Optimize5/","nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/Optimizer/"])
