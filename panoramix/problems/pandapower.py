import numpy as np

from panoramix.problems.interface import AbstractProblem
from ml4ps import PandaPowerBackend


class PandaPowerVoltageControl(AbstractProblem):
    """"""

    backend = PandaPowerBackend()
    feature_names = {
        'bus': ['res_vm_pu', 'max_vm_pu', 'min_vm_pu'],
        'gen': ['res_q_mvar', 'vm_pu', 'min_q_mvar', 'max_q_mvar', 'in_service'],
        'ext_grid': ['res_q_mvar', 'vm_pu', 'min_q_mvar', 'max_q_mvar', 'in_service'],
        'load': ['p_mw'],
        'line': ['res_pl_mw', 'res_loading_percent', 'in_service'],
        'trafo': ['res_pl_mw', 'res_loading_percent']
    }
    address_names = {
        'bus': ['name'],
        'gen': ['bus', 'name'],
        'ext_grid': ['bus', 'name'],
        'load': ['bus', 'name'],
        'line': ['from_bus', 'to_bus', 'name'],
        'trafo': ['hv_bus', 'lv_bus', 'name']
    }
    metrics_dict = {}

    def __init__(self):
        """"""
        super().__init__()
        self.metrics_dict = {
            # Voltage set points
            "Generation Voltage Set Points (p.u.)": generation_voltage_setpoint,
            # Joule losses
            "Line Joule Losses (MW)": line_joule_losses,
            "Transformer Joule Losses (MW)": trafo_joule_losses,
            "Total Joule Losses (MW)": total_joule_losses,
            "Normalized Joule Losses": normalized_joule_losses,
            # Bus voltages
            "Bus Voltage (p.u.)": bus_voltage,
            "Bus Normalized Voltage": bus_normalized_voltage,
            "Buses with Over Voltage": bus_over_voltage,
            "Buses with Under Voltage": bus_under_voltage,
            "Buses with Illicit Voltage": bus_illicit_voltage,
            "Buses with Illicit Voltage, eps=0.05": bus_illicit_voltage_005,
            "Buses with Illicit Voltage, eps=0.1": bus_illicit_voltage_01,
            "Snapshots with Illicit Voltage": snapshots_illicit_voltage,
            "Snapshots with Illicit Voltage, eps=0.05": snapshots_illicit_voltage_005,
            "Snapshots with Illicit Voltage, eps=0.1": snapshots_illicit_voltage_01,
            # Branch loading
            "Line Loading Percent (%)": line_loading_percent,
            "Transformer Loading Percent (%)": trafo_loading_percent,
            "Branch Normalized Current": branch_normalized_current,
            "Branches with Illicit Current": branch_illicit_current,
            "Branches with Illicit Current, eps=0.05": branch_illicit_current_005,
            "Branches with Illicit Current, eps=0.1": branch_illicit_current_01,
            "Snapshots with Illicit Current": snapshots_illicit_current,
            "Snapshots with Illicit Current, eps=0.05": snapshots_illicit_current_005,
            "Snapshots with Illicit Current, eps=0.1": snapshots_illicit_current_01,
            # Reactive Generation
            "Generator Reactive Power (MVAr)": generator_reactive_power,
            "Generator Normalized Reactive Power": generator_normalized_reactive_power,
            "Generators with Over Reactive Power": generator_over_reactive_power,
            "Generators with Under Reactive Power": generator_under_reactive_power,
            "Generators with Illicit Reactive Power": generator_illicit_reactive_power,
            "Generators with Illicit Reactive Power, eps=0.05": generator_illicit_reactive_power_005,
            "Generators with Illicit Reactive Power, eps=0.1": generator_illicit_reactive_power_01,
            "Snapshots with Illicit Reactive Power": snapshots_illicit_reactive_power,
            "Snapshots with Illicit Reactive Power, eps=0.05": snapshots_illicit_reactive_power_005,
            "Snapshots with Illicit Reactive Power, eps=0.1": snapshots_illicit_reactive_power_01,
            # Illicit Snapshots
            "Snapshots with Illicit Values": snapshots_illicit_values,
            "Snapshots with Illicit Values, eps=0.05": snapshots_illicit_values_005,
            "Snapshots with Illicit Values, eps=0.1": snapshots_illicit_values_01,
            # Object disconnections
            "Line N-1": line_n1,
            "Line N-2": line_n2,
            "Gen N-1": gen_n1,
            "Gen N-2": gen_n2,
            "Line in Service": line_in_service,
            "Gen in Service": gen_in_service,
        }


def generation_voltage_setpoint(values):
    """Voltage set points in per-unit at all generators and ext_grids."""
    gen_values, gen_names = values['gen']['vm_pu'], values['gen']['name']
    ext_grid_values, ext_grid_names = values['ext_grid']['vm_pu'], values['ext_grid']['name']
    return np.concatenate([gen_values, ext_grid_values]), np.concatenate([gen_names, ext_grid_names])


def line_joule_losses(values):
    """Joule losses in MW at all transmission lines."""
    return values['line']['res_pl_mw'], values['line']['name']


def trafo_joule_losses(values):
    """Joule losses in MW at all transformer."""
    return values['trafo']['res_pl_mw'], values['trafo']['name']


def total_joule_losses(values):
    """Total Joule losses in MW summed over the power grid."""
    return np.sum(values['line']['res_pl_mw']) + np.sum(values['trafo']['res_pl_mw']), '0'


def normalized_joule_losses(values):
    """Total Joule losses summed over the power grid, divided by the total consumption."""
    total_joule = np.sum(values['line']['res_pl_mw']) + np.sum(values['trafo']['res_pl_mw'])
    total_load = np.sum(values['load']['p_mw'])
    return total_joule / total_load, '0'


def bus_voltage(values):
    """Bus voltages in per-unit."""
    return values['bus']['res_vm_pu'], values['bus']['name']


def bus_normalized_voltage(values):
    """Bus voltages normalized by their min-max range. (0=min, 1=max)"""
    v = values['bus']['res_vm_pu']
    v_min = values['bus']['min_vm_pu']
    v_max = values['bus']['max_vm_pu']
    return (v - v_min) / (v_max - v_min), values['bus']['name']


def bus_over_voltage(values):
    """Buses whose voltages are above their maximal authorized value."""
    v_normalized, bus_name = bus_normalized_voltage(values)
    return v_normalized > 1., bus_name


def bus_under_voltage(values):
    """Buses whose voltages are below their minimal authorized value."""
    v_normalized, bus_name = bus_normalized_voltage(values)
    return v_normalized < 0., bus_name


def bus_illicit_voltage(values):
    """Buses whose voltages are out of their authorized range."""
    v_over, bus_name = bus_over_voltage(values)
    v_under, bus_name = bus_under_voltage(values)
    return v_over | v_under, bus_name


def bus_illicit_voltage_005(values):
    """Buses whose voltages are out of their authorized range, with 5% less on both sides."""
    v_normalized, bus_name = bus_normalized_voltage(values)
    return (v_normalized < 0.05) | (v_normalized > 0.95), bus_name


def bus_illicit_voltage_01(values):
    """Buses whose voltages are out of their authorized range, with 1O% less on both sides."""
    v_normalized, bus_name = bus_normalized_voltage(values)
    return (v_normalized < 0.1) | (v_normalized > 0.9), bus_name


def snapshots_illicit_voltage(values):
    """Snapshots with at least one illicit voltage."""
    illicit_bus_voltages, _ = bus_illicit_voltage(values)
    return illicit_bus_voltages.any(), '0'


def snapshots_illicit_voltage_005(values):
    """Snapshots with at least one illicit voltage, with a range 5% smaller on both sides."""
    illicit_bus_voltages, _ = bus_illicit_voltage_005(values)
    return illicit_bus_voltages.any(), '0'


def snapshots_illicit_voltage_01(values):
    """Snapshots with at least one illicit voltage, with a range 10% smaller on both sides."""
    illicit_bus_voltages, _ = bus_illicit_voltage_01(values)
    return illicit_bus_voltages.any(), '0'


def line_loading_percent(values):
    """Line loading percentage, 100 corresponds to a fully loaded line."""
    return values['line']['res_loading_percent'], values['line']['name']


def trafo_loading_percent(values):
    """Trafo loading percentage, 100 corresponds to a fully loaded line."""
    return values['trafo']['res_loading_percent'], values['trafo']['name']


def branch_normalized_current(values):
    """Branch normalized current."""
    line = values['line']['res_loading_percent'] / 100.
    trafo = values['trafo']['res_loading_percent'] / 100.
    return np.concatenate([line, trafo]), np.concatenate([values['line']['name'], values['trafo']['name']])


def branch_illicit_current(values):
    """Branches with illicit currents w.r.t. their thermal limits."""
    i_normalized, branch_name = branch_normalized_current(values)
    return i_normalized > 1., branch_name


def branch_illicit_current_005(values):
    """Branches with illicit currents w.r.t. 95% of their thermal limits."""
    i_normalized, branch_name = branch_normalized_current(values)
    return i_normalized > 0.95, branch_name


def branch_illicit_current_01(values):
    """Branches with illicit currents w.r.t. 90% of their thermal limits."""
    i_normalized, branch_name = branch_normalized_current(values)
    return i_normalized > 0.9, branch_name


def snapshots_illicit_current(values):
    """Snapshots with at least one illicit current."""
    illicit_current, _ = branch_illicit_current(values)
    return illicit_current.any(), "0"


def snapshots_illicit_current_005(values):
    """Snapshots with at least one illicit current, with a range 5% smaller on both sides."""
    illicit_current, _ = branch_illicit_current_005(values)
    return illicit_current.any(), "0"


def snapshots_illicit_current_01(values):
    """Snapshots with at least one illicit current, with a range 10% smaller on both sides."""
    illicit_current, _ = branch_illicit_current_01(values)
    return illicit_current.any(), "0"


def generator_reactive_power(values):
    """Generator reactive power in MW."""
    return np.concatenate([values['gen']['res_q_mvar'], values['ext_grid']['res_q_mvar']]), \
        np.concatenate([values['gen']['name'], values['ext_grid']['name']])


def generator_normalized_reactive_power(values):
    """Generator reactive power normalized by their min-max range. (0=min, 1=max)"""
    q = np.concatenate([values['gen']['res_q_mvar'], values['ext_grid']['res_q_mvar']])
    q_min = np.concatenate([values['gen']['min_q_mvar'], values['ext_grid']['min_q_mvar']])
    q_max = np.concatenate([values['gen']['max_q_mvar'], values['ext_grid']['max_q_mvar']])
    return (q - q_min) / (q_max - q_min), np.concatenate([values['gen']['name'], values['ext_grid']['name']])


def generator_over_reactive_power(values):
    """Generators with a reactive power larger than their maximal authorized value."""
    q_normalized, gen_name = bus_normalized_voltage(values)
    return q_normalized > 1., gen_name


def generator_under_reactive_power(values):
    """Generators with a reactive power smaller than their minimal authorized value."""
    q_normalized, gen_name = bus_normalized_voltage(values)
    return q_normalized < 0., gen_name


def generator_illicit_reactive_power(values):
    """Generators with reactive power out of their authorized value."""
    q_normalized, gen_name = bus_normalized_voltage(values)
    return (q_normalized < 0.) | (q_normalized > 1.), gen_name


def generator_illicit_reactive_power_005(values):
    """Generators with reactive power out of their authorized value, with a range 5% smaller on both sides."""
    q_normalized, gen_name = bus_normalized_voltage(values)
    return (q_normalized < 0.05) | (q_normalized > 0.95), gen_name


def generator_illicit_reactive_power_01(values):
    """Generators with reactive power out of their authorized value, with a range 10% smaller on both sides."""
    q_normalized, gen_name = bus_normalized_voltage(values)
    return (q_normalized < 0.1) | (q_normalized > 0.9), gen_name


def snapshots_illicit_reactive_power(values):
    """Snapshots with at least one illicit reactive power."""
    illicit_reactive_power, _ = generator_illicit_reactive_power(values)
    return illicit_reactive_power.any(), "0"


def snapshots_illicit_reactive_power_005(values):
    """Snapshots with at least one illicit reactive power, with a range 5% smaller on both sides."""
    illicit_reactive_power, _ = generator_illicit_reactive_power_005(values)
    return illicit_reactive_power.any(), "0"


def snapshots_illicit_reactive_power_01(values):
    """Snapshots with at least one illicit reactive power, with a range 10% smaller on both sides."""
    illicit_reactive_power, _ = generator_illicit_reactive_power_01(values)
    return illicit_reactive_power.any(), "0"


def snapshots_illicit_values(values):
    """Snapshot with at least one illicit value."""
    v, _ = snapshots_illicit_current(values)
    i, _ = snapshots_illicit_current(values)
    q, _ = snapshots_illicit_reactive_power(values)
    return v | i | q, '0'


def snapshots_illicit_values_005(values):
    """Snapshot with at least one illicit value, with a range 5% smaller on both sides."""
    v, _ = snapshots_illicit_current_005(values)
    i, _ = snapshots_illicit_current_005(values)
    q, _ = snapshots_illicit_reactive_power_005(values)
    return v | i | q, '0'


def snapshots_illicit_values_01(values):
    """Snapshot with at least one illicit value, with a range 1O% smaller on both sides."""
    v, _ = snapshots_illicit_current_01(values)
    i, _ = snapshots_illicit_current_01(values)
    q, _ = snapshots_illicit_reactive_power_01(values)
    return v | i | q, '0'


def line_n1(values):
    """Snapshots with 1 disconnected line."""
    df = values['line']['in_service']
    false_count = len(df) - df.sum()
    return false_count == 1, '0'


def line_n2(values):
    """Snapshots with 2 disconnected lines."""
    df = values['line']['in_service']
    false_count = len(df) - df.sum()
    return false_count == 2, '0'


def gen_n1(values):
    """Snapshots with 1 disconnected generator."""
    df = values['gen']['in_service']
    false_count = len(df) - df.sum()
    return false_count == 1, '0'


def gen_n2(values):
    """Snapshots with 2 disconnected generators."""
    df = values['gen']['in_service']
    false_count = len(df) - df.sum()
    return false_count == 2, '0'


def line_in_service(values):
    """Lines that are in service."""
    return values['line']['in_service'] == 1., values['line']['name']


def gen_in_service(values):
    """Generators that are in service."""
    return values['gen']['in_service'] == 1., values['gen']['name']
