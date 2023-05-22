from __future__ import division

import os
import sys

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.utils import shuffle
import pandas as pd
import numpy as np
import uproot
import joblib

from Utils.combXS import *
from Datasets.Signal.Wto3l import *
from Datasets.Run2017.Data import *
from Datasets.Run2017.Background import *
from Skimmer.AnalysisSkimmer import *
from Skimmer.ZSelector import *
from Weighter.Fake_weight import *

#samples = background_samples + signal_samples
samples = ["WZTo3LNu","ZZTo4L","fake"] + signal_samples
files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)
xs, sumW = combXS(xs_sig,sumW_sig,xs_bkg,sumW_bkg)
lumi = 41.4*1000

#vars_test = ["dxyL1", "dzL1", "etaL1", "ip3dL1", "phiL1", "sip3dL1", 
#			 "dxyL2", "dzL2", "etaL2", "ip3dL2", "phiL2", "sip3dL2",
#			 "dxyL3", "dzL3", "etaL3", "ip3dL3", "phiL3", "sip3dL3",
#			 "dR12", "dR13", "dR23", "dRM0", "m3l", "mt", "met", "nJets",
#			 "M0", "m3l_pt"]
#vars_test = ["etaL1", "phiL1", 
#			 "etaL2", "phiL2",
#			 "etaL3", "phiL3",
#			 "dR12", "dR13", "dR23", "dRM0", "m3l", "mt", "met", "nJets",
#			 "M0", "m3l_pt"]
vars_test = [
			 "m3l", "mt", "met", "nJets",
			 "M0", "m3l_pt"]
vars_check = ["sType"]

effs = {}
#events = pd.DataFrame()
part = {}
for i in range(len(samples)):
	if ("data" in samples[i]) or ("fake" in samples[i]):
		weight = xs[samples[i]]/sumW[samples[i]]
	else:
		weight = xs[samples[i]]/sumW[samples[i]]*lumi
	if "Wto3l" in samples[i]: sType = 1
	else: sType = 0

	file = uproot.open(files[samples[i]])
	events_in = file["passedEvents"]

	vars_in = signal_vars
	temp = events_in.arrays(vars_in)

	data = {}
	for key in temp: data[key.decode("utf-8")] = temp[key]
	del temp
	#data["weight"] = weight
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
		data["genWeight"] = data["genWeight"]*data["fake_weight"]*data["fail"] + data["genWeight"]*data["fake_weight"]*data["fail2"]
		data["selection"] = data["fail"] | data["fail2"]

	data["Weights"] = weight * data["pileupWeight"] * data["genWeight"]
	df = pd.DataFrame.from_dict(data)
	df = df[df["selection"]]
	df = df[vars_test+vars_check+["Weights"]]
	part[samples[i]] = df
	#events = pd.concat([events,df])

	if ("WZ" in samples[i]) or ("ZZ" in samples[i]):
		data["fWeight"] = (data["fake_weight"]*data["fail"] + data["fake_weight"]*data["fail2"]) * (-1)
		data["Weights"] = data["Weights"] * data["fWeight"]
		data["selection"] = data["fail"] | data["fail2"]

		df = pd.DataFrame.from_dict(data)
		df = df[df["selection"]]
		df = df[vars_test+vars_check+["Weights"]]
		part["%s_fake"%(samples[i])] = df
		#events = pd.concat([events,df])

#Shuffle DF and split into training and testing
events_train, events_test = pd.DataFrame(), pd.DataFrame()
for s in samples:
	df_train, df_test = train_test_split(part[s], test_size=0.33, random_state=123456)
	events_train = pd.concat([events_train, df_train])
	events_test = pd.concat([events_test, df_test])
	if ("WZ" in s) or ("ZZ" in s):
		df_train, df_test = train_test_split(part["%s_fake"%(s)], test_size=0.33, random_state=123456)
		events_train = pd.concat([events_train, df_train])
		events_test = pd.concat([events_test, df_test])

events_train = shuffle(events_train)
events_train = events_train.reset_index(drop=True)
events_test = shuffle(events_test)
events_test = events_test.reset_index(drop=True)

## Normalize features
maxW = pd.concat([events_train["Weights"],events_test["Weights"]]).max()
minW = pd.concat([events_train["Weights"],events_test["Weights"]]).min()
events_train["Weights"] = (events_train["Weights"]-minW)/(maxW-minW)
events_test["Weights"] = (events_test["Weights"]-minW)/(maxW-minW)
#maxW = pd.concat([events_train,events_test]).max()
#minW = pd.concat([events_train,events_test]).min()
#events_train = (events_train-minW)/(maxW-minW)
#events_test = (events_test-minW)/(maxW-minW)
#
#maxW.to_pickle("maxes.pkl")
#minW.to_pickle("mins.pkl")

# Import Random Forest Model
from sklearn.ensemble import RandomForestClassifier

# Create a Guassian Classifier
clf = RandomForestClassifier(n_estimators=100)

# Train the model using the training sets
clf.fit(events_train[vars_test],events_train[vars_check],sample_weight=events_train["Weights"])

# Save and import model
joblib.dump(clf, "forest_model.joblib")

rf = joblib.load("forest_model.joblib")

# Predict
y_pred = rf.predict(events_test[vars_test])

# Import metrics for accuracy calculation
from sklearn import metrics

# Model accuracy
print("Accuracy:",metrics.accuracy_score(events_test[vars_check], y_pred, sample_weight=events_test["Weights"]))

feature_imp = pd.Series(rf.feature_importances_,index=vars_test).sort_values(ascending=False)
print(feature_imp)

import matplotlib.pyplot as plt
#import seaborn as sns
# Creating a bar plot
plt.barh(feature_imp.index, feature_imp)
# Add labels to your graph
plt.xlabel('Feature Importance Score')
plt.ylabel('Features')
plt.title("Visualizing Important Features")
plt.legend()
plt.savefig("forest_var_dist.png")
