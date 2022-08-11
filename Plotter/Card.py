import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def card(data,p,s,e,out,pRatio,datacard):

	m_1 = np.arange(4,15,.02)
	m_2 = np.arange(15,25,.05)
	m_3 = np.arange(25,55,.1)
	m_4 = np.arange(55,70.1,.2)
	masses = np.concatenate((m_1,m_2,m_3,m_4),axis=None)

	data_out = open("DataCards/data_out_%s.txt"%(p[1]),"w")
	
	data_out.write("mass")
	for m in masses:
		data_out.write(",%.2f"%(m))
	data_out.write("\n")

	for i in range(len(s)):
		sel = data[s[i]]["selection"]
		sel_og2 = data[s[i]]["fail2"]
		to_plot = data[s[i]][p[2]][sel]
		weight_arr = data[s[i]]["eventWeight"][sel]

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
			weight_arr2 = data[s[i]]["eventWeight"][sel_og2]

		y = np.array([])
		for m in masses:
			low = m - m*.02
			high = m + m*.02

			in_range = (to_plot>=low) & (to_plot<=high)
			counts = np.sum(in_range*weight_arr)

			if "fake" in s[i]:
				WZ_in_range = (WZ_plot >=low) & (WZ_plot <=high)
				WZ_in_range2= (WZ_plot2>=low) & (WZ_plot2<=high)
				WZ_counts = np.sum(WZ_in_range *WZ_weight )
				WZ_counts2= np.sum(WZ_in_range2*WZ_weight2)

				ZZ_in_range = (ZZ_plot >=low) & (ZZ_plot <=high)
				ZZ_in_range2= (ZZ_plot2>=low) & (ZZ_plot2<=high)
				ZZ_counts = np.sum(ZZ_in_range *ZZ_weight )
				ZZ_counts2= np.sum(ZZ_in_range2*ZZ_weight2)

				DY_in_range = (DY_plot >=low) & (DY_plot <=high)
				DY_in_range2= (DY_plot2>=low) & (DY_plot2<=high)
				DY_counts = np.sum(DY_in_range *DY_weight )
				DY_counts2= np.sum(DY_in_range2*DY_weight2)

				in_range2 = (to_plot2>=low) & (to_plot2<=high)
				counts2 = np.sum(in_range2*weight_arr2)

				counts = counts - WZ_counts - ZZ_counts - DY_counts - counts2 + WZ_counts2 + ZZ_counts2 + DY_counts2 

			y = np.append(y,counts)

		data_out.write("%s"%(s[i]))
		for x in y:
			data_out.write(",%f"%(x))
		data_out.write("\n")

	data_out.close()

