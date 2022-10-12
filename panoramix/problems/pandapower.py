import numpy as np

from panoramix.problems.interface import AbstractProblem
from ml4ps import PandaPowerBackend


class PandaPowerVoltageControl(AbstractProblem):
    """"""

    name = "PandaPowerVoltageControl"
    backend = PandaPowerBackend()
    data_structure = {
        'bus': {"feature_names": ['res_vm_pu', 'max_vm_pu', 'min_vm_pu']},
        'gen': {"feature_names": ['res_q_mvar', 'vm_pu']},
        'load': {"feature_names": ['p_mw']},
        'line': {"feature_names": ['res_pl_mw', 'res_loading_percent']},
        'trafo': {"feature_names": ['res_pl_mw', 'res_loading_percent']}
    }
    metrics_dict = {}

    def __init__(self):
        """"""
        super().__init__()
        self.metrics_dict = {
            "Line Joule Losses (MW)": line_joule_losses,
            "Transformer Joule Losses (MW)": trafo_joule_losses,
            "Total Joule Losses (MW)": total_joule_losses,
            "Normalized Joule Losses": normalized_joule_losses,
            "Bus Voltage (p.u.)": bus_voltage,
            "Bus Over Voltage": over_voltage,
            "Bus Under Voltage": under_voltage,
            "Bus Illicit Voltage": illicit_voltage,
            "Line Loading Percent (%)": line_loading_percent,
            "Transformer Loading Percent (%)": trafo_loading_percent,
            "Branch Overloading": over_current,
            "Generation Reactive Power (MVAr)": generation_reactive_power,
            "Generation Voltage Set Points (p.u.)": generation_voltage_setpoint
        }


def line_joule_losses(values):
    return values['line']['features']['res_pl_mw']

def trafo_joule_losses(values):
    return values['trafo']['features']['res_pl_mw']

def total_joule_losses(values):
    return np.sum(values['line']['features']['res_pl_mw']) + np.sum(values['trafo']['features']['res_pl_mw'])

def normalized_joule_losses(values):
    total_joule = np.sum(values['line']['features']['res_pl_mw']) + np.sum(values['trafo']['features']['res_pl_mw'])
    total_load = np.sum(values['load']['features']['p_mw'])
    return total_joule / total_load

def bus_voltage(values):
    return values['bus']['features']['res_vm_pu']

def over_voltage(values):
    return values['bus']['features']['res_vm_pu'] > values['bus']['features']['max_vm_pu']

def under_voltage(values):
    return values['bus']['features']['res_vm_pu'] < values['bus']['features']['min_vm_pu']

def illicit_voltage(values):
    return over_voltage(values) | under_voltage(values)

def line_loading_percent(values):
    return values['line']['features']['res_loading_percent']

def trafo_loading_percent(values):
    return values['trafo']['features']['res_loading_percent']

def over_current(values):
    line_over_current = line_loading_percent(values) > 100
    trafo_over_current = trafo_loading_percent(values) > 100
    return np.concatenate([line_over_current, trafo_over_current])

def generation_reactive_power(values):
    return values['gen']['features']['res_q_mvar']

def generation_voltage_setpoint(values):
    return values['gen']['features']['vm_pu']
