from powerdata_view.plot import plot_float_summary, plot_float_summary_grid, plot_float_correlation, \
     plot_bool_summary, plot_float_summary_boxplot
from powerdata_view.utils import slugify, make_dir
from tabulate import tabulate
import matplotlib.pyplot as plt

import pandas as pd
import tqdm
import os


def display_table(key, df, path, statistics="summary"):
    """Displays comparison tables. Depends on the desired statistics (summary or correlation), and on the data type."""
    data_type = df.stack().dtype
    if data_type in ['bool', 'object']:
        if statistics == "summary":
            table = pd.DataFrame((df.sum() / df.count()).map("{:.1%}".format), columns=['Percentage'])
        elif statistics == "correlation":
            table = df.corr().apply(lambda s: s.apply(lambda x: '{:.2e}'.format(x)))
        else:
            raise ValueError("Statistics {} is not valid.".format(statistics))
    elif data_type in ['float', 'int']:
        if statistics == "summary":
            table = df.describe().apply(lambda s: s.apply(lambda x: '{:.2e}'.format(x)))
        elif statistics == "correlation":
            table = df.corr().apply(lambda s: s.apply(lambda x: '{:.2e}'.format(x)))
        else:
            raise ValueError("Statistics {} is not valid.".format(statistics))

    if path is not None:
        key_slug = slugify(key)
        with open(os.path.join(path, key_slug+'.txt'), 'w') as f:
            f.write(tabulate(table, headers='keys', tablefmt='plain', numalign="right", disable_numparse=True))
            f.write('\n\n')
            f.write(tabulate(table, headers='keys', tablefmt='latex', numalign="right", disable_numparse=True))


def display_plot(key, color_dict, df, path, statistics="summary", val_range=None, **kwargs):
    """Displays comparison plots. Depends on the desired statistics (summary or correlation), and on the data type."""

    night_mode = kwargs.get("night_mode", False)
    if night_mode:
        plt.style.use('dark_background')
    figsize = kwargs.get("figsize", [6.4, 4.8])
    colors = [color_dict[dataset_name] for dataset_name in df.columns]#plt.cm.tab10

    data_type = df.stack().dtype
    if data_type in ['bool', 'object']:
        if statistics == "summary":
            plot_bool_summary(df, key, path, figsize, colors)
        elif statistics == "correlation":
            pass ## Correlation plots for bool are not that interesting.
            #plot_bool_correlation(df, key, path, figsize, dpi, colors)
    elif data_type == 'float':
        if statistics == "summary":
            plot_float_summary(df, val_range, key, path, figsize, colors, log=True)
            plot_float_summary(df, val_range, key, path, figsize, colors, log=False)
            plot_float_summary_grid(df, val_range, key, path, figsize, colors, log=True)
            plot_float_summary_grid(df, val_range, key, path, figsize, colors, log=False)
            plot_float_summary_boxplot(df, val_range, key, path, figsize, colors)
        elif statistics == "correlation":
            plot_float_correlation(df, key, path, figsize, colors, night_mode)


def aggregate_versions(metrics_name, df_dict, focus="all"):
    """Aggregates together multiple versions of a metrics, depending on the focus. One column per version.

        - If focus is set to ``all'', all objects and snapshots are considered and concatenated in the same vector.
        - If focus is set to ``snapshot'', each snapshot is considered separately.
        - If focus is set to ``object'', each object is considered separately

    """
    object_list = list(next(iter(df_dict.values())).columns.values)
    snapshot_list = list(next(iter(df_dict.values())).index.values)

    out = {}
    val_range = {}
    tmp = pd.concat([pd.DataFrame(data=v.stack(), columns=[k]) for k, v in df_dict.items()], axis=1)
    _min, _max = 1.*tmp.min().min(), 1.*tmp.max().max()
    if focus == "all":
        out[metrics_name] = pd.concat([pd.DataFrame(data=v.stack(), columns=[k]) for k, v in df_dict.items()], axis=1)
        val_range[metrics_name] = [_min - 0.1 * (_max - _min), _max + 0.1 * (_max - _min)]
    elif focus == "snapshot":
        for snapshot_name in snapshot_list:
            out[metrics_name+' - '+snapshot_name] = pd.DataFrame({k: v.loc[snapshot_name] for k, v in df_dict.items()})
            val_range[metrics_name+' - '+snapshot_name] = [_min - 0.1 * (_max - _min), _max + 0.1 * (_max - _min)]
    elif focus == "object":
        for object_name in object_list:
            out[metrics_name+' - '+object_name] = pd.DataFrame({k: v[object_name] for k, v in df_dict.items()})
            val_range[metrics_name + ' - ' + object_name] = [_min - 0.1 * (_max - _min), _max + 0.1 * (_max - _min)]
    return out, val_range


def compare_simple(df_dict_dict, color_dict, path, display="table", statistics="summary", focus="all", **kwargs):
    """Compares features for a single tuple (display, statistics, focus)."""
    pbar = tqdm.tqdm(df_dict_dict.items())
    for metrics_name, df_dict in pbar:
        pbar.set_description('            Processing {}'.format(metrics_name))
        metrics_path = make_dir(path, metrics_name)
        aggregate_dict, val_range = aggregate_versions(metrics_name, df_dict, focus=focus)
        for aggregate_name, aggregate_df in aggregate_dict.items():
            if display == "table":
                display_table(aggregate_name, aggregate_df, metrics_path, statistics=statistics)
            elif display == "plot":
                display_plot(aggregate_name, color_dict, aggregate_df, metrics_path, statistics=statistics, val_range=val_range[aggregate_name], **kwargs)


def compare_exhaustive(df_dict_dict, color_dict, save_path, display_modes, statistics_modes, focus_modes, **kwargs):
    """Compares multiple metrics dataframe together and store the resulting tables / plots."""

    display_modes_list = [k for k, v in display_modes.items() if v]
    statistics_modes_list = [k for k, v in statistics_modes.items() if v]
    focus_modes_list = [k for k, v in focus_modes.items() if v]

    for display in display_modes_list:
        print("Display = {}".format(display))
        display_path = make_dir(save_path, display)
        for statistics in statistics_modes_list:
            print("    Statistics = {}".format(statistics))
            statistics_path = make_dir(display_path, statistics)
            for focus in focus_modes_list:
                print("        Focus = {}".format(focus))
                focus_path = make_dir(statistics_path, focus)
                compare_simple(df_dict_dict, color_dict, focus_path, display=display, statistics=statistics, focus=focus, **kwargs)
