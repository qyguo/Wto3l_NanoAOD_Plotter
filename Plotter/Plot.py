import numpy as np
import matplotlib.pyplot as plt

def plot(data,p,s,e):

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

	# Make Plot

	#fig = plt.figure(constrained_layout=False,figsize=(10,13),)
	#gs = fig.add_gridspec(10,1)
	#ax1 = fig.add_subplot(gs[:7,:])
	#ax2 = fig.add_subplot(gs[7:,:])

	last, data_made = 0,[]
	for i in range(len(s)):
		to_plot = data[s[i]][p[2]][data[s[i]]["selection"]]
		weight_arr = data[s[i]]["weight"]*data[s[i]]["genWeight"][data[s[i]]["selection"]]
		if e or data[s[i]]["sType"]=="data":
			y,binEdges = np.histogram(to_plot,bins=p[3],range=(p[4],p[5]),weights=weight_arr)
			error = np.sqrt(y)*data[s[i]]["weight"]
		else:
			error = 0
		y,binEdges = np.histogram(to_plot,bins=p[3],range=(p[4],p[5]),weights=weight_arr)
		bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
		if data[s[i]]["sType"]=="MC":
			plt.bar(bincenters,y,yerr=error,bottom=last,label='%s: %.2f'%(s[i],np.sum(y)))
			last += y
		elif data[s[i]]["sType"]=="sig":
			plt.errorbar(bincenters,y,yerr=error,drawstyle='steps-mid',label='%s: %.2f'%(s[i],np.sum(y)))
		else:
			plt.errorbar(bincenters,y,yerr=error,drawstyle='steps-mid',fmt="o",color='black',label='%s: %.2f'%(s[i],np.sum(y)))
			data_made = y

	plt.xlabel("%s (%s)"%(p[0],p[6]))
	plt.ylabel("Number of Events")
	plt.ylim(bottom=0)
	plt.title("%s"%(p[0]))
	plt.legend(loc='best',fontsize='x-small')
	plt.show()
	plt.clf()
