from abc import ABC, abstractmethod
import pandas as pd
import os


class MetricsProcessorInterface(ABC):
    """Abstract Base Class for a metrics processor.

    It loads power grids, performs a power flow computations, and then iteratively computes a series of metrics defined
    in the dictionary `metrics_dict`.
    """

    def __init__(self):
        pass

    @property
    @abstractmethod
    def metrics_dict(self):
        """Dictionary of metrics functions. Should be overridden."""
        pass

    @abstractmethod
    def load_power_grid(self, filename):
        """Loads a power grid file. Should be overriden in a proper implementation."""
        pass

    @abstractmethod
    def run_powerflow(self, power_grid):
        """Runs a power flow simulation. Should be overriden in a proper implementation."""
        pass

    def initialize_table_dict(self):
        """Initializes the dictionary of metrics as containing empty dataframes as items."""
        return {key: pd.DataFrame([[]], columns=[], index=[]) for key in self.metrics_dict.keys()}

    def add_assessment_row(self, filepath, df_dict):
        """Imports and simulates a file, computes metrics and appends them to table_dict."""
        power_grid = self.load_power_grid(filepath)
        sample_name = os.path.splitext(os.path.basename(filepath))[0]
        self.run_powerflow(power_grid)
        for key, metrics in self.metrics_dict.items():
            metrics_val, metrics_col = metrics(power_grid)
            r = pd.DataFrame([metrics_val], columns=[metrics_col], index=[sample_name])
            df_dict[key] = pd.concat([r, df_dict[key]], axis=0, join='outer')
