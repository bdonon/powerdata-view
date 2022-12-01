import os.path

import panoramix as px
import argparse
import json
import time


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compare versions of a dataset.')
    parser.add_argument('--config_file', type=str, required=True, help='Config .json file.')

    args = parser.parse_args()
    with open(args.config_file) as f:
        config = json.load(f)

    problem_name = config.get("problem_name")
    problem = px.get_problem(problem_name)
    paths_to_dataset_versions = config.get("paths_to_dataset_versions")
    output_dir = config.get("output_dir")
    modes = config.get("modes", {})
    figure_settings = config.get("figure_settings", {})

    # Déjà, on vérifie si chaque dataset a des métriques dont le nom correspond bien
    for _, path in paths_to_dataset_versions.items():
        metrics_dir = os.path.join(path, problem_name)
        px.compute_save_metrics(path, problem, metrics_dir)

    # On regarder si il y a déjà une sortie qui s'appelle comme ça....
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Run directory
    save_name = time.strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(output_dir, save_name)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with open(os.path.join(save_path, "config.json"), "w") as outfile:
        json.dump(config, outfile)

    # Load metrix and compare them
    df_dict_dict = px.load_multiple_metrics(paths_to_dataset_versions, problem_name)
    px.compare_exhaustive(df_dict_dict, save_path, **modes, **figure_settings)
