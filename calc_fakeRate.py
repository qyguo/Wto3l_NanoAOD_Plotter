from __future__ import division
import numpy as np
import uproot
import sys
import matplotlib.pyplot as plt
import os
import pickle
import time
from tqdm import tqdm
from prettytable import PrettyTable

from Utils.combXS import *
from Datasets.Signal.Wto3l import *
from Datasets.Run2017.Data import *
from Datasets.Run2017.Background import *
from Skimmer.AnalysisSkimmer import *
from Skimmer.FakeSkimmer import *
from Skimmer.ZSelector import *
from Plotter.Plot import *
from FakeRate.Fake_calc import *
from FakeRate.Fake_weight import *

MC_measure = False

#Define parameters from plotting
samples = background_samples + ["data"]#data_samples
#samples = ["ZZTo4L","WZTo3LNu","data"]
#samples = ["ZZTo4L","WZTo3LNu","DYJetsToLL_M0To1","data"]
files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)

if "data" in samples: MC_measure = False
else: MC_measure = True

lumi = 41.4*1000
error_on_MC = False
pt_bins = [5,10,15,20,30,60]
#pt_bins = [5,10,15,20,30,40,60]
#pt_bins = [5,10,15,20,30,45,60,80,100]
#pt_bins = [5,8,10,12,15,20,30,100]
#pt_bins = [5,8,10,12,15,20,30,60,100]
#pt_bins = [5,10,20,30,45,80]

#out_dir = "FakeRate_tightIdIso_loosePre_Zdiff10_MET40_NoDr1312_tightCut"
#out_dir = "FakeRate_tightIDlooseIso_tightPre_Zdiff10_MET40_NoDr1312_tightCut_tightlep12"
out_dir = "FakeRate_test2"
#if not os.path.exists("/orange/avery/nikmenendez/Output/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/Output/%s/"%(out_dir))
#if not os.path.exists("/orange/avery/nikmenendez/pickle/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/pickle/%s/"%(out_dir))
if not os.path.exists("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/"%(out_dir)): os.makedirs("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/"%(out_dir))
if not os.path.exists("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/"%(out_dir)): os.makedirs("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/"%(out_dir))
#if not os.path.exists("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/Output/%s/"%(out_dir)): os.makedirs("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/Output/%s/"%(out_dir))

# CALCULATE FAKERATE

plots = [

# 1D Plots
#[Title,save name,variable plotted,nBins,low,high,unit,plot data]
["3 Lep Invariant Mass",		"looseNT_m3l","m3l",50,0,250,"GeV",True,							"fail"],
["Electron Pair Mass",			"looseNT_mass1","M1",50,0,200,"GeV",True,							"fail"],
["Muon pT",						"looseNT_pTL3","pTL3",int(pt_bins[-1]/2),0,pt_bins[-1],"GeV",True,	"fail"],
["Fail pT",						"looseNT_failpT","pTL3",pt_bins,0,60,"GeV",True,					"fail"],
["3 Lep + MET Transverse Mass",	"looseNT_mt","mt",50,0,300,"GeV",True,								"fail"],
["Transverse Missing Energy",	"looseNT_met","met",50,0,250,"GeV",True,							"fail"],
["Transver Missing Energy Phi",	"looseNT_met_phi","met_phi",40,-4,4,"phi",True,						"fail"],
["2e Electron Transverse Mass",	"looseNT_M1T","M1T",100,0,200,"GeV",True,							"fail"],
["Number of Electrons",			"looseNT_nElec","nElectrons",6,0,6,"n",True,						"fail"],
["Number of Leptons",			"looseNT_nLep","nLeptons",6,0,6,"n",True,							"fail"],
["Number of Good Leptons",		"looseNT_nGoodLep","nGoodLeptons",6,0,6,"n",True,					"fail"],
["3 Mu pT",						"looseNT_m3l_pt","m3l_pt",75,0,150,"GeV",True,						"fail"],
["dR Between e1 and e2",		"looseNT_dR12","dR12",100,0,6,"dR",True,							"fail"],
["dR Between e1 and Muon",		"looseNT_dR13","dR13",100,0,6,"dR",True,							"fail"],
["dR Between e2 and Muon",		"looseNT_dR23","dR23",100,0,6,"dR",True,							"fail"],
["Muon eta",					"looseNT_etaL3","etaL3",60,-3.,3.,"eta",True,						"fail"], 
["Muon phi",					"looseNT_phiL3","phiL3",40,-4.,4.,"phi",True,						"fail"], 
["Muon Isolation",				"looseNT_IsoL3","IsoL3",50,0.,0.5,"pfRelIso03_all",True,			"fail"], 
["Muon 3D Impact Parameter",	"looseNT_ip3dL3","ip3dL3",25,0.,0.05,"IP3D",True,					"fail"], 
["Muon Significance of 3D IP",	"looseNT_sip3dL3","sip3dL3",40,0.,4.,"SIP3D",True,					"fail"], 
["Muon mvaId",					"looseNT_mvaIdL3","mvaIdL3",6,0,6,"ID",True,						"fail"],
["Muon Origin",					"looseNT_sourceL3","sourceL3",10,-1,9,"Muon Origin",False,          "fail"],

["3 Lep Invariant Mass",		"tight_m3l","m3l",50,0,250,"GeV",True,								"pass"],
["Electron Pair Mass",			"tight_mass1","M1",50,0,200,"GeV",True,								"pass"],
["Muon pT",						"tight_pTL3","pTL3",int(pt_bins[-1]/2),0,pt_bins[-1],"GeV",True,	"pass"],
["Pass pT",						"tight_passpT","pTL3",pt_bins,0,60,"GeV",True,						"pass"],
["3 Lep + MET Transverse Mass",	"tight_mt","mt",50,0,300,"GeV",True,								"pass"],
["Transverse Missing Energy",	"tight_met","met",50,0,250,"GeV",True,								"pass"],
["Transver Missing Energy Phi",	"tight_met_phi","met_phi",40,-4,4,"phi",True,						"pass"],
["2e Electron Transverse Mass",	"tight_M1T","M1T",100,0,200,"GeV",True,								"pass"],
["Number of Electrons",			"tight_nElec","nElectrons",6,0,6,"n",True,							"pass"],
["Number of Leptons",			"tight_nLep","nLeptons",6,0,6,"n",True,								"pass"],
["Number of Good Leptons",		"tight_nGoodLep","nGoodLeptons",6,0,6,"n",True,						"pass"],
["3 Mu pT",						"tight_m3l_pt","m3l_pt",75,0,150,"GeV",True,						"pass"],
["dR Between e1 and e2",		"tight_dR12","dR12",100,0,6,"dR",True,								"pass"],
["dR Between e1 and Muon",		"tight_dR13","dR13",100,0,6,"dR",True,								"pass"],
["dR Between e2 and Muon",		"tight_dR23","dR23",100,0,6,"dR",True,								"pass"],
["Muon eta",					"tight_etaL3","etaL3",60,-3.,3.,"eta",True,							"pass"], 
["Muon phi",					"tight_phiL3","phiL3",40,-4.,4.,"phi",True,							"pass"], 
["Muon Isolation",				"tight_IsoL3","IsoL3",50,0.,0.5,"pfRelIso03_all",True,				"pass"], 
["Muon 3D Impact Parameter",	"tight_ip3dL3","ip3dL3",25,0.,0.05,"IP3D",True,						"pass"], 
["Muon Significance of 3D IP",	"tight_sip3dL3","sip3dL3",40,0.,4.,"SIP3D",True,					"pass"], 
["Muon mvaId",					"tight_mvaIdL3","mvaIdL3",6,0,6,"ID",True,							"pass"],
["Muon Origin",					"tight_sourceL3","sourceL3",10,-1,9,"Muon Origin",False,          	"pass"],

["3 Lep Invariant Mass",		"loose_m3l","m3l",50,0,250,"GeV",True,								"none"],
["Electron Pair Mass",			"loose_mass1","M1",50,0,200,"GeV",True,								"none"],
["Muon pT",						"loose_pTL3","pTL3",int(pt_bins[-1]/2),0,pt_bins[-1],"GeV",True,	"none"],
["Loose pT",					"loose_loosepT","pTL3",pt_bins,0,60,"GeV",True,						"none"],
["3 Lep + MET Transverse Mass",	"loose_mt","mt",50,0,300,"GeV",True,								"none"],
["Transverse Missing Energy",	"loose_met","met",50,0,250,"GeV",True,								"none"],
["Transver Missing Energy Phi",	"loose_met_phi","met_phi",40,-4,4,"phi",True,						"none"],
["2e Electron Transverse Mass",	"loose_M1T","M1T",100,0,200,"GeV",True,								"none"],
["Number of Electrons",			"loose_nElec","nElectrons",6,0,6,"n",True,							"none"],
["Number of Leptons",			"loose_nLep","nLeptons",6,0,6,"n",True,								"none"],
["Number of Good Leptons",		"loose_nGoodLep","nGoodLeptons",6,0,6,"n",True,						"none"],
["3 Mu pT",						"loose_m3l_pt","m3l_pt",75,0,150,"GeV",True,						"none"],
["dR Between e1 and e2",		"loose_dR12","dR12",100,0,6,"dR",True,								"none"],
["dR Between e1 and Muon",		"loose_dR13","dR13",100,0,6,"dR",True,								"none"],
["dR Between e2 and Muon",		"loose_dR23","dR23",100,0,6,"dR",True,								"none"],
["Muon eta",					"loose_etaL3","etaL3",60,-3.,3.,"eta",True,							"none"], 
["Muon phi",					"loose_phiL3","phiL3",40,-4.,4.,"phi",True,							"none"], 
["Muon Isolation",				"loose_IsoL3","IsoL3",50,0.,0.5,"pfRelIso03_all",True,				"none"], 
["Muon 3D Impact Parameter",	"loose_ip3dL3","ip3dL3",25,0.,0.05,"IP3D",True,						"none"], 
["Muon Significance of 3D IP",	"loose_sip3dL3","sip3dL3",40,0.,4.,"SIP3D",True,					"none"], 
["Muon mvaId",					"loose_mvaIdL3","mvaIdL3",6,0,6,"ID",True,							"none"],
["Muon Origin",					"loose_sourceL3","sourceL3",10,-1,9,"Muon Origin",False,          	"none"],
]

print("Calculating Fake Rate and Fake Weight")
xs, sumW = combXS(xs_sig,sumW_sig,xs_bkg,sumW_bkg)
effs = {}
for i in range(len(samples)):
	tic = time.perf_counter()
	print("Processing %s... "%(samples[i]),end='',flush=True)
	if "data" not in samples[i]:
		weight = xs[samples[i]]/sumW[samples[i]]*lumi
	else:
		weight = xs[samples[i]]/sumW[samples[i]]
	if "Wto3l" in samples[i]: sType = "sig"
	elif "data" in samples[i]: sType = "data"
	else: sType = "MC"	

	print("Reading in ",end='',flush=True)
	file = uproot.open(files[samples[i]])
	events = file["passedEvents"]
	#events.show()
	#print(events.keys())
	#print(events.typenames())

	vars_in = signal_vars
	#print(vars_in)
	temp = events.arrays(vars_in)
	#print(temp)
	#print(temp["genWeight"])
	#print(temp["nMuons"])
	#temp["genWeight"].array(library="np")
	#print("genWeight", )

	data = {}
	data = events.arrays(vars_in, library="np")
	#for key1 in temp: print(key1)
	#for key in temp: data[key.decode("utf-8")] = temp[key]
	del temp
	data["weight"] = np.array([weight]*len(data["nMuons"]))
	data["sType"] = np.array([sType]*len(data["nMuons"]))
	if "data" not in samples[i]:
		data["pileupWeight"] = data["pileupWeight"]/32
	#print("Processing %s with %i events"%(samples[i],len(data["nMuons"])))
	print("%i events... "%(len(data["nMuons"])),end='',flush=True)

	# Select other variables
	print("Selecting Vars... ",end='',flush=True)
	data = select(data)

	# Perform Cuts
	print("Skimming... ",end='',flush=True)
	data["selection"],effs[samples[i]],data["selection_fail"],data["selection_pass"] = skim(data)

	#data["selection_pass"], data["selection_fail"] = fake_skim(data)

	# Save resulting data
	print("Saving Results... ",end='',flush=True)
	all_vars = data.keys()
	if MC_measure:
		#if samples[i] not in ["ZZTo4L","WZTo3LNu","DYJetsToLL_M0To1"]:
		#	with open("/orange/avery/nikmenendez/pickle/%s/%s.p"%(out_dir,"data"),'ab') as handle:
		#		pickle.dump(data, handle)
		#else:
		#	with open("/orange/avery/nikmenendez/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
		#		pickle.dump(data, handle)
		#	with open("/orange/avery/nikmenendez/pickle/%s/%s.p"%(out_dir,"data"),'ab') as handle:
		#		pickle.dump(data, handle)
		#with open("/orange/avery/nikmenendez/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
		with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
			pickle.dump(data, handle)

		data["sType"] = np.array(["data"]*len(data["nMuons"]))
		#with open("/orange/avery/nikmenendez/pickle/%s/%s.p"%(out_dir,"data"),'ab') as handle:
		with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/%s.p"%(out_dir,"data"),'ab') as handle:
			pickle.dump(data, handle)
	else:
		#with open("/orange/avery/nikmenendez/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
		with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
			pickle.dump(data, handle)
	print("Done! ",end='',flush=True)
	toc = time.perf_counter()
	tot_time = toc-tic
	if tot_time<60:
		print("Total time was %.2f seconds"%(tot_time))
	else:
		print("Total time was %.2f minutes"%(tot_time/60))

print("Combining Samples...")
data = {}
if MC_measure:
	#samples2 = ["ZZTo4L","WZTo3LNu","DYJetsToLL_M0To1","data"]
	samples2 = samples + ["data"]
	for s in samples2:
		print("Opening %s"%(s))
		if s!="data":
			#with open("/orange/avery/nikmenendez/pickle/%s/%s.p"%(out_dir,s),'rb') as handle:
			with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/%s.p"%(out_dir,s),'rb') as handle:
				data[s] = pickle.load(handle)
		else:
			data[s] = {}
			for v in all_vars:
				data[s][v] = np.array([])
			#with open("/orange/avery/nikmenendez/pickle/%s/%s.p"%(out_dir,s),'rb') as handle:
			with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/%s.p"%(out_dir,s),'rb') as handle:
				for q in samples:
					#if q in samples2: continue

					temp = pickle.load(handle)
					for v in all_vars:
						temp2 = np.concatenate((data[s][v],temp[v]), axis=None)
						if "selection" in v:
							temp2 = temp2==1
						data[s][v] = temp2
			print(v)
			print(data[s][v])
else:
	for i in range(len(samples)):
		#with open("/orange/avery/nikmenendez/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
		with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
			data[samples[i]] = pickle.load(handle)

#print(data.keys())

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

if MC_measure: samples = samples2

fake_weight_b, fake_weight_e = fake_calc(data,samples,pt_bins,out_dir)
print("pT bins:")
print(pt_bins)
print("Fake Weight in barrel:")
print(*fake_weight_b,sep=", ")
print("Fake Weight in endcap:")
print(*fake_weight_e,sep=", ")

# Make Plots
print("Generating Plots")
for p in tqdm(plots):
	plot(data,p,samples,error_on_MC,out_dir,True)


## APPLY AND VALIDATE FAKE RATE
#
#print("")
#print("Applying and Validating Fake Weight")
#
#samples = ["ZZTo4L","WZTo3LNu","DYJetsToLL_M0To1","fake","data"]
#files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)
#
#plots = [
#
## 1D Plots
##[Title,save name,variable plotted,nBins,low,high,unit,plot data]
#["3 Lep Invariant Mass","val_m3l","m3l",50,0,250,"GeV",True],
#["Electron Pair Mass","val_mass1","M1",50,0,200,"GeV",True],
#["Muon pT","val_pTL3","pTL3",int(pt_bins[-1]/2),0,pt_bins[-1],"GeV",True],
#["Muon eta","val_etaL3","etaL3",60,-3.,3.,"eta",True], 
#["Muon phi","val_phiL3","phiL3",40,-4.,4.,"phi",True], 
#["Muon Isolation","val_IsoL3","IsoL3",50,0.,0.5,"pfRelIso03_all",True], 
#["Muon 3D Impact Parameter","val_ip3dL3","ip3dL3",25,0.,0.05,"IP3D",True], 
#["Muon Significance of 3D Impact Parameter","val_sip3dL3","sip3dL3",40,0.,4.,"SIP3D",True], 
#["3 Lep + MET Transverse Mass","val_mt","mt",50,0,300,"GeV",True],
#["Transverse Missing Energy","val_met","met",50,0,250,"GeV",True],
#["Transver Missing Energy Phi","val_met_phi","met_phi",40,-4,4,"phi",True],
#["Electron Pair Transverse Mass","val_M1T","M1T",100,0,200,"GeV",True],
#["Number of Electrons","val_nElec","nElectrons",6,0,6,"n",True],
#["Number of Leptons","val_nLep","nLeptons",6,0,6,"n",True],
#["Number of Good Leptons","val_nGoodLep","nGoodLeptons",6,0,6,"n",True],
#["3 Mu pT","val_m3l_pt","m3l_pt",75,0,150,"GeV",True],
#["dR Between Leading and Subleading","val_dR12","dR12",100,0,6,"dR",True],
#["dR Between Leading and Muon","val_dR13","dR13",100,0,6,"dR",True],
#["dR Between Subleading and Muon","val_dR23","dR23",100,0,6,"dR",True],
#["Muon mvaId","val_mvaIdL3","mvaIdL3",6,0,6,"ID",True],
#
#]
#
#xs, sumW = combXS(xs_sig,sumW_sig,xs_bkg,sumW_bkg)
#effs = {}
#for i in range(len(samples)):
#	tic = time.perf_counter()
#	print("Processing %s... "%(samples[i]),end='',flush=True)
#	if ("data" in samples[i]) or ("fake" in samples[i]):
#		weight = xs[samples[i]]/sumW[samples[i]]
#	else:
#		weight = xs[samples[i]]/sumW[samples[i]]*lumi
#	if "Wto3l" in samples[i]: sType = "sig"
#	elif "data" in samples[i]: sType = "data"
#	else: sType = "MC"	
#
#	print("Reading in ",end='',flush=True)
#	file = uproot.open(files[samples[i]])
#	events = file["passedEvents"]
#
#	vars_in = signal_vars
#	temp = events.arrays(vars_in)
#
#	data = {}
#	for key in temp: data[key.decode("utf-8")] = temp[key]
#	del temp
#	data["weight"] = weight
#	data["sType"] = sType
#	if not (("data" in samples[i]) or ("fake" in samples[i])):
#		data["pileupWeight"] = data["pileupWeight"]/32
#	#print("Processing %s with %i events"%(samples[i],len(data["nMuons"])))
#	print("%i events... "%(len(data["nMuons"])),end='',flush=True)
#
#	# Select other variables
#	print("Selecting Vars... ",end='',flush=True)
#	data = select(data)
#
#	# Perform Cuts
#	print("Skimming... ",end='',flush=True)
#	data["selection"],effs[samples[i]] = skim_val(data)
#	data["selection"],effs[samples[i]],data["fail"] = skim_flip(data,effs[samples[i]],samples[i])
#
#	print("Weighting... ",end='',flush=True)
#	data["fake_weight"] = Fake_weight(data,samples[i],fake_weight_b,fake_weight_e,pt_bins)
#	if "fake" in samples[i]: data["genWeight"] = data["genWeight"]*data["fake_weight"]*data["fail"]
#
#	# Save resulting data
#	print("Saving Results... ",end='',flush=True)
#	with open("/orange/avery/nikmenendez/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
#		pickle.dump(data, handle)
#	print("Done! ",end='',flush=True)
#	toc = time.perf_counter()
#	tot_time = toc-tic
#	if tot_time<60:
#		print("Total time was %.2f seconds"%(tot_time))
#	else:
#		print("Total time was %.2f minutes"%(tot_time/60))
#
#data = {}
#for i in range(len(samples)):
#	with open("/orange/avery/nikmenendez/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
#		data[samples[i]] = pickle.load(handle)
#
#print("Efficiencies of each cut:")
#cuts = ["Sample"]
#for key in effs[samples[0]]:
#	cuts.append(key)
#x = PrettyTable(cuts)
#for key in effs:
#	row = [key]
#	for key2 in effs[key]:
#		row.append("%.2f%%"%(effs[key][key2]))
#	x.add_row(row)
#table = open("/orange/avery/nikmenendez/Output/%s/Efficiency_Table.txt"%(out_dir),"w")
#table.write(x.get_string())
#table.close()
#print(x)
#
## Make Plots
#print("Generating Plots")
#for p in tqdm(plots):
#	plot(data,p,samples,error_on_MC,out_dir,True)




print("")
print('\a')
print("Uploading plots to web")
import subprocess
#print("scp -r /orange/avery/nikmenendez/Output/%s/ nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/ZpX/UL/"%(out_dir))
#print("scp -r /publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/ qguo@lxplus.cern.ch:/eos/user/q/qguo/www/Wto3l/SR_Selection/ZpX/UL/"%(out_dir))
print("scp -r qyguo@lxslc706.ihep.ac.cn://publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/ /eos/user/q/qguo/www/Wto3l/SR_Selection/ZpX/UL/Output/"%(out_dir))
print("cp /eos/user/q/qguo/www/Wto3l/SR_Selection/ZpX/UL/Output/index.php  /eos/user/q/qguo/www/Wto3l/SR_Selection/ZpX/UL/Output/%s/"%(out_dir))
#subprocess.run(["scp","-r","/orange/avery/nikmenendez/Output/%s/"%(out_dir),"nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/ZpX/UL/"])
#subprocess.run(["scp","-r","/orange/avery/nikmenendez/Output/%s/"%(out_dir),"nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/ZpX/UL/"])
#subprocess.run(["scp","-r","/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/"%(out_dir),"qguo@lxplus.cern.ch:/eos/user/q/qguo/www/Zprime/Wto3l/SR_Selection/ZpX/UL/"])
