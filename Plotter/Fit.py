import numpy as np

def SigFit(data,sample):

	for s in sample:
		if not ("Wto3l" in s):
			continue
		
		["Lower Mass diMu Pair" ,"mass2","M2",76,3.5,80.5,"GeV",True]

		fit_window = 0.05
		yie_window = 0.02
		split = 42

		mass = float(s.partition("_M")[2])
		fit_min = mass - mass*fit_window
		fit_max = mass + mass*fit_window
		yie_min = mass - mass*yie_window
		yie_max = maxx + maxx*yie_window
			
		if mass>=split: M = "M1"
		else:			M = "M2"

		fit_sel = (data[s][data[s]["selection"]]*(data[s][M]>fit_min)) & (data[s][data[s]["selection"]]*(data[s][M]<fit_max))
		yie_sel = (data[s][data[s]["selection"]]*(data[s][M]>yie_min)) & (data[s][data[s]["selection"]]*(data[s][M]<yie_max))
		to_fit = data[s][M][fit_sel]
		to_yie = data[s][M][yie_sel]




