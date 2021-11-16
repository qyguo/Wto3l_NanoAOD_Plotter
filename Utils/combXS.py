def combXS(xs_sig,sumW_sig,xs_bkg,sumW_bkg):
	xs, sumW = {}, {}
	for s in xs_sig:
		xs[s] = xs_sig[s]
		sumW[s] = sumW_sig[s]
	for s in xs_bkg:
		xs[s] = xs_bkg[s]
		sumW[s] = sumW_bkg[s]

	xs["data"] = 1
	sumW["data"] = 1
	xs["fake"] = 1
	sumW["fake"] = 1

	return xs, sumW

def combFiles(sig,bkg,data,sig_file,bkg_file,data_file):
	files = {}
	for s in sig:
		files[s] = sig_file[s]
	for b in bkg:
		files[b] = bkg_file[b]
	for d in data:
		files[d] = data_file[d]

	return files

