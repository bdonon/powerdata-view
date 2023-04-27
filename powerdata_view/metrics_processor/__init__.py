from powerdata_view.metrics_processor.interface import MetricsProcessorInterface
from powerdata_view.metrics_processor.pandapower import PandaPowerMetricsProcessor
from powerdata_view.metrics_processor.pypowsybl import PyPowSyblMetricsProcessor


def get_metrics_processor(identifier):
    if identifier == 'PandaPowerMetricsProcessor':
        return PandaPowerMetricsProcessor()
    elif identifier == 'PyPowSyblMetricsProcessor':
        return PyPowSyblMetricsProcessor()
    else:
        raise NotImplementedError
