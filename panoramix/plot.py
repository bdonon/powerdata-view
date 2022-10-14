from panoramix.utils import slugify
import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_float_summary(df, key, path=None, figsize=None, dpi=50, colors=plt.cm.tab10, **kwargs):
    figsize = [6.4, 4.8] if figsize is None else figsize
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_title(key)

    df.plot.hist(bins=100, grid=False, alpha=0.5, color=[colors(i) for i in range(len(df.index))], ax=ax)

    plt.tight_layout()
    if path is not None:
        plt.savefig(os.path.join(path, slugify(key) + '.png'))
    plt.show()


def plot_float_summary_grid(df, key, path=None, figsize=None, dpi=50, colors=plt.cm.tab10, **kwargs):
    figsize = [6.4, 4.8] if figsize is None else figsize
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    #ax = fig.gca()
    #ax.set_title(key)

    axs = df.hist(bins=100, grid=False, sharex=True, sharey=True, ax=ax)
    plt.suptitle(key)
    for i, ax in enumerate(axs.flat):
        for bar in ax.patches:
            bar.set_color(colors(i))

    plt.tight_layout()
    if path is not None:
        plt.savefig(os.path.join(path, slugify(key) + '_grid.png'))
    plt.show()


def plot_float_correlation(df, key, path=None, figsize=None, dpi=50, **kwargs):
    figsize = [6.4, 4.8] if figsize is None else figsize
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_title(key)

    pd.plotting.scatter_matrix(df, alpha=0.5, ax=ax, hist_kwds={'bins': 100})

    plt.tight_layout()
    if path is not None:
        plt.savefig(os.path.join(path, slugify(key) + '.png'))
    plt.show()


def plot_bool_summary(df, key, path=None, figsize=None, dpi=50, colors=plt.cm.tab10, **kwargs):
    figsize = [6.4, 4.8] if figsize is None else figsize
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_title(key)

    percentage = pd.DataFrame((df.sum() / df.count()), columns=['Percentage'])
    percentage.plot(kind='bar', legend=False, stacked=True, ax=ax)
    for i, bar in enumerate(ax.patches):
        bar.set_color(colors(i))
        p = percentage.iloc[i].values[0]
        ax.text(i, p, '{:.2%}'.format(p), horizontalalignment='center', verticalalignment='bottom')
    plt.ylim([0, 1.1])
    ax.set_yticklabels([f'{x:.1%}' for x in ax.get_yticks()])

    plt.tight_layout()
    if path is not None:
        plt.savefig(os.path.join(path, slugify(key) + '.png'))
    plt.show()


def plot_bool_correlation(df, key, path=None, figsize=None, dpi=50, **kwargs):
    figsize = [6.4, 4.8] if figsize is None else figsize
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_title(key)

    correlation = df.corr()
    im = ax.matshow(correlation, vmin=-1, vmax=1)
    ax.set_xticks(range(correlation.shape[1]), correlation.columns)
    ax.set_yticks(range(correlation.shape[1]), correlation.columns)
    fig.colorbar(im)

    plt.tight_layout()
    if path is not None:
        plt.savefig(os.path.join(path, slugify(key) + '.png'))
    plt.show()
