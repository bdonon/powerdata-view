# panoramix
Policy assessment for the idefix project.

The goal is to be able to compare metrics over different versions of a dataset.
More specifically, let us consider the case where you have multiple methods that you want to compare.
You will first apply your different methods to the same test set, and then compare the results.

## Build metrics tables

At first, you need to compute metrics over the dataset you want to consider.
You need to do this for all different versions of you dataset :
```
import panoramix as px

problem = px.PandaPowerVoltageControl()
data_dir = 'data/case60nordic_2000/test'
px.compute_save_metrics(data_dir, problem)
```
This creates a small directory inside the test set whose name is defined by `problem.name`.
In this case, the problem name is also `PandaPowerVoltageControl`.

## Comparison

Once you have computed metrics over the different versions of your test set, you may compare them.
All tables and plots are stored in a directory that you should define.
```
import panoramix as px

test_sets_versions = {
    'Default': 'data/test/PandaPowerVoltageControl/',
    'OPF Solver': 'opf/test/PandaPowerVoltageControl/',
    'Idéfix': 'idéfix/model01/processed_test/PandaPowerVoltageControl/'
}

px.load_compare_exhaustive(test_sets_versions, save_path='tmp')
```

## Options

There are multiple options for the comparison:
- `dark`: If True, it produces night mode plots. By default set to False.
- `figsize`: Size of figures. By default, set to `[6.4, 4.8]`, but I recommend `[8, 5]` for slides presentations.
- `dpi`: Resolution of figures. By default, set to `50`, but I recommend `200` for slides presentations.
- `focus_modes`: List of focus modes that should be considered. By default, set to `["all", "object", "snapshot"]`.
  - `"all"`: considers all snapshots and all objects.
  - `"object"`: considers each object separately.
  - `"snapshot"`: considers each snapshot separately.
- `statistics_modes`: List of statistics modes that should be considered. By default, set to `["summary", "correlation"]`.
  - `"summary`: Simply compares distributions for each version of the dataset.
  - `"correlation"`: Computes the correlation of the different versions of the dataset.
- `display_modes`: List of focus modes that should be processed. By default, set to `["table", "plot"]`.
  - `"table"`: Returns tables.
  - `"plot"`: Returns plots.

## Building your own metrics

You can provide a different problem implementation, as long as you follow the provided interface AbstractProblem.
