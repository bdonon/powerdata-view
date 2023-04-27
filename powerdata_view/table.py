import pandas as pd


def table_float_summary(df):
    return df.describe().apply(lambda s: s.apply(lambda x: '{:.2e}'.format(x)))


def table_float_correlation(df):
    return df.corr().apply(lambda s: s.apply(lambda x: '{:.2e}'.format(x)))


def table_bool_summary(df):
    return pd.DataFrame((df.sum() / df.count()).map("{:.1%}".format), columns=['Percentage'])


def table_bool_correlation(df):
    return df.corr().apply(lambda s: s.apply(lambda x: '{:.2e}'.format(x)))
