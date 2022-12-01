from abc import ABC, abstractmethod
import pandas as pd
import os


class AbstractProblem(ABC):
    """"""

    def __init__(self):
        """"""
        pass

    @property
    @abstractmethod
    def backend(self):
        """ML4PS backend. Should be overridden."""
        pass

    @property
    @abstractmethod
    def feature_names(self):
        """Feature names that should be extracted from the network by the backend. Should be overridden."""
        pass

    @property
    @abstractmethod
    def address_names(self):
        """Address names that should be extracted from the network by the backend. Should be overridden."""
        pass

    @property
    @abstractmethod
    def metrics_dict(self):
        """Dictionary of metrics functions. Should be overridden."""
        pass

    def initialize_table_dict_old(self):
        """Initializes the dictionary of assessment tables."""
        return {key: [] for key in self.metrics_dict.keys()}

    def initialize_table_dict(self):
        return {key: pd.DataFrame([[]], columns=[], index=[]) for key in self.metrics_dict.keys()}

    def add_assessment_row_old(self, file, table_dict):
        """Imports and simulates a file, computes metrics and appends them to table_dict."""
        net = self.backend.load_network(file)
        self.backend.run_network(net, enforce_q_lims=True, delta_q=0.)
        values = self.backend.get_data_network(net, self.data_structure)
        for key, metrics in self.metrics_dict.items():
            table_dict[key].append(metrics(values))

    def add_assessment_row(self, file, df_dict):
        """Imports and simulates a file, computes metrics and appends them to table_dict."""
        net = self.backend.load_network(file)
        sample_name = os.path.splitext(os.path.basename(file))[0]
        self.backend.run_network(net, enforce_q_lims=True, delta_q=0.)
        values = self.backend.get_data_network(net,
                                               feature_names=self.feature_names,
                                               address_names=self.address_names,
                                               address_to_int=False)
        for key, metrics in self.metrics_dict.items():
            metrics_val, metrics_col = metrics(values)
            r = pd.DataFrame([metrics_val], columns=[metrics_col], index=[sample_name])
            df_dict[key] = pd.concat([df_dict[key], r])

