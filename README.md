# Wto3l NanoAOD Plotter

Framework for cutting and plotting nanoAOD ntuples.

# Datasets

Define the datasets you want to run over in the datasets folder. Within datasets are directories for year and signalMC. Within year are files for data and MC background. Define any new datasets using the current ones as examples.

# Cuts

Cuts are defined in Skimmer/AnalysisSkimmer.py. Define each cut as:
```python
  selection, eff["Cut Name"] = cut(data["Cut variable"] < cut, selection)
```
This will record the efficiency of the cut and save all the efficiencies into a table.

Additional variables are defined in Skimmer/ZSelector.py. Here operations can be performed on data to create new variables or modify existing ones. It is recommended to perform vectorized operations on the numpy arrays as for loops will be slow.

# Plotting

All the plotting settings are chosen in make_plots.py. Here are the settings to modify:
1) samples: include the samples you want plotted
2) error_on_MC: True if you want error bars on MC. False otherwise.
3) out_dir: Name of the directory you want to export plots to
4) plots: Define each plot you want created in the format
```python
["Title","file name","variable",nBins,low,high,"Unit",include data True or False]
```
5) web upload: Last line uploads plots to my personal CERN webpage. Change this to upload it to yours or remove it.

# Running

After everything is defined as you want:

```bash
source setup_hpg.sh
python make_plots.py
```
