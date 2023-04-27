import os
import tqdm
import pandas as pd


def compute_save_metrics(data_dir, metrics_processor, metrics_processor_name):
    """Computes and saves metrics dictionary if it hasn't been done before."""
    panoramix_dir = os.path.join(data_dir, "powerdata_view")
    if not os.path.exists(panoramix_dir):
        os.mkdir(panoramix_dir)
    metrics_dir = os.path.join(panoramix_dir, metrics_processor_name)
    if not os.path.exists(metrics_dir):
        os.mkdir(metrics_dir)
        df_dict = compute_metrics(data_dir, metrics_processor)
        save_metrics(df_dict, metrics_dir)
    else:
        print("{} already exists. Metrics will not be computed again.".format(metrics_dir))


def compute_metrics(data_dir, problem):
    """Computes metrics dictionary."""
    df_dict = problem.initialize_table_dict()
    data_files = os.listdir(data_dir)
    for file in tqdm.tqdm(data_files, desc='Building metrics for {}'.format(data_dir)):
        try:
            problem.add_assessment_row(os.path.join(data_dir, file), df_dict)
        except:
           continue
    return df_dict


def save_metrics(df_dict, save_path):
    """Saves dictionary of metrics dataframes."""
    for name, df in df_dict.items():
        path = os.path.join(save_path, name+'.csv')
        df.to_csv(path)


def load_metrics(path):
    """Loads dictionary of metrics dataframes."""
    df_dict = {}
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if filepath.endswith('.csv'):
            name = os.path.splitext(filename)[0]
            df_dict[name] = pd.read_csv(filepath, index_col=0)
    return df_dict


def load_multiple_metrics(dataset_versions, problem_name):
    """Loads one dictionary of metrics dataframes per dataset version."""
    out = {}
    for version in dataset_versions:
        metrics_dir = os.path.join(version.path, "powerdata_view", problem_name)
        out[version.name] = load_metrics(metrics_dir)
    return {mn: {vn: out[vn][mn] for vn in out.keys()} for mn in next(iter(out.values())).keys()}
