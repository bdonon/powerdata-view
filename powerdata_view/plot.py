from powerdata_view.utils import slugify
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd
import os
import gc

def plot_float_summary(df, val_range, key, path, figsize, colors, log=False, extension=".pdf", title=True):
    """Plots of the different histogram versions."""
    fig, ax = plt.subplots(figsize=figsize)
    if title:
        if log:
            plt.title(key + ' - Log Scale')  # , loc='center', wrap=True)
        else:
            plt.title(key)
    #_range = [df.min().min(), df.max().max()]
    for i, name in enumerate(df.columns):
        data = df[name].astype(float).to_numpy()
        plt.hist(data[~np.isnan(data)], density=True, bins=100, alpha=0.5, color=colors[i], label=name, range=val_range)
    ax.yaxis.set_ticks([])

    plt.legend()
    if log:
        plt.yscale('log')
        ax.yaxis.set_ticks([])
        name = os.path.join(path, slugify(key) + '_log_scale' + extension)
    else:
        name = os.path.join(path, slugify(key) + extension)
    plt.tight_layout()
    plt.savefig(name, bbox_inches='tight')
    plt.cla()
    plt.clf()
    plt.close()
    gc.collect()


def plot_float_summary_grid(df, val_range, key, path, figsize, colors, log=False, grid=None, extension=".pdf", title=True):
    """Grid of plots of the different histogram versions."""

    def get_layout(df):
        """Returns the right values of nrows and ncol such that grid data is displayed evenly."""
        N = len(df.columns)
        n = np.floor(np.sqrt(N)).astype(int)
        if N == n ** 2:
            return n, n
        elif N <= n * (n + 1):
            return n, n + 1
        elif N <= (n + 1) ** 2:
            return n + 1, n + 1

    if grid is None:
        nx, ny = get_layout(df)
    else:
        nx, ny = grid[0], grid[1]
    fig, axs = plt.subplots(nx, ny, figsize=figsize)
    if title:
        if log:
            fig.suptitle(key+' - Log Scale')#, loc='center', wrap=True)
        else:
            fig.suptitle(key)
    #_range = [df.min().min(), df.max().max()]
    y_max = 0
    y_max_log = 0
    y_min_log = 1e12

    if len(df.columns) == 1 :
        axs_flat = [axs]
    else:
        axs_flat = axs.flat

    for i, name in enumerate(df.columns):
        data = df[name].astype(float).to_numpy().astype(float)
        axs_flat[i].hist(data[~np.isnan(data)], density=True, bins=100, color=colors[i], range=val_range)
        axs_flat[i].set_title(name)
        axs_flat[i].label_outer()
        y_max = max(y_max, axs_flat[i].get_ylim()[1])

        # Get limits for log scale
        axs_flat[i].set_yscale('log')
        y_max_log = max(y_max_log, axs_flat[i].get_ylim()[1])
        y_min_log = min(y_min_log, axs_flat[i].get_ylim()[0])
        axs_flat[i].set_yscale('linear')



    for i, name in enumerate(df.columns):
        if log:
            axs_flat[i].set_yscale('log')
            axs_flat[i].set_ylim([y_min_log, y_max_log])
            axs_flat[i].yaxis.set_ticks([])
        else:
            axs_flat[i].set_ylim([0, y_max])
            axs_flat[i].yaxis.set_ticks([])
    for ax in axs_flat[len(df.columns):]:
        ax.set_axis_off()  # Make unused subplots invisible


    if log:
        name = os.path.join(path, slugify(key) + '_grid_log_scale' + extension)
    else:
        name = os.path.join(path, slugify(key) + '_grid' + extension)
    plt.tight_layout()
    plt.savefig(name, bbox_inches='tight')
    plt.cla()
    plt.clf()
    plt.close()
    gc.collect()


def plot_float_summary_boxplot(df, val_range, key, path, figsize, colors, extension=".pdf", title=True):
    """Boxplots of the different histogram versions."""
    fig, ax = plt.subplots(figsize=figsize)
    if title:
        ax.set_title(key)#, loc='center', wrap=True)
    for i, c in enumerate(df.columns):
        data = df[c]
        box = plt.boxplot([data[~np.isnan(data)]], positions=[0.25*i], patch_artist=True, labels=[c])
        box['boxes'][0].set_facecolor("None")
        box['boxes'][0].set_edgecolor(colors[i])
        box['medians'][0].set_color(colors[i])
        box['whiskers'][0].set_color(colors[i])
        box['whiskers'][1].set_color(colors[i])
        box['caps'][0].set_color(colors[i])
        box['caps'][1].set_color(colors[i])
        for flier in box['fliers']:
            flier.set_markeredgecolor(colors[i])

    plt.xlim([-0.15, 0.25*(len(df.columns)-1)+0.15])
    plt.ylim(val_range)

    # box = plt.boxplot([df[c] for c in df.columns], patch_artist=True, labels=df.columns)
    # #for i, patch in enumerate(box['boxes']):
    # for i in range(len(df.columns)):
    #     #patch.set_facecolor("None")
    #     #patch.set_edgecolor(colors(i))
    #     box['boxes'][i].set_facecolor("None")
    #     box['boxes'][i].set_edgecolor(colors(i))
    #     box['medians'][i].set_color(colors(i))
    #     box['whiskers'][2*i].set_color(colors(i))
    #     box['whiskers'][2*i+1].set_color(colors(i))
    #     box['caps'][2*i].set_color(colors(i))
    #     box['caps'][2*i+1].set_color(colors(i))
    #     box['fliers'][i].set_color(colors(i))
    plt.tight_layout()
    plt.savefig(os.path.join(path, slugify(key) + '_boxplot' + extension), bbox_inches='tight')
    plt.cla()
    plt.clf()
    plt.close()
    gc.collect()


def plot_float_correlation(df, key, path, figsize, colors, night_mode, extension=".pdf", title=True):
    """Correlation scatter plot for float metrics."""
    _min, _max = df.min().min(), df.max().max()
    _range = [_min - 0.1*(_max - _min), _max + 0.1*(_max - _min)]

    color = 'firebrick' if night_mode else 'royalblue'
    axs = pd.plotting.scatter_matrix(df, alpha=1., s=1., figsize=figsize,
                                     hist_kwds={'bins': 100, 'color': colors[0], 'range':_range},
                                     color=color)
    for i, subaxis in enumerate(axs):
        for j, ax in enumerate(subaxis):
            ax.set_xlim(_range)
            ax.yaxis.set_ticks([])
            if i == j:
                # Change color of diagonal elements
                [bar.set_color(colors[i]) for bar in ax.patches]
            else:
                # Plot x=y for non-diagonal elements
                color = 'white' if night_mode else 'black'
                ax.axline((0, 0), slope=1., color=color, linewidth=1., alpha=0.5)
                ax.set_ylim(_range)
            ax.tick_params(axis='x', labelrotation=0)
    if title:
        plt.suptitle(key)#, loc='center', wrap=True)
    plt.tight_layout()
    plt.savefig(os.path.join(path, slugify(key) + extension), bbox_inches='tight')
    plt.cla()
    plt.clf()
    plt.close()
    gc.collect()


def plot_bool_summary(df, key, path, figsize, colors, extension=".pdf", title=True):
    """Bar plot for bool metrics."""
    fig, ax = plt.subplots(figsize=figsize)
    if title:
        ax.set_title(key)#, loc='center', wrap=True)
    percentage = pd.DataFrame((df.sum() / df.count()), columns=['Percentage'])


    div = 10000 - df.count()
    percentage = pd.DataFrame(((df.sum() + div) / 10000), columns=['Percentage'])
    # # TODO : il faut trouver un moyen de capturer les divergences plutôt que juste les exclure.
    percentage.plot(kind='bar', legend=False, stacked=True, ax=ax, ylim=[0, 1.1])
    for i, bar in enumerate(ax.patches):
        bar.set_color(colors[i])
        p = percentage.iloc[i].values[0]
        ax.text(i, p+0.03, '{:.2%}'.format(p), horizontalalignment='center', verticalalignment='bottom')
    #ax.set_ylim([0, 1.1])

    ax.tick_params(axis='x', labelrotation=0)
    ax.set_yticks([0., 0.5, 1.])  # Useless, but avoids a UserWarning.
    ax.set_yticklabels([f'{x:.0%}' for x in ax.get_yticks().tolist()])
    plt.tight_layout()
    plt.savefig(os.path.join(path, slugify(key) + extension), bbox_inches='tight')
    plt.cla()
    plt.clf()
    plt.close()
    gc.collect()


def plot_bool_correlation(df, key, path, figsize, colors, extension=".pdf", title=True):
    """Correlation matrix for boolean metrics."""
    fig, ax = plt.subplots(figsize=figsize)
    if title:
        ax.set_title(key)#, loc='center', wrap=True)
    im = ax.matshow(df.corr(), vmin=-1, vmax=1)
    ax.set_xticks(range(len(df.columns)), df.columns)
    ax.set_yticks(range(len(df.columns)), df.columns)
    fig.colorbar(im)
    plt.tight_layout()
    plt.savefig(os.path.join(path, slugify(key) + extension), bbox_inches='tight')
    plt.cla()
    plt.clf()
    plt.close()
    gc.collect()
