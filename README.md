![](figures/powerdata-view_banner_dark.png#gh-dark-mode-only)
![](figures/powerdata-view_banner_light.png#gh-light-mode-only)
An open-source statistical analysis tool for power grid datasets.

# Content

This tool was designed to compare power grid datasets, by generating histograms, boxplots, correlation plots,
and statistics table. 
It is compatible with datasets generated using powerdata-gen.

| ![](figures/bus-voltage-pu_boxplot_dark.png#gh-dark-mode-only) ![](figures/bus-voltage-pu_boxplot_light.png#gh-light-mode-only) |            ![](figures/bus-voltage-pu_grid_dark.png#gh-dark-mode-only) ![](figures/bus-voltage-pu_grid_light.png#gh-light-mode-only)            |
|:--------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------:|
| ![](figures/bus-voltage-pu_dark.png#gh-dark-mode-only) ![](figures/bus-voltage-pu_light.png#gh-light-mode-only)                 | ![](figures/snapshots-with-illicit-voltage_dark.png#gh-dark-mode-only) ![](figures/snapshots-with-illicit-voltage_light.png#gh-light-mode-only) |

# Installation

First, you need to clone the repository :
```
git clone https://github.com/bdonon/powerdata_view.git
```
Then, go inside the project :
```
cd powerdata_view
```

## Virtual Environment
It is usually a good practice to have a virtual environment per project, so that any package installation that 
you do for one project will not alter the others.
There are multiple ways of creating a virtual environment (virtualenv, conda or even your IDE).

In the following, we guide you through the creation of a virtual environment using the package virtualenv :
```
pip install virtualenv
virtualenv venv -p python3.10
```
Then, you need to activate the virtual environment :
```
source venv/bin/activate
```

## Installing dependencies

Once your virtual environment activated, you will have to install the packages that powerdata-view requires :
```
pip install -r requirements.txt
```

# Basic Usage

To run powerdata-view, you just need to run the following :
```
python main.py
```
The generated tables and/or figures are located in `outputs/`.

# Configuration File

The configuration is defined in `config/config.yaml` :
- `metrics_processor_name`: Defines the metrics processor. Two implementations are provided:
  - `"PandaPowerMetricsProcessor"` : reads and processes [PandaPower](http://www.pandapower.org) data ;
  - `"PyPowSyblMetricsProcessor"` : reads and processes [PyPowSybl](https://pypowsybl.readthedocs.io) data.
- `dataset_versions`: Defines the different datasets you want to compare. For each dataset, you need to provide
    a name, a path and a color.
- `modes`: Different modes. Each mode can be activated by setting it to True.
  - `focus_modes`:
    - `all`: considers all snapshots and all objects.
    - `object`: considers each object separately.
    - `snapshot`: considers each snapshot separately.
  - `display_modes`:
    - `table`: Returns tables.
    - `plot`: Returns figures.
  - `statistics_modes`:
    - `summary`: Simply compares distributions for each version of the dataset.
    - `correlation`: Computes the correlation of the different versions of the dataset.

# Using a Different Configuration File

If you want to define a different configuration file (e.g. `config_2.yaml`), make sure to 
place it inside the `config/` directory, and use it using the following :
```
python main.py --config-name=config_2.yaml
```

# Contact

If you have any trouble using this tool, or if you have any question, please feel free to 
contact me at [balthazar.donon@uliege.be](mailto:balthazar.donon@uliege.be)
