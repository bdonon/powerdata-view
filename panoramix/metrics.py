import os
import tqdm
import pandas as pd


def compute_save_metrics(data_dir, problem, out_dir):
    """Computes and saves metrics dictionary if it hasn't been done before."""
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        df_dict = compute_metrics(data_dir, problem)
        save_metrics(df_dict, out_dir)
    else:
        print("{} already exists. Metrics will not be computed again.".format(out_dir))


def compute_metrics(data_dir, problem):
    """Computes metrics dictionary."""
    backend = problem.backend
    data_files = backend.get_valid_files(data_dir)
    df_dict = problem.initialize_table_dict()
    for file in tqdm.tqdm(data_files, desc='Building metrics for {}'.format(data_dir)):
        problem.add_assessment_row(file, df_dict)
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


def load_multiple_metrics(paths_to_dataset_versions, problem_name):
    """Loads one dictionary of metrics dataframes per dataset version."""
    out = {}
    for version_name, version_path in paths_to_dataset_versions.items():
        metrics_dir = os.path.join(version_path, problem_name)
        out[version_name] = load_metrics(metrics_dir)
    return {mn: {vn: out[vn][mn] for vn in out.keys()} for mn in next(iter(out.values())).keys()}
