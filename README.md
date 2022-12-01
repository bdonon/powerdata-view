# panoramix
Compares metrics over different versions of a power grid dataset.

```
python main.py --config_file=config/config.json
```

## Options

Options should be specified in the `config.json` file:
- `"problem_name"`: Name of a problem instance. For now, only `"PandaPowerVoltageControl"` is available.
- `"paths_to_dataset_versions"`: Dictionary of paths to dataset versions. Keys will be used as figure titles.
- `"output_dir"`: Path to an output directory.
- `"modes`: Dictionary of modes.
  - `"focus_modes"`: List of requested focus modes. By default, set to `["all", "object", "snapshot"]`.
    - `"all"`: considers all snapshots and all objects.
    - `"object"`: considers each object separately.
    - `"snapshot"`: considers each snapshot separately.
  - `"display_modes"`: List of requested focus modes. By default, set to `["table", "plot"]`.
    - `"table"`: Returns tables.
    - `"plot"`: Returns plots.
  - `"statistics_modes"`: List of requested statistics modes. By default, set to `["summary", "correlation"]`.
    - `"summary`: Simply compares distributions for each version of the dataset.
    - `"correlation"`: Computes the correlation of the different versions of the dataset.
  - `"figure_settings"`
    - `"dark"`: If True, it produces night mode plots. By default set to False.
    - `"figsize"`: Size of figures. By default, set to `[6.4, 4.8]`, but I recommend `[8, 5]` for slides presentations.
    - `"dpi"`: Resolution of figures. By default, set to `50`, but I recommend `200` for slides presentations.
