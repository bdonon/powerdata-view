import matplotlib.pyplot as plt
import pandas as pd


def plot_float_summary(df, ax, colors):
    df.plot.hist(bins=100, grid=False, alpha=0.5, color=[colors(i) for i in range(len(df.index))], ax=ax)


def plot_float_correlation(df, ax):
    pd.plotting.scatter_matrix(df, alpha=0.5, ax=ax, hist_kwds={'bins': 100})


def plot_bool_summary(df, ax, colors):
    percentage = pd.DataFrame((df.sum() / df.count()), columns=['Percentage'])
    percentage.plot(kind='bar', legend=False, stacked=True, ax=ax)
    for i, bar in enumerate(ax.patches):
        bar.set_color(colors(i))
        p = percentage.iloc[i].values[0]
        ax.text(i, p, '{:.2%}'.format(p), horizontalalignment='center', verticalalignment='bottom')
    plt.ylim([0, 1.1])
    ax.set_yticklabels([f'{x:.1%}' for x in ax.get_yticks()])


def plot_bool_correlation(df, fig, ax):
    correlation = df.corr()
    im = ax.matshow(correlation, vmin=-1, vmax=1)
    ax.set_xticks(range(correlation.shape[1]), correlation.columns)
    ax.set_yticks(range(correlation.shape[1]), correlation.columns)
    fig.colorbar(im)
