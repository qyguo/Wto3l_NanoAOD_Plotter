import os
import numpy as np
import matplotlib.pyplot as plt

# c definition
#[  0  ,    1    ,        2       ,  3  , 4 , 5  , 6  ,    7    ]
#[Title,save name,variable plotted,nBins,low,high,unit,plot data]

def ROC(bkg,sig,c,out,plots,m):
	if not os.path.exists("/orange/avery/nikmenendez/Output/Optimize5/%s/"%(out)): os.makedirs("/orange/avery/nikmenendez/Output/Optimize5/%s/"%(out))

	#if m < 30:
	#	selection_bkg = ((bkg["M2"] <= m+(m*1.02)) & (bkg["M2"] >= m-(m*1.02)))
	#	selection_sig = ((sig["M2"] <= m+(m*1.02)) & (sig["M2"] >= m-(m*1.02)))
	#else:
	#	selection_bkg = ((bkg["M1"] <= m+(m*1.02)) & (bkg["M1"] >= m-(m*1.02)))
	#	selection_sig = ((sig["M1"] <= m+(m*1.02)) & (sig["M1"] >= m-(m*1.02)))

	selection_bkg = ((bkg["M1"] <= m+(m*1.02)) & (bkg["M1"] >= m-(m*1.02))) | ((bkg["M2"] <= m+(m*1.02)) & (bkg["M2"] >= m-(m*1.02)))
	selection_sig = ((sig["M1"] <= m+(m*1.02)) & (sig["M1"] >= m-(m*1.02))) | ((sig["M2"] <= m+(m*1.02)) & (sig["M2"] >= m-(m*1.02)))

	for key in bkg:
		if key=="weight" or key=="sType": continue
		bkg[key] = bkg[key][selection_bkg]
		sig[key] = sig[key][selection_sig]

	tot_bkg = np.sum(bkg["weight_arr"])
	tot_sig = np.sum(sig["weight_arr"])
	og_ratio = tot_sig/np.sqrt(tot_bkg)

	# Less than cut
	if not os.path.exists("/orange/avery/nikmenendez/Output/Optimize5/%s/%s</"%(out,c[1])): os.makedirs("/orange/avery/nikmenendez/Output/Optimize5/%s/%s</"%(out,c[1]))
	best_ratio = og_ratio
	best_cut = c[5]
	best_count, count = c[3]-1,0
	cut_values = np.arange(c[4],c[5],(c[5]-c[4])/c[3])

	nSigs, nBkgs, nRatio = [], [], []
	for i in cut_values:
		bkg_select = bkg[c[2]] <= i
		bkgN = np.sum(bkg["weight_arr"][bkg_select])

		sig_select = sig[c[2]] <= i
		sigN = np.sum(sig["weight_arr"][sig_select])
		
		ratio = sigN/np.sqrt(bkgN)
		if ratio > best_ratio:
			best_ratio = ratio
			best_cut = i
			best_count = count

		count += 1

		nSigs.append(sigN)
		nBkgs.append(bkgN)
		nRatio.append((sigN/np.sqrt(bkgN))/og_ratio)

	improvement = best_ratio/og_ratio

	plt.plot(cut_values,nRatio)
	plt.scatter(cut_values[best_count],nRatio[best_count],color='g',label="Best ratio at %s <= %.2f. %.2fx No Cut"%(c[2],best_cut,improvement))

	plt.xlabel("%s Cut Values (%s)"%(c[0],c[6]))
	plt.ylabel("nSignal / sqrt(nBackground) Improvement")
	plt.ylim(0,2)
	plt.legend(loc='best',fontsize='x-small')
	plt.title("Signal Separation for %s <= Cut"%(c[0]))
	plt.savefig("/orange/avery/nikmenendez/Output/Optimize5/%s/%s</cut_calc.png"%(out,c[1]))
	plt.clf()

	best_cut_lt = best_cut
	nRatio_lt = nRatio

	# Greater than cut
	if not os.path.exists("/orange/avery/nikmenendez/Output/Optimize5/%s/%s>/"%(out,c[1])): os.makedirs("/orange/avery/nikmenendez/Output/Optimize5/%s/%s>/"%(out,c[1]))
	best_ratio = og_ratio
	best_cut = c[4]
	best_count, count = 0,0
	cut_values = np.arange(c[4],c[5],(c[5]-c[4])/c[3])

	nSigs, nBkgs, nRatio = [], [], []
	for i in cut_values:
		bkg_select = bkg[c[2]] >= i
		bkgN = np.sum(bkg["weight_arr"][bkg_select])

		sig_select = sig[c[2]] >= i
		sigN = np.sum(sig["weight_arr"][sig_select])
		
		ratio = sigN/np.sqrt(bkgN)
		if ratio > best_ratio:
			best_ratio = ratio
			best_cut = i
			best_count = count

		count += 1

		nSigs.append(sigN)
		nBkgs.append(bkgN)
		nRatio.append((sigN/np.sqrt(bkgN))/og_ratio)

	improvement = best_ratio/og_ratio

	plt.plot(cut_values,nRatio)
	plt.scatter(cut_values[best_count],nRatio[best_count],color='g',label="Best ratio at %s >= %.2f. %.2fx No Cut"%(c[2],best_cut,improvement))

	plt.xlabel("%s Cut Values (%s)"%(c[0],c[6]))
	plt.ylabel("nSignal / sqrt(nBackground) Improvement")
	plt.ylim(0,2)
	plt.legend(loc='best',fontsize='x-small')
	plt.title("Signal Separation for %s >= Cut"%(c[0]))
	plt.savefig("/orange/avery/nikmenendez/Output/Optimize5/%s/%s>/cut_calc.png"%(out,c[1]))
	plt.clf()
	
	best_cut_gt = best_cut
	nRatio_gt = nRatio

	return best_cut_lt, best_cut_gt, nRatio_lt, nRatio_gt, cut_values, cut_values
