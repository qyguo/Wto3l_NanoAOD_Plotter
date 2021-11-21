import numpy as np
import matplotlib.pyplot as plt

def plot(data,p,s,e,out):

	# Sort Samples by Amount of Statistics
	stats = []
	nSig,nData = 0,0
	for i in range(len(s)):
		if data[s[i]]["sType"]=="MC":
			stats.append(len(data[s[i]][p[2]][data[s[i]]["selection"]]))
		elif data[s[i]]["sType"]=="sig":
			nSig+=1
		else:
			nData+=1

	s_sorted = [x for _,x in sorted(zip(stats,s[:-(nSig+nData)]))]
	s_sorted.reverse()
	s = s_sorted + s[-(nSig+nData):]
	if not p[7]: s = s[:-1]

	# Make Plot

	fig = plt.figure(constrained_layout=False,figsize=(10,13),)
	gs = fig.add_gridspec(10,1)
	ax1 = fig.add_subplot(gs[:7,:])
	ax2 = fig.add_subplot(gs[7:,:])

	last, data_made, MC_error, data_error = 0,[],0,0
	tot_data, tot_MC, err_data, err_MC = 0, 0, 0, 0
	for i in range(len(s)):
		to_plot = data[s[i]][p[2]][data[s[i]]["selection"]]
		weight_arr = data[s[i]]["weight"]*data[s[i]]["genWeight"][data[s[i]]["selection"]]*data[s[i]]["pileupWeight"][data[s[i]]["selection"]]
		y,binEdges = np.histogram(to_plot,bins=p[3],range=(p[4],p[5]))
		hidden_error = np.sqrt(np.abs(y))*data[s[i]]["weight"]
		if e or data[s[i]]["sType"]=="data":
			error = hidden_error
			tot_data = np.sum(weight_arr)
			err_data = np.sqrt(tot_data)
		elif data[s[i]]["sType"]=="MC":
			error = 0
			if not ("fake" in s[i]):
				tot_MC += np.sum(weight_arr)
				err_MC += np.sqrt(np.sum(weight_arr))
		else:
			error = 0
		y,binEdges = np.histogram(to_plot,bins=p[3],range=(p[4],p[5]),weights=weight_arr)
		bincenters = 0.5*(binEdges[1:]+binEdges[:-1])

		# Fake reweighting with WZ and ZZ
		if "fake" in s[i]:
			sam = "WZTo3LNu"
			WZ_plot = data[sam][p[2]][data[sam]["fail"]]
			WZ_weight = data[sam]["weight"]*data[sam]["genWeight"][data[sam]["fail"]]*data[sam]["pileupWeight"][data[sam]["fail"]]*data[sam]["fake_weight"][data[sam]["fail"]]
			WZ_weight2= data[sam]["weight"]*data[sam]["genWeight"][data[sam]["fail"]]*data[sam]["pileupWeight"][data[sam]["fail"]]*data[sam]["fake_weight"][data[sam]["fail"]]*data[sam]["fake_weight"][data[sam]["fail"]]
			sam = "ZZTo4L"
			ZZ_plot = data[sam][p[2]][data[sam]["fail"]]
			ZZ_weight = data[sam]["weight"]*data[sam]["genWeight"][data[sam]["fail"]]*data[sam]["pileupWeight"][data[sam]["fail"]]*data[sam]["fake_weight"][data[sam]["fail"]]
			ZZ_weight2= data[sam]["weight"]*data[sam]["genWeight"][data[sam]["fail"]]*data[sam]["pileupWeight"][data[sam]["fail"]]*data[sam]["fake_weight"][data[sam]["fail"]]*data[sam]["fake_weight"][data[sam]["fail"]]
			
			yWZ, binEdges = np.histogram(WZ_plot,bins=p[3],range=(p[4],p[5]),weights=WZ_weight)
			yZZ, binEdges = np.histogram(ZZ_plot,bins=p[3],range=(p[4],p[5]),weights=ZZ_weight)
			
			yWZ2, binEdges = np.histogram(WZ_plot,bins=p[3],range=(p[4],p[5]),weights=WZ_weight2)
			yZZ2, binEdges = np.histogram(ZZ_plot,bins=p[3],range=(p[4],p[5]),weights=ZZ_weight2)

			y = y - yWZ - yZZ
			tot_MC += np.sum(weight_arr) - np.sum(WZ_weight) - np.sum(ZZ_weight)
			err_MC += np.sqrt(np.sum(weight_arr)) + np.sqrt(np.sum(WZ_weight)) + np.sqrt(np.sum(ZZ_weight))

		if data[s[i]]["sType"]=="MC":
			ax1.bar(bincenters,y,yerr=error,bottom=last,width=binEdges[1]-binEdges[0],label='%s: %.2f'%(s[i],np.sum(y)))
			last += y
			MC_error += hidden_error
		elif data[s[i]]["sType"]=="sig":
			ax1.errorbar(bincenters,y,yerr=error,drawstyle='steps-mid',label='%s: %.2f'%(s[i],np.sum(y)))
		else:
			ax1.errorbar(bincenters,y,yerr=error,drawstyle='steps-mid',fmt="o",color='black',label='%s: %.2f'%(s[i],np.sum(y)))
			data_made = y
			data_error = hidden_error

	ax1.set_xlabel("%s (%s)"%(p[0],p[6]))
	ax1.set_ylabel("Number of Events")
	ax1.set_ylim(bottom=0)
	ax1.set_xlim(p[4],p[5])
	ax1.legend(loc='best',fontsize='x-small')

	if len(data_made)>0 and len(last) > 0:
		ratio = data_made/last
		ratioErr = ratio*(data_error/data_made + MC_error/last)
		ax2.errorbar(bincenters,ratio,yerr=ratioErr,drawstyle='steps-mid',fmt="o",color='black')

		#tot_data = np.sum(data_made)
		#tot_MC = np.sum(last)
		dataMCratio = tot_data/tot_MC
		dataMCerror = dataMCratio*(err_MC/tot_MC + err_data/tot_data)
		ax1.text(0.0,1.0,'Data/Pred = %.2f +- %.2f'%(dataMCratio,dataMCerror),size=20,transform = ax1.transAxes)
		

	ax2.set_xlabel("%s (%s)"%(p[0],p[6]))
	ax2.set_ylabel("Data/MC Ratio")
	ax2.set_ylim(bottom=0,top=2)
	ax2.set_xlim(p[4],p[5])
	start, end = ax2.get_ylim()
	ax2.yaxis.set_ticks(np.arange(start, end, 0.25))
	ax2.grid()


	fig.suptitle("%s"%(p[0]))
	fig.savefig("/home/nikmenendez/Output/%s/%s.png"%(out,p[1]))
	fig.clf()
	plt.close(fig)
