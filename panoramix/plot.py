from panoramix.utils import slugify
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
import os


def plot_float_summary(df, key, path, figsize, dpi, colors):
    """Plots of the different histogram versions."""
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_title(key)
    _range = [df.min().min(), df.max().max()]
    for i, name in enumerate(df.columns):
        data = df[name].astype(float).to_numpy()
        plt.hist(data[~np.isnan(data)], density=True, bins=100, alpha=0.5, color=colors(i), label=name, range=_range)
    ax.yaxis.set_ticks([])
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(path, slugify(key) + '.png'))
    plt.close()


def plot_float_summary_grid(df, key, path, figsize, dpi, colors):
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

    nx, ny = get_layout(df)
    fig, axs = plt.subplots(nx, ny, figsize=figsize, dpi=dpi)
    fig.suptitle(key)
    _range = [df.min().min(), df.max().max()]
    y_max = 0
    for i, name in enumerate(df.columns):
        data = df[name].astype(float).to_numpy().astype(float)
        axs.flat[i].hist(data[~np.isnan(data)], density=True, bins=100, color=colors(i), range=_range)
        axs.flat[i].set_title(name)
        axs.flat[i].label_outer()
        axs.flat[i].yaxis.set_ticks([])
        y_max = max(y_max, axs.flat[i].get_ylim()[1])
    for i, name in enumerate(df.columns):
        axs.flat[i].set_ylim([0, y_max])
    for ax in axs.flat[len(df.columns):]:
        ax.set_axis_off()  # Make unused subplots invisible
    plt.tight_layout()
    plt.savefig(os.path.join(path, slugify(key) + '_grid.png'))
    plt.close()


def plot_float_summary_boxplot(df, key, path, figsize, dpi, colors):
    """Boxplots of the different histogram versions."""
    plt.subplots(figsize=figsize, dpi=dpi)
    for i, c in enumerate(df.columns):
        box = plt.boxplot([df[c]], positions=[0.25*i], patch_artist=True, labels=[c])
        box['boxes'][0].set_facecolor("None")
        box['boxes'][0].set_edgecolor(colors(i))
        box['medians'][0].set_color(colors(i))
        box['whiskers'][0].set_color(colors(i))
        box['whiskers'][1].set_color(colors(i))
        box['caps'][0].set_color(colors(i))
        box['caps'][1].set_color(colors(i))
        for flier in box['fliers']:
            flier.set_markeredgecolor(colors(i))

    plt.xlim([-0.15, 0.25*(len(df.columns)-1)+0.15])

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
    plt.savefig(os.path.join(path, slugify(key) + '_boxplot.png'))
    plt.close()


def plot_float_correlation(df, key, path, figsize, dpi, colors, dark):
    """Correlation scatter plot for float metrics."""
    _min, _max = df.min().min(), df.max().max()
    _range = [_min - 0.1*(_max - _min), _max + 0.1*(_max - _min)]

    color = 'firebrick' if dark else 'royalblue'
    axs = pd.plotting.scatter_matrix(df, alpha=1., s=0.5, figsize=figsize,
                                     hist_kwds={'bins': 100, 'color': colors(0), 'range':_range},
                                     color=color)
    for i, subaxis in enumerate(axs):
        for j, ax in enumerate(subaxis):
            ax.set_xlim(_range)
            ax.tick_params(axis='x', labelrotation=0)
            ax.yaxis.set_ticks([])
            if i == j:
                # Change color of diagonal elements
                [bar.set_color(colors(i)) for bar in ax.patches]
            else:
                # Plot x=y for non-diagonal elements
                color = 'white' if dark else 'black'
                ax.axline((0, 0), slope=1., color=color, linewidth=1.)
                ax.set_ylim(_range)

    plt.suptitle(key)
    plt.tight_layout()
    plt.savefig(os.path.join(path, slugify(key) + '.png'), dpi=dpi)
    plt.close()


def plot_bool_summary(df, key, path, figsize, dpi, colors):
    """Bar plot for bool metrics."""
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_title(key)
    percentage = pd.DataFrame((df.sum() / df.count()), columns=['Percentage'])
    percentage.plot(kind='bar', legend=False, stacked=True, ax=ax)
    for i, bar in enumerate(ax.patches):
        bar.set_color(colors(i))
        p = percentage.iloc[i].values[0]
        ax.text(i, p, '{:.2%}'.format(p), horizontalalignment='center', verticalalignment='bottom')
    ax.set_ylim([0, 1.1])
    ax.set_yticks(ax.get_yticks())  # Useless, but avoids a UserWarning.
    ax.set_yticklabels([f'{x:.1%}' for x in ax.get_yticks().tolist()])
    plt.tight_layout()
    plt.savefig(os.path.join(path, slugify(key) + '.png'))
    plt.close()


def plot_bool_correlation(df, key, path, figsize, dpi, colors):
    """Correlation matrix for boolean metrics."""
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_title(key)
    im = ax.matshow(df.corr(), vmin=-1, vmax=1)
    ax.set_xticks(range(len(df.columns)), df.columns)
    ax.set_yticks(range(len(df.columns)), df.columns)
    fig.colorbar(im)
    plt.tight_layout()
    plt.savefig(os.path.join(path, slugify(key) + '.png'))
    plt.close()
