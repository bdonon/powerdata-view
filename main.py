import powerdata_view as pv
from powerdata_view.metrics_processor import get_metrics_processor

import warnings
warnings.filterwarnings('ignore')

import hydra
import os
os.environ["HYDRA_FULL_ERROR"] = "1"


@hydra.main(version_base=None, config_path="config", config_name="config")
def main(cfg):

    # Check if metrics have already been computed for each dataset version. If not, computes them.
    metrics_processor = get_metrics_processor(cfg.metrics_processor_name)
    for version in cfg.dataset_versions:
        pv.compute_save_metrics(version.path, metrics_processor, cfg.metrics_processor_name)

    # Load metrics and compare the different versions.
    df_dict_dict = pv.load_multiple_metrics(cfg.dataset_versions, cfg.metrics_processor_name)
    color_dict = {version.name: version.color for version in cfg.dataset_versions}
    save_path = hydra.core.hydra_config.HydraConfig.get().runtime.output_dir
    pv.compare_exhaustive(df_dict_dict, color_dict, save_path, **cfg.modes, **cfg.figure_settings)


if __name__ == '__main__':
    main()
