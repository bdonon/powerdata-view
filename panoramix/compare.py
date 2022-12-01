from panoramix.plot import plot_float_summary, plot_float_summary_grid, plot_float_correlation, \
    plot_bool_correlation, plot_bool_summary, plot_float_summary_boxplot
from panoramix.metrics import load_multiple_metrics
from panoramix.utils import slugify, make_dir
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
    elif data_type == 'float':
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


def display_plot(key, df, path, statistics="summary", **kwargs):
    """Displays comparison plots. Depends on the desired statistics (summary or correlation), and on the data type."""

    dark = kwargs.get("dark", False)
    if dark:
        plt.style.use('dark_background')
    figsize = kwargs.get("figsize", [6.4, 4.8])
    dpi = kwargs.get("dpi", 50)
    colors = plt.cm.tab10

    data_type = df.stack().dtype
    if data_type in ['bool', 'object']:
        if statistics == "summary":
            plot_bool_summary(df, key, path, figsize, dpi, colors)
        elif statistics == "correlation":
            pass ## Correlation plots for bool are not that interesting.
            #plot_bool_correlation(df, key, path, figsize, dpi, colors)
    elif data_type == 'float':
        if statistics == "summary":
            plot_float_summary(df, key, path, figsize, dpi, colors)
            plot_float_summary_grid(df, key, path, figsize, dpi, colors)
            plot_float_summary_boxplot(df, key, path, figsize, dpi, colors)
        elif statistics == "correlation":
            plot_float_correlation(df, key, path, figsize, dpi, colors, dark)


def aggregate_versions(metrics_name, df_dict, focus="all"):
    """Aggregates together multiple versions of a metrics, depending on the focus. One column per version.

        - If focus is set to ``all'', all objects and snapshots are considered and concatenated in the same vector.
        - If focus is set to ``snapshot'', each snapshot is considered separately.
        - If focus is set to ``object'', each object is considered separately

    """
    object_list = list(next(iter(df_dict.values())).columns.values)
    snapshot_list = list(next(iter(df_dict.values())).index.values)

    out = {}
    if focus == "all":
        out[metrics_name] = pd.concat([pd.DataFrame(data=v.stack(), columns=[k]) for k, v in df_dict.items()], axis=1)
    elif focus == "snapshot":
        for snapshot_name in snapshot_list:
            out[metrics_name+' - '+snapshot_name] = pd.DataFrame({k: v.loc[snapshot_name] for k, v in df_dict.items()})
    elif focus == "object":
        for object_name in object_list:
            out[metrics_name+' - '+object_name] = pd.DataFrame({k: v[object_name] for k, v in df_dict.items()})
    return out


def compare_simple(df_dict_dict, path, display="table", statistics="summary", focus="all", **kwargs):
    """Compares features for a single tuple (display, statistics, focus)."""
    pbar = tqdm.tqdm(df_dict_dict.items())
    for metrics_name, df_dict in pbar:
        pbar.set_description('            Processing {}'.format(metrics_name))
        metrics_path = make_dir(path, metrics_name)
        aggregate_dict = aggregate_versions(metrics_name, df_dict, focus=focus)
        for aggregate_name, aggregate_df in aggregate_dict.items():
            if display == "table":
                display_table(aggregate_name, aggregate_df, metrics_path, statistics=statistics)
            elif display == "plot":
                display_plot(aggregate_name, aggregate_df, metrics_path, statistics=statistics, **kwargs)


def compare_exhaustive(df_dict_dict, save_path, display_modes=None, statistics_modes=None, focus_modes=None, **kwargs):
    """Compares multiple metrics dataframe together and store the resulting tables / plots."""

    if display_modes is None:
        display_modes = ["table", "plot"]
    if statistics_modes is None:
        statistics_modes = ["summary", "correlation"]
    if focus_modes is None:
        focus_modes = ["all", "object", "snapshot"]

    for display in display_modes:
        print("Display = {}".format(display))
        display_path = make_dir(save_path, display)
        for statistics in statistics_modes:
            print("    Statistics = {}".format(statistics))
            statistics_path = make_dir(display_path, statistics)
            for focus in focus_modes:
                print("        Focus = {}".format(focus))
                focus_path = make_dir(statistics_path, focus)
                compare_simple(df_dict_dict, focus_path, display=display, statistics=statistics, focus=focus, **kwargs)
