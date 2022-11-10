import numpy as np

from panoramix.problems.interface import AbstractProblem
from ml4ps import PandaPowerBackend


class PandaPowerVoltageControl(AbstractProblem):
    """"""

    name = "PandaPowerVoltageControl"
    backend = PandaPowerBackend()
    data_structure = {
        'bus': ['res_vm_pu', 'max_vm_pu', 'min_vm_pu'],
        'gen': ['res_q_mvar', 'vm_pu', 'min_q_mvar', 'max_q_mvar', 'in_service'],
        'load': ['p_mw'],
        'line': ['res_pl_mw', 'res_loading_percent', 'in_service'],
        'trafo': ['res_pl_mw', 'res_loading_percent']
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
            "Snapshots with Illicit Voltages": snapshots_illicit_voltages,
            "Bus Over Voltage": over_voltage,
            "Bus Under Voltage": under_voltage,
            "Bus Illicit Voltage": illicit_voltage,
            "Line Loading Percent (%)": line_loading_percent,
            "Transformer Loading Percent (%)": trafo_loading_percent,
            "Branch Overloading": over_current,
            "Generation Reactive Power (MVAr)": generation_reactive_power,
            "Generation Voltage Set Points (p.u.)": generation_voltage_setpoint,
            "Line N-1": line_n1,
            "Line N-2": line_n2,
            "Gen N-1": gen_n1,
            "Gen N-2": gen_n2,
            "Line in Service": line_in_service,
            "Gen in Service": gen_in_service,
        }


def snapshots_illicit_voltages(values):
    illicit_bus_voltages = illicit_voltage(values)
    return illicit_bus_voltages.any()


def line_in_service(values):
    return values['line']['in_service'] == 1.


def gen_in_service(values):
    return values['gen']['in_service'] == 1.


def line_n1(values):
    df = values['line']['in_service']
    false_count = len(df) - df.sum()
    return false_count == 1


def line_n2(values):
    df = values['line']['in_service']
    false_count = len(df) - df.sum()
    return false_count == 2


def gen_n1(values):
    df = values['gen']['in_service']
    false_count = len(df) - df.sum()
    return false_count == 1


def gen_n2(values):
    df = values['gen']['in_service']
    false_count = len(df) - df.sum()
    return false_count == 2


def line_joule_losses(values):
    return values['line']['res_pl_mw']

def trafo_joule_losses(values):
    return values['trafo']['res_pl_mw']

def total_joule_losses(values):
    return np.sum(values['line']['res_pl_mw']) + np.sum(values['trafo']['res_pl_mw'])

def normalized_joule_losses(values):
    total_joule = np.sum(values['line']['res_pl_mw']) + np.sum(values['trafo']['res_pl_mw'])
    total_load = np.sum(values['load']['p_mw'])
    return total_joule / total_load

def bus_voltage(values):
    return values['bus']['res_vm_pu']

def normalized_bus_voltage(values):
    v = values['bus']['res_vm_pu']
    v_min = values['bus']['min_vm_pu']
    v_max = values['bus']['max_vm_pu']
    return (v-v_min) / (v_max - v_min)

def over_voltage(values):
    return values['bus']['res_vm_pu'] > values['bus']['max_vm_pu']

def under_voltage(values):
    return values['bus']['res_vm_pu'] < values['bus']['min_vm_pu']

def illicit_voltage(values):
    return over_voltage(values) | under_voltage(values)

def line_loading_percent(values):
    return values['line']['res_loading_percent']

def trafo_loading_percent(values):
    return values['trafo']['res_loading_percent']

def normalized_branch_current(values):
    line_normalized_branch_current = values['line']['res_loading_percent'] / 100.
    trafo_normalized_branch_current = values['trafo']['res_loading_percent'] / 100.
    return np.concatenate([line_normalized_branch_current, trafo_normalized_branch_current])

def over_current(values):
    line_over_current = line_loading_percent(values) > 100
    trafo_over_current = trafo_loading_percent(values) > 100
    return np.concatenate([line_over_current, trafo_over_current])

def generation_reactive_power(values):
    return values['gen']['res_q_mvar']

def normalized_generation_reactive_power(values):
    q = values['gen']['res_q_mvar']
    q_min = values['gen']['min_q_mvar']
    q_max = values['gen']['max_q_mvar']
    return (q - q_min) / (q_max - q_min)

def generation_voltage_setpoint(values):
    return values['gen']['vm_pu']
