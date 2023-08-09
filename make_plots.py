from __future__ import division
import sys
#sys.path.append('/afs/ihep.ac.cn/users/q/qyguo/.local/lib/python3.8/site-packages')
#sys.path.append('')
import numpy as np
import uproot
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


#Define parameters from plotting
samples = background_samples + ["data"]
files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)

lumi = 41.4*1000
error_on_MC = False

out_dir = "2e_ptCheck_allId"
#if not os.path.exists("/orange/avery/nikmenendez/Output/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/Output/%s/"%(out_dir))
#if not os.path.exists("/orange/avery/nikmenendez/Output/pickle/%s/"%(out_dir)): os.makedirs("/orange/avery/nikmenendez/Output/pickle/%s/"%(out_dir))
if not os.path.exists("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/"%(out_dir)): os.makedirs("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/"%(out_dir))
if not os.path.exists("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/"%(out_dir)): os.makedirs("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/"%(out_dir))

plots = [

# 1D Plots
#[Title,save name,variable plotted,nBins,low,high,unit,plot data]
["3 Lep Invariant Mass","m3l","m3l",50,0,200,"GeV",True],
["3 Lep + MET Transverse Mass","mt","mt",50,0,300,"GeV",True],
["Electron Pair Mass","mass1","M1",50,0,200,"GeV",True],
["Leading e pT","pTL1","pTL1",50,0,100,"GeV",True],
["Subleading e pT","pTL2","pTL2",50,0,100,"GeV",True],
["Muon pT","pTL3","pTL3",30,0,60,"GeV",True],
["Leading e eta","etaL1","etaL1",60,-3.,3.,"eta",True],
["Subleading e eta","etaL2","etaL2",60,-3.,3.,"eta",True],
["Muon eta","etaL3","etaL3",60,-3.,3.,"eta",True],
["Leading e phi","phiL1","phiL1",40,-4.,4.,"phi",True],
["Subleading e phi","phiL2","phiL2",40,-4.,4.,"phi",True],
["Muon phi","phiL3","phiL3",40,-4.,4.,"phi",True],
["Leading e Isolation","IsoL1","IsoL1",50,0.,1.0,"pfRelIso03_all",True],
["Subleading e Isolation","IsoL2","IsoL2",50,0.,1.0,"pfRelIso03_all",True],
["Muon Isolation","IsoL3","IsoL3",50,0.,1.0,"pfRelIso03_all",True],
["Leading e 3D Impact Parameter","ip3dL1","ip3dL1",25,0.,0.05,"IP3D",True],
["Subleading e 3D Impact Parameter","ip3dL2","ip3dL2",25,0.,0.05,"IP3D",True],
["Muon 3D Impact Parameter","ip3dL3","ip3dL3",25,0.,0.05,"IP3D",True],
["Leading e Significance of 3D Impact Parameter","sip3dL1","sip3dL1",40,0.,4.,"SIP3D",True],
["Subleading e Significance of 3D Impact Parameter","sip3dL2","sip3dL2",40,0.,4.,"SIP3D",True],
["Muon Significance of 3D Impact Parameter","sip3dL3","sip3dL3",40,0.,4.,"SIP3D",True],
["Transverse Missing Energy","met","met",50,0,250,"GeV",True],
["Transver Missing Energy Phi","met_phi","met_phi",40,-4,4,"phi",True],
["dR Between Leading e and Subleading e","dR12","dR12",100,0,6,"dR",True],
["dR Between Leading e and Muon","dR13","dR13",100,0,6,"dR",True],
["dR Between Subleading e and Muon","dR23","dR23",100,0,6,"dR",True],
["Muon MediumId","medIdL3","medIdL3",2,0,2,"Fail/Pass",True],
["Muon mvaId","mvaIdL3","mvaIdL3",6,0,6,"ID",True],
["Muon softId","softIdL3","softIdL3",2,0,2,"ID",True],
["Number of Good Muons","nGoodMuons","nGoodMuons",5,0,5,"n",True],
["Number of Leptons","nLeptons","nLeptons",7,0,7,"n",True],
["Number of b jets","nbJets","nbJets",5,0,5,"n",True],

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
	data = events.arrays(vars_in, library="np")
	#for key in temp: data[key.decode("utf-8")] = temp[key]
	del temp
	#data["weight"] = weight
	#data["sType"] = sType
	data["weight"] = np.array([weight]*len(data["nMuons"]))
	data["sType"] = np.array([sType]*len(data["nMuons"]))
	if "data" not in samples[i]:
		data["pileupWeight"] = data["pileupWeight"]/32
	print("Processing %s with %i events"%(samples[i],len(data["nMuons"])))

	# Select other variables
	data = select(data)

	# Perform Cuts
	data["selection"],effs[samples[i]],data["selection_fail"],data["selection_pass"] = skim(data)

	# Save resulting data
	#with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
	with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/%s.p"%(out_dir,samples[i]),'wb') as handle:
		pickle.dump(data, handle)

data = {}
for i in range(len(samples)):
	#with open("/orange/avery/nikmenendez/Output/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
	with open("/publicfs/cms/data/hzz/guoqy/Zprime/results/pickle/%s/%s.p"%(out_dir,samples[i]),'rb') as handle:
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
#table = open("/orange/avery/nikmenendez/Output/%s/Efficiency_Table.txt"%(out_dir),"w")
table = open("/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/Efficiency_Table.txt"%(out_dir),"w")
table.write(x.get_string())
table.close()
print(x)


# Make Plots
print("Generating Plots")
for p in tqdm(plots):
	if "data" in samples:
		plot(data,p,samples,error_on_MC,out_dir,True)
	else:
		plot(data,p,samples,error_on_MC,out_dir,False)

print('\a')
print("Uploading plots to web")
import subprocess
#print("scp -r /orange/avery/nikmenendez/Output/%s/ nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/ZpX/UL/"%(out_dir))
print("scp -r /publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/ qguo@lxplus.cern.ch:/eos/user/q/qguo/www/Zprime/Wto3l/SR_Selection/ZpX/UL/"%(out_dir))
#subprocess.run(["scp","-r","/orange/avery/nikmenendez/Output/%s/"%(out_dir),"nimenend@lxplus.cern.ch:/eos/user/n/nimenend/www/Wto3l/SR_Selection/ZpX/UL/"])
subprocess.run(["scp","-r","/publicfs/cms/data/hzz/guoqy/Zprime/results/Output/%s/"%(out_dir),"qguo@lxplus.cern.ch:/eos/user/q/qguo/www/Zprime/Wto3l/SR_Selection/ZpX/UL/"])
