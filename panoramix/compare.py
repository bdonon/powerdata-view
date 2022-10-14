from panoramix.plot import plot_float_summary, plot_float_summary_grid, plot_float_correlation, plot_bool_correlation, plot_bool_summary
from panoramix.metrics import load_multiple_metrics
from panoramix.utils import slugify, make_dir
from tabulate import tabulate
import matplotlib.pyplot as plt

import pandas as pd
import os


def build_df_dict(metrics_name, metrics_dict, focus="all", **kwargs):
    """Build a summary dataframe depending on the focus choice. One row per dataset.

        - If focus is set to ``all'', all objects and snapshots are considered and concatenated in the same vector.
        - If focus is set to ``snapshot'', each snapshot is considered separately.
        - If focus is set to ``object'', each object is considered separately
    """
    default_df = list(metrics_dict.values())[0]
    object_list = list(default_df.columns.values)
    snapshot_list = list(default_df.index.values)

    df_dict = {}

    if focus == "all":
        df_dict[metrics_name] = pd.DataFrame({k: v.stack() for k, v in metrics_dict.items()})

    elif focus == "snapshot":
        for snapshot_name in snapshot_list:
            name = metrics_name + ' - Snapshot ' + snapshot_name
            df_dict[name] = pd.DataFrame({k: v.loc[snapshot_name] for k, v in metrics_dict.items()})

    elif focus == "object":
        for object_name in object_list:
            name = metrics_name + ' - Object ' + object_name
            df_dict[name] = pd.DataFrame({k: v[object_name] for k, v in metrics_dict.items()})

    return df_dict


def display_table(key, df, path, statistics="summary", **kwargs):
    """Displays comparison tables. Depends on the desired statistics (summary or correlation), and on the data type."""
    data_type = df.stack().dtype
    if data_type == 'bool':
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

    print(key)
    print(tabulate(table, headers='keys', numalign="right", disable_numparse=True))
    print('\n')

    if path is not None:
        key_slug = slugify(key)
        with open(os.path.join(path, key_slug+'.txt'), 'w') as f:
            f.write(tabulate(table, headers='keys', tablefmt='plain', numalign="right", disable_numparse=True))
            f.write('\n\n')
            f.write(tabulate(table, headers='keys', tablefmt='latex', numalign="right", disable_numparse=True))


def display_plot(key, df, path, statistics="summary", dark=False, **kwargs):
    """Displays comparison plots. Depends on the desired statistics (summary or correlation), and on the data type."""

    plt.style.use('dark_background') if dark else plt.style.use('default')
    data_type = df.stack().dtype
    if data_type == 'bool':
        if statistics == "summary":
            plot_bool_summary(df, key, path, **kwargs)
        elif statistics == "correlation":
            plot_bool_correlation(df, key, path, **kwargs)
    elif data_type == 'float':
        if statistics == "summary":
            plot_float_summary(df, key, path, **kwargs)
            plot_float_summary_grid(df, key, path, **kwargs)
        elif statistics == "correlation":
            plot_float_correlation(df, key, path, **kwargs)



def compare_simple(df_dict, path, display="table", **kwargs):
    """Compares features for a single tuple (display, statistics, focus)."""
    for metrics_name, metrics_dict in df_dict.items():
        metrics_path = make_dir(path, metrics_name)
        df_dict = build_df_dict(metrics_name, metrics_dict, **kwargs)
        for key, df in df_dict.items():
            if display == "table":
                display_table(key, df, metrics_path, **kwargs)
            elif display == "plot":
                display_plot(key, df, metrics_path, **kwargs)


def load_compare_exhaustive(metrics_group_path_dict, **kwargs):
    """Loads multiple metrics directories and compares them together."""

    save_path = kwargs.get("save_path", None)
    display_modes = kwargs.get("display_modes", ["table", "plot"])
    statistics_modes = kwargs.get("statistics_modes", ["summary", "correlation"])
    focus_modes = kwargs.get("focus_modes", ["all", "object", "snapshot"])

    df_dict = load_multiple_metrics(metrics_group_path_dict)
    for display in display_modes:
        display_path = make_dir(save_path, display)
        for statistics in statistics_modes:
            statistics_path = make_dir(display_path, statistics)
            for focus in focus_modes:
                focus_path = make_dir(statistics_path, focus)
                compare_simple(df_dict, focus_path, display=display, statistics=statistics, focus=focus, **kwargs)
