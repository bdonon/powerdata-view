import os
import tqdm
import pandas as pd


def compute_save_metrics(data_dir, problem):
    """Computes and saves metrics dictionary."""
    metrics_dict = compute_metrics(data_dir, problem)
    problem_path = os.path.join(data_dir, problem.name)
    os.mkdir(problem_path)
    save_metrics(metrics_dict, problem_path)


def compute_metrics(data_dir, problem):
    """Computes metrics dictionary."""
    backend = problem.backend
    data_files = backend.get_valid_files(data_dir)
    table_dict = problem.initialize_table_dict()
    file_list = []
    for file in tqdm.tqdm(data_files):
        problem.add_assessment_row(file, table_dict)
        file_list.append(os.path.basename(file))
    metrics_dict = {key: pd.DataFrame(data=table, index=file_list) for key, table in table_dict.items()}
    return metrics_dict


def save_metrics(metrics_dict, save_path):
    """Saves metrics."""
    for metrics_name, metrics_df in metrics_dict.items():
        metrics_path = os.path.join(save_path, metrics_name+'.csv')
        metrics_df.to_csv(metrics_path)


def load_metrics(metrics_group_path):
    """Loads metrics."""
    metrics_dict = {}
    for filename in os.listdir(metrics_group_path):
        metrics_path = os.path.join(metrics_group_path, filename)
        if metrics_path.endswith('.csv'):
            metrics_name = os.path.splitext(filename)[0]
            metrics_df = pd.read_csv(metrics_path, index_col=0)
            metrics_dict[metrics_name] = metrics_df
    return metrics_dict


def load_multiple_metrics(metrics_group_path_dict):
    """Loads metrics computed over multiple datasets."""
    default_metrics_group_path = list(metrics_group_path_dict.values())[0]
    default_metrics_filename_list = os.listdir(default_metrics_group_path)
    tmp = {}
    for dataset_name, metrics_group_path in metrics_group_path_dict.items():
        metrics_filename_list = os.listdir(metrics_group_path)
        assert set(list(metrics_filename_list)) == set(list(default_metrics_filename_list))
        tmp[dataset_name] = load_metrics(metrics_group_path)

    out = {}
    dataset_name_list = list(metrics_group_path_dict.keys())
    for metrics_filename in default_metrics_filename_list:
        metrics_name = os.path.splitext(metrics_filename)[0]
        out[metrics_name] = {}
        for dataset_name in dataset_name_list:
            out[metrics_name][dataset_name] = tmp[dataset_name][metrics_name]

    return out
