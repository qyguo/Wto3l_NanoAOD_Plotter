import numpy as np
import matplotlib.pyplot as plt

def ROC(bkg,sig,p,out):
	tot_bkg = np.sum(bkg["weight_arr"])
	tot_sig = np.sum(sig["weight_arr"])
	og_ratio = tot_sig/np.sqrt(tot_bkg)

	best_ratio = og_ratio
	best_cut = p[5]
	best_count, count = p[3]-1,0

	sig_effs, bkg_effs = [], []
	for i in np.arange(p[4],p[5],(p[5]-p[4])/p[3]):
		if p[7]: bkg_select = bkg[p[2]] < i
		else:    bkg_select = bkg[p[2]] > i
		bkgN = np.sum(bkg["weight_arr"][bkg_select])
		if p[7]: sig_select = sig[p[2]] < i
		else:    sig_select = sig[p[2]] > i
		sigN = np.sum(sig["weight_arr"][sig_select])
		
		ratio = sigN/np.sqrt(bkgN)
		if ratio > best_ratio:
			best_ratio = ratio
			best_cut = i
			best_count = count

		count += 1

		sig_effs.append(sigN/tot_sig)
		bkg_effs.append(bkgN/tot_bkg)

	improvement = best_ratio/og_ratio

	plt.plot(bkg_effs,sig_effs)
	if p[7]: plt.scatter(bkg_effs[best_count],sig_effs[best_count],color='g',label="Best ratio at %s < %.2f. %.2fx No Cut"%(p[2],best_cut,improvement))
	else:    plt.scatter(bkg_effs[best_count],sig_effs[best_count],color='g',label="Best ratio at %s > %.2f. %.2fx No Cut"%(p[2],best_cut,improvement))
	plt.plot([0,1],'--')

	plt.xlabel("Background Efficiency")
	plt.ylabel("Signal Efficiency")
	plt.ylim(0,1)
	plt.xlim(0,1)
	plt.legend(loc='best',fontsize='x-small')
	plt.title("ROC Curve for %s Cut"%(p[0]))
	plt.savefig("/home/nikmenendez/Output/ROC/%s/%s.png"%(out,p[1]))
	plt.clf()

	return best_ratio, best_cut
