from abc import ABC, abstractmethod


class AbstractProblem(ABC):
    """"""

    def __init__(self):
        """"""
        pass

    @property
    @abstractmethod
    def name(self):
        """Problem name. Should be overridden."""
        pass

    @property
    @abstractmethod
    def backend(self):
        """ML4PS backend. Should be overridden."""
        pass

    @property
    @abstractmethod
    def data_structure(self):
        """Data structure that should be extracted from the network by the backend. Should be overridden."""
        pass

    @property
    @abstractmethod
    def metrics_dict(self):
        """Dictionary of metrics functions. Should be overridden."""
        pass

    def initialize_table_dict(self):
        """Initializes the dictionary of assessment tables."""
        return {key: [] for key in self.metrics_dict.keys()}

    def add_assessment_row(self, file, table_dict):
        """Imports and simulates a file, computes metrics and appends them to table_dict."""
        net = self.backend.load_network(file)
        self.backend.run_network(net, enforce_q_lims=True, delta_q=0.)
        values = self.backend.get_data_network(net, self.data_structure)
        for key, metrics in self.metrics_dict.items():
            table_dict[key].append(metrics(values))
