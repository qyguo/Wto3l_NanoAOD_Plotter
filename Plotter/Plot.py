import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def plot(data,p,s,e,out,pRatio,datacard):

	# Sort Samples by Amount of Statistics
	stats = []
	nSig,nData = 0,0
	#for i in range(len(s)):
	#	if data[s[i]]["sType"]=="MC":
	#		stats.append(len(data[s[i]][p[2]][data[s[i]]["selection"]]))
	#	elif data[s[i]]["sType"]=="sig":
	#		nSig+=1
	#	else:
	#		nData+=1

	#s_sorted = [x for _,x in sorted(zip(stats,s[:-(nSig+nData)]))]
	#s_sorted.reverse()
	#s = s_sorted + s[-(nSig+nData):]
	#if not p[7]: s.remove("data")

	# Make Plot

	if pRatio and p[7]:
		fig = plt.figure(constrained_layout=False,figsize=(10,13),)
		gs = fig.add_gridspec(10,1)
		ax1 = fig.add_subplot(gs[:7,:])
		ax2 = fig.add_subplot(gs[7:,:])
	else:
		fig = plt.figure(constrained_layout=False,figsize=(10,7),)
		ax1 = fig.add_subplot()
		

	if datacard: data_out = open("DataCards/data_out_%s.txt"%(p[1]),"w")
	last, data_made, MC_error, data_error = 0,[],0,0
	tot_data, tot_MC, err_data, err_MC = 0, 0, 0, 0
	for i in range(len(s)):
		if (not p[7]) and ("data" in s[i]): continue
		sel = data[s[i]]["selection"]
		sel_og2 = data[s[i]]["fail2"]
		#to_plot = data[s[i]][p[2]][data[s[i]]["selection"]]
		to_plot = data[s[i]][p[2]][sel]
		#weight_arr = data[s[i]]["weight"]*data[s[i]]["genWeight"][data[s[i]]["selection"]]*data[s[i]]["pileupWeight"][data[s[i]]["selection"]]
		weight_arr = data[s[i]]["eventWeight"][sel]
		y,binEdges = np.histogram(to_plot,bins=p[3],range=(p[4],p[5]))
		hidden_error = np.sqrt(np.abs(y))*data[s[i]]["weight"]
		if e or data[s[i]]["sType"]=="data":
			error = hidden_error
			count = len(weight_arr)
			tot_data = np.sum(weight_arr)
			count_err = np.sqrt(count)
			err_data = np.sqrt(tot_data)
		elif data[s[i]]["sType"]=="MC": 
			error = 0
			if not ("fake" in s[i]):
				count = len(weight_arr)*data[s[i]]["weight"]
				count_w = np.sum(weight_arr)
				tot_MC += np.sum(weight_arr)
				if len(weight_arr)>0:
					count_err = np.sqrt(len(weight_arr))*np.average(weight_arr)
				else:
					count_err = 0
				count_err_w = np.sqrt(np.sum(weight_arr))
				#err_MC += np.sqrt(np.sum(weight_arr))
				err_MC += count_err
		else:
			error = 0
			count_w = np.sum(weight_arr)
			count_err = np.sqrt(len(weight_arr))*np.average(weight_arr)
			
		y,binEdges = np.histogram(to_plot,bins=p[3],range=(p[4],p[5]),weights=weight_arr)
		bincenters = 0.5*(binEdges[1:]+binEdges[:-1])

		# Fake reweighting with WZ and ZZ
		if "fake" in s[i]:
			sam = "WZTo3LNu"
			sel_fail, sel_fail2 = data[sam]["fail"], data[sam]["fail2"]
			WZ_plot = data[sam][p[2]][sel_fail]
			WZ_weight = data[sam]["eventWeight"][sel_fail]
			WZ_plot2 = data[sam][p[2]][sel_fail2]
			WZ_weight2 = data[sam]["eventWeight"][sel_fail2]

			sam = "ZZTo4L"
			sel_fail, sel_fail2 = data[sam]["fail"], data[sam]["fail2"]
			ZZ_plot = data[sam][p[2]][sel_fail]
			ZZ_weight = data[sam]["eventWeight"][sel_fail]
			ZZ_plot2 = data[sam][p[2]][sel_fail2]
			ZZ_weight2 = data[sam]["eventWeight"][sel_fail2]
			
			sam = "DYJetsToLL_M0To1"
			sel_fail, sel_fail2 = data[sam]["fail"], data[sam]["fail2"]
			DY_plot = data[sam][p[2]][sel_fail]
			DY_weight = data[sam]["eventWeight"][sel_fail]
			DY_plot2 = data[sam][p[2]][sel_fail2]
			DY_weight2 = data[sam]["eventWeight"][sel_fail2]

			to_plot2= data[s[i]][p[2]][sel_og2]
			to_weight2 = data[s[i]]["eventWeight"][sel_og2]
			
			yWZ, binEdges = np.histogram(WZ_plot,bins=p[3],range=(p[4],p[5]),weights=WZ_weight)
			yZZ, binEdges = np.histogram(ZZ_plot,bins=p[3],range=(p[4],p[5]),weights=ZZ_weight)
			yDY, binEdges = np.histogram(DY_plot,bins=p[3],range=(p[4],p[5]),weights=DY_weight)
			
			yWZ2, binEdges = np.histogram(WZ_plot2,bins=p[3],range=(p[4],p[5]),weights=WZ_weight2)
			yZZ2, binEdges = np.histogram(ZZ_plot2,bins=p[3],range=(p[4],p[5]),weights=ZZ_weight2)
			yDY2, binEdges = np.histogram(DY_plot2,bins=p[3],range=(p[4],p[5]),weights=DY_weight2)

			y2, binEdges = np.histogram(to_plot2,bins=p[3],range=(p[4],p[5]),weights=to_weight2)

			#For 3P0F Validation
			y = y - yWZ - yZZ - yDY - y2 + yWZ2 + yZZ2 + yDY2
			y = [0 if x<0 else x for x in y]
			count_w = np.sum(weight_arr) - np.sum(WZ_weight) - np.sum(ZZ_weight) - np.sum(DY_weight) - np.sum(to_weight2) + np.sum(WZ_weight2) + np.sum(ZZ_weight2) + np.sum(DY_weight2)
			count_err += np.sqrt(len(weight_arr))*np.average(weight_arr) + np.sqrt(len(WZ_weight))*np.average(WZ_weight) + np.sqrt(len(ZZ_weight))*np.average(ZZ_weight) + np.sqrt(len(DY_weight))*np.average(DY_weight) + np.sqrt(len(to_weight2))*np.average(to_weight2) + np.sqrt(len(WZ_weight2))*np.average(WZ_weight2) + np.sqrt(len(ZZ_weight2))*np.average(ZZ_weight2) + np.sqrt(len(DY_weight2))*np.average(DY_weight2)

			#For 2P1F Validation
			#y = y - yWZ2 - yZZ2
			#count_w = np.sum(weight_arr) - np.sum(WZ_weight2) - np.sum(ZZ_weight2)
			#count_err += np.sqrt(len(weight_arr))*np.average(weight_arr) + np.sqrt(len(WZ_weight2))*np.average(WZ_weight2) + np.sqrt(len(ZZ_weight2))*np.average(ZZ_weight2)

			tot_MC += count_w
			err_MC += count_err

		if data[s[i]]["sType"]=="MC":
			ax1.bar(bincenters,y,yerr=error,bottom=last,width=binEdges[1]-binEdges[0],label='%s: %.2f +- %.2f'%(s[i],count_w,count_err))
			last += y
			MC_error += hidden_error
			ys = [str(j) for j in y]
			if datacard: data_out.write("%s,%s\n"%(s[i],",".join(ys)))
		elif data[s[i]]["sType"]=="sig":
			ax1.errorbar(bincenters,y,yerr=error,drawstyle='steps-mid',label='%s: %.2f +- %.2f'%(s[i],count_w,count_err))
			ys = [str(j) for j in y]
			if datacard: data_out.write("%s,%s\n"%(s[i],",".join(ys)))
		else:
			ax1.errorbar(bincenters,y,yerr=error,drawstyle='steps-mid',fmt="o",color='black',label='%s: %i +- %.2f'%(s[i],tot_data,err_data))
			data_made = y
			data_error = hidden_error
			ys = [str(j) for j in y]
			if datacard: data_out.write("%s,%s\n"%(s[i],",".join(ys)))

	if datacard: data_out.close()
	ax1.set_xlabel("%s (%s)"%(p[0],p[6]),size='x-large')
	ax1.set_ylabel("Number of Events",size='x-large')
	ax1.set_ylim(bottom=0)
	ax1.set_xlim(p[4],p[5])
	if len(p)>8:
		if p[8]=='log': ax1.set_yscale('symlog')
	ax1.legend(loc='best',fontsize='x-small')

	if pRatio and p[7]:
		if len(data_made)>0 and len(last) > 0:
			ratio = data_made/last
			ratioErr = ratio*(data_error/data_made + MC_error/last)
			ax2.errorbar(bincenters,ratio,yerr=ratioErr,drawstyle='steps-mid',fmt="o",color='black')

			#tot_data = np.sum(data_made)
			#tot_MC = np.sum(last)
			dataMCratio = tot_data/tot_MC
			dataMCerror = dataMCratio*(err_MC/tot_MC + err_data/tot_data)
			ax1.text(0.0,1.0,'2017, Data/Pred = %.2f +- %.2f'%(dataMCratio,dataMCerror),size=15,transform = ax1.transAxes)
			

		ax2.set_xlabel("%s (%s)"%(p[0],p[6]),size='x-large')
		ax2.set_ylabel("Data/MC Ratio",size='x-large')
		ax2.set_ylim(bottom=0,top=2)
		ax2.set_xlim(p[4],p[5])
		start, end = ax2.get_ylim()
		ax2.yaxis.set_ticks(np.arange(start, end, 0.25))
		ax2.grid()
	else:
		ax1.text(0.0,1.0,'2017',size=15,transform = ax1.transAxes)


	fig.suptitle("%s"%(p[0]),size='xx-large')
	fig.savefig("/orange/avery/nikmenendez/Output/%s/%s.png"%(out,p[1]))
	fig.clf()
	plt.close(fig)
