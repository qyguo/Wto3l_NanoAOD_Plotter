from __future__ import division

import os
os.environ['KERAS_BACKEND']='tensorflow'

#import tensorflow
#from tensorflow.python.keras.models import Sequential, Model
#from tensorflow.python.keras.layers import Input, Activation, Dense, Convolution2D, MaxPooling2D, Dropout, Flatten, LeakyReLU, ReLU
#from tensorflow.python.keras.utils import np_utils
#from tensorflow.python.keras.optimizers import TFOptimizer
from tensorflow import keras

from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dense, Dropout, ReLU
from keras.utils import np_utils
from tensorflow.keras.optimizers import Adam

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import pandas as pd
import numpy as np
import uproot

from Utils.combXS import *
from Datasets.Signal.Wto3l import *
from Datasets.Run2017.Data import *
from Datasets.Run2017.Background import *
from Skimmer.AnalysisSkimmer import *
from Skimmer.ZSelector import *

samples = background_samples + signal_samples
files = combFiles(signal_samples, background_samples, data_samples, signal_files, background_files, data_files)
xs, sumW = combXS(xs_sig,sumW_sig,xs_bkg,sumW_bkg)
lumi = 41.4*1000

vars_test = ["dxyL1", "dzL1", "etaL1", "ip3dL1", "phiL1", "sip3dL1",
			 "dxyL2", "dzL2", "etaL2", "ip3dL2", "phiL2", "sip3dL2",
			 "dxyL3", "dzL3", "etaL3", "ip3dL3", "phiL3", "sip3dL3",
			 "dR12", "dR13", "dR23", "dRM0", "m3l", "mt", "met", "met_phi", "nJets",
			 "M0", "m3l_pt"]
vars_check = ["sType"]

effs = {}
events = pd.DataFrame()
for i in range(len(samples)):
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
	data["pileupWeight"] = data["pileupWeight"]/32
	data["Weights"] = weight * data["pileupWeight"] * data["genWeight"]
	print("Processing %s with %i events"%(samples[i],len(data["nMuons"])))

	# Select other variables
	data = select(data)

	# Perform Cuts
	data["selection"],effs[samples[i]],data["fail"],data["fail2"] = skim(data,samples[i])

	df = pd.DataFrame.from_dict(data)
	df = df[df["selection"]]
	df = df[vars_test+vars_check+["Weights"]]
	events = pd.concat([events,df])

#Shuffle DF and split into training and testing

events = shuffle(events)
events = events.reset_index(drop=True)
events_train, events_test = train_test_split(events, test_size=0.33, random_state=123456)

# early stopping callback
from keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='val_loss', patience=10)

# model checkpoint callback
# this saves our model architecture + parameters into dense_model.h5
from keras.callbacks import ModelCheckpoint
model_checkpoint = ModelCheckpoint('dense_model.h5', monitor='val_loss', 
                                  verbose=0, save_best_only=True, 
                                  save_weights_only=False, mode='auto', 
                                  period=1)

# Plot Classifier Output

def plot_classifier_output():

    print('... drawing discriminator output')
    
    sig_train = events_train[events_train.sType == 1][vars_test]
    bkg_train = events_train[events_train.sType == 0][vars_test]
    
    sig_test  = events_test[events_test.sType == 1][vars_test]
    bkg_test  = events_test[events_test.sType == 0][vars_test]

    ## these are already normalised to unity
    weights_sig_train = events_train[events_train.sType == 1]['Weights']
    weights_bkg_train = events_train[events_train.sType == 0]['Weights']    
    
    weights_sig_test  = events_test[events_test.sType == 1]['Weights']
    weights_bkg_test  = events_test[events_test.sType == 0]['Weights']

    ## but before the splitting, so re-normalise
    weights_sig_train = weights_sig_train.multiply(1./weights_sig_train.sum())
    weights_bkg_train = weights_bkg_train.multiply(1./weights_bkg_train.sum())
    
    weights_sig_test = weights_sig_test.multiply(1./weights_sig_test.sum())
    weights_bkg_test = weights_bkg_test.multiply(1./weights_bkg_test.sum())

    #if n_classses > 2 sig proba is the last one (in the way the code is written) 
    Y_pred_sig_train = model.predict(sig_train)[:,0]
    Y_pred_bkg_train = model.predict(bkg_train)[:,0]
    Y_pred_sig_test  = model.predict(sig_test)[:,0]
    Y_pred_bkg_test  = model.predict(bkg_test)[:,0]

    # This will be the min/max of our plots
    c_max = max(np.max(d) for d in np.concatenate([Y_pred_sig_train,Y_pred_bkg_train,Y_pred_sig_test,Y_pred_bkg_test]))
    c_min = min(np.min(d) for d in np.concatenate([Y_pred_sig_train,Y_pred_bkg_train,Y_pred_sig_test,Y_pred_bkg_test]))

    # Get histograms of the classifiers
    Histo_training_S = np.histogram(Y_pred_sig_train,bins=40,range=(c_min,c_max),weights=weights_sig_train)
    Histo_training_B = np.histogram(Y_pred_bkg_train,bins=40,range=(c_min,c_max),weights=weights_bkg_train)
    Histo_testing_S = np.histogram(Y_pred_sig_test,bins=40,range=(c_min,c_max),weights=weights_sig_test)
    Histo_testing_B = np.histogram(Y_pred_bkg_test,bins=40,range=(c_min,c_max),weights=weights_bkg_test)
    
    # Lets get the min/max of the Histograms
    AllHistos = [Histo_training_S,Histo_training_B,Histo_testing_S,Histo_testing_B]
    h_max     = max([histo[0].max() for histo in AllHistos])*1.2
    h_min     = min([histo[0].min() for histo in AllHistos])
    
    # Get the histogram properties (binning, widths, centers)
    bin_edges = Histo_training_S[1]
    bin_centers = ( bin_edges[:-1] + bin_edges[1:]  ) /2.
    bin_widths = (bin_edges[1:] - bin_edges[:-1])
    
    # To make error bar plots for the data, take the Poisson uncertainty sqrt(N)
    ErrorBar_testing_S = np.sqrt(Histo_testing_S[0]/Y_pred_sig_test.size)
    ErrorBar_testing_B = np.sqrt(Histo_testing_B[0]/Y_pred_bkg_test.size)
    
    plt.clf() 
    # Draw objects
    ax1 = plt.subplot(111)
    
    # Draw solid histograms for the training data
    ax1.bar(bin_centers-bin_widths/2.,Histo_training_S[0],facecolor='blue',linewidth=0,width=bin_widths,label='S (Train)',alpha=0.5)
    ax1.bar(bin_centers-bin_widths/2.,Histo_training_B[0],facecolor='red',linewidth=0,width=bin_widths,label='B (Train)',alpha=0.5)
    
    # # Draw error-bar histograms for the testing data
    ax1.errorbar(bin_centers, Histo_testing_S[0], yerr=ErrorBar_testing_S, xerr=None, ecolor='blue',c='blue',fmt='o',label='S (Test)')
    ax1.errorbar(bin_centers, Histo_testing_B[0], yerr=ErrorBar_testing_B, xerr=None, ecolor='red',c='red',fmt='o',label='B (Test)')
    
    # Make a colorful backdrop to show the clasification regions in red and blue
    ax1.axvspan(0.5, c_max, color='blue',alpha=0.08)
    ax1.axvspan(c_min,0.5, color='red',alpha=0.08)

    # Adjust the axis boundaries (just cosmetic)
    ax1.axis([c_min, c_max, h_min, h_max])

    # Make labels and title
    plt.title("Classification with scikit-learn")
    plt.xlabel("Classifier output")
    plt.ylabel("Normalized Yields")
    
    # Make legend with smalll font
    legend = ax1.legend(loc='upper center', shadow=True,ncol=2)
    for alabel in legend.get_texts():
        alabel.set_fontsize('small')

    # Save the result to png
    plt.savefig("nn_score_output.png")

#Create model

inputs = Input(shape=(len(vars_test),), name = 'input')
#x = Dropout(.1, name = 'input_dropout_.2')(inputs)
x = Dense(64, name = 'hidden1', activation="ReLU")(inputs)
#x = Dropout(.1, name = 'hidden1_dropout_.1')(x)
x = Dense(32, name = 'hidden2', activation="ReLU")(x)
#x = Dropout(.1, name = 'hidden2_dropout_.1')(x)
#x = LeakyReLU(.1, name = 'LeakyReLU1_.1')(x)
#x = ReLU(name = 'ReLU1')(x)
outputs = Dense(1, name = 'output', activation='sigmoid')(x)

model = Model(inputs=inputs, outputs=outputs)
#opt = keras.optimizers.Adam(learning_rate=0.0001)
#opt = Adam(learning_rate=0.0002, beta_1=0.5, epsilon=0.001)
opt = Adam()
model.compile(opt, loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

history = model.fit(events_train[vars_test],
                    events_train[vars_check],
                    epochs=20,
                    batch_size=256,
                    sample_weight = events_train['Weights'].values,
                    verbose=1,
                    #callbacks=[early_stopping], 
                    validation_split=0.25)

import matplotlib.pyplot as plt
# plot loss vs epoch
plt.figure(figsize=(15,10))
ax = plt.subplot(2, 2, 1)
ax.plot(history.history['loss'], label='loss')
ax.plot(history.history['val_loss'], label='val_loss')
ax.legend(loc="upper right")
ax.set_xlabel('epoch')
ax.set_ylabel('loss')

# plot accuracy vs epoch
ax = plt.subplot(2, 2, 2)
ax.plot(history.history['accuracy'], label='acc')
ax.plot(history.history['val_accuracy'], label='val_acc')
ax.legend(loc="upper left")
ax.set_xlabel('epoch')
ax.set_ylabel('acc')

plt.savefig("loss_acc.png")

plot_classifier_output()

results = model.evaluate(events_test[vars_test], events_test[vars_check])
print(results)

#Save model
model.save("ZSelector_model_alt.h5")
