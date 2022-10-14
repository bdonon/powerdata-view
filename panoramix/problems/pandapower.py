import numpy as np

from panoramix.problems.interface import AbstractProblem
from ml4ps import PandaPowerBackend


class PandaPowerVoltageControl(AbstractProblem):
    """"""

    name = "PandaPowerVoltageControl"
    backend = PandaPowerBackend()
    data_structure = {
        'bus': {"feature_names": ['res_vm_pu', 'max_vm_pu', 'min_vm_pu']},
        'gen': {"feature_names": ['res_q_mvar', 'vm_pu', 'min_q_mvar', 'max_q_mvar']},
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
            "Normalized Bus Voltage": normalized_bus_voltage,
            "Normalized Branch Current": normalized_branch_current,
            "Normalized Reactive Generation": normalized_generation_reactive_power,
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

def normalized_bus_voltage(values):
    v = values['bus']['features']['res_vm_pu']
    v_min = values['bus']['features']['min_vm_pu']
    v_max = values['bus']['features']['max_vm_pu']
    return (v-v_min) / (v_max - v_min)

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

def normalized_branch_current(values):
    line_normalized_branch_current = values['line']['features']['res_loading_percent'] / 100.
    trafo_normalized_branch_current = values['trafo']['features']['res_loading_percent'] / 100.
    return np.concatenate([line_normalized_branch_current, trafo_normalized_branch_current])

def over_current(values):
    line_over_current = line_loading_percent(values) > 100
    trafo_over_current = trafo_loading_percent(values) > 100
    return np.concatenate([line_over_current, trafo_over_current])

def generation_reactive_power(values):
    return values['gen']['features']['res_q_mvar']

def normalized_generation_reactive_power(values):
    q = values['gen']['features']['res_q_mvar']
    q_min = values['gen']['features']['min_q_mvar']
    q_max = values['gen']['features']['max_q_mvar']
    return (q - q_min) / (q_max - q_min)

def generation_voltage_setpoint(values):
    return values['gen']['features']['vm_pu']
