from abc import ABC
import pandapower as pp
import numpy as np
from powerdata_view.metrics_processor.interface import MetricsProcessorInterface


class PandaPowerMetricsProcessor(MetricsProcessorInterface, ABC):
    """Metrics Processor that relies on `PandaPower <http://www.pandapower.org>`_."""

    metrics_dict = {}

    def __init__(self):
        super().__init__()
        self.metrics_dict = {

            # Voltage set points
            "Generation Voltage Set Points (p.u.)": generation_voltage_setpoint,

            # Joule losses
            "Line Joule Losses (MW)": line_joule_losses,
            "Transformer Joule Losses (MW)": trafo_joule_losses,
            "Total Joule Losses (MW)": total_joule_losses,
            "Normalized Joule Losses": normalized_joule_losses,

            # Shunt actions
            "Shunt Steps": shunt_steps,
            "Shunt Steps Normalized": shunt_steps_normalized,

            # Load consumption
            "Load Active Power (MW)": load_active_power,
            "Load Total Active Power (MW)": load_total_active_power,
            "Load Reactive Power (MVAr)": load_reactive_power,
            "Load Total Reactive Power (MVAr)": load_total_reactive_power,
            "Load Power Factor": load_power_factor,

            # Bus voltages
            "Bus Voltage (p.u.)": bus_voltage,
            "Bus Normalized Voltage": bus_normalized_voltage,
            "Buses with Over Voltage": bus_over_voltage,
            "Buses with Under Voltage": bus_under_voltage,
            "Buses with Illicit Voltage": bus_illicit_voltage,
            "Buses with Illicit Voltage, eps=0.05": bus_illicit_voltage_005,
            "Buses with Illicit Voltage, eps=0.1": bus_illicit_voltage_01,
            "Buses with Illicit Voltage, eps=0.25": bus_illicit_voltage_025,
            "Buses with Illicit Voltage, eps=-0.05": bus_illicit_voltage_m005,
            "Buses with Illicit Voltage, eps=-0.1": bus_illicit_voltage_m01,
            "Snapshots with Illicit Voltage": snapshots_illicit_voltage,
            "Snapshots with Illicit Voltage, eps=0.05": snapshots_illicit_voltage_005,
            "Snapshots with Illicit Voltage, eps=0.1": snapshots_illicit_voltage_01,
            "Snapshots with Illicit Voltage, eps=0.25": snapshots_illicit_voltage_025,
            "Snapshots with Illicit Voltage, eps=-0.05": snapshots_illicit_voltage_m005,
            "Snapshots with Illicit Voltage, eps=-0.1": snapshots_illicit_voltage_m01,
            "Voltage Violation Count per Snapshot": voltage_violation_count,

            # Branch loading
            "Line Loading Percent (%)": line_loading_percent,
            "Transformer Loading Percent (%)": trafo_loading_percent,
            "Branch Normalized Current": branch_normalized_current,
            "Branches with Illicit Current": branch_illicit_current,
            "Branches with Illicit Current, eps=0.05": branch_illicit_current_005,
            "Branches with Illicit Current, eps=0.1": branch_illicit_current_01,
            "Branches with Illicit Current, eps=-0.05": branch_illicit_current_m005,
            "Branches with Illicit Current, eps=-0.1": branch_illicit_current_m01,
            "Snapshots with Illicit Current": snapshots_illicit_current,
            "Snapshots with Illicit Current, eps=0.05": snapshots_illicit_current_005,
            "Snapshots with Illicit Current, eps=0.1": snapshots_illicit_current_01,
            "Snapshots with Illicit Current, eps=-0.05": snapshots_illicit_current_m005,
            "Snapshots with Illicit Current, eps=-0.1": snapshots_illicit_current_m01,
            "Current Violation Count per Snapshot": current_violation_count,

            # Reactive Generation
            "Generator Active Power (MW)": generator_active_power,
            "Generator Total Active Power (MW)": generator_total_active_power,
            "Generator Reactive Power (MVAr)": generator_reactive_power,
            "Generator Total Reactive Power (MVAr)": generator_total_reactive_power,
            "Generator Normalized Reactive Power": generator_normalized_reactive_power,
            "Generators with Over Reactive Power": generator_over_reactive_power,
            "Generators with Under Reactive Power": generator_under_reactive_power,
            "Generators with Illicit Reactive Power": generator_illicit_reactive_power,
            "Generators with Illicit Reactive Power, eps=0.05": generator_illicit_reactive_power_005,
            "Generators with Illicit Reactive Power, eps=0.1": generator_illicit_reactive_power_01,
            "Generators with Illicit Reactive Power, eps=-0.05": generator_illicit_reactive_power_m005,
            "Generators with Illicit Reactive Power, eps=-0.1": generator_illicit_reactive_power_m01,
            "Snapshots with Illicit Reactive Power": snapshots_illicit_reactive_power,
            "Snapshots with Illicit Reactive Power, eps=0.05": snapshots_illicit_reactive_power_005,
            "Snapshots with Illicit Reactive Power, eps=0.1": snapshots_illicit_reactive_power_01,
            "Reactive Violation Count per Snapshot": reactive_violation_count,

            # Illicit Snapshots
            "Snapshots with Illicit Values": snapshots_illicit_power_grid,
            "Snapshots with Illicit Values, eps=0.05": snapshots_illicit_power_grid_005,
            "Snapshots with Illicit Values, eps=0.1": snapshots_illicit_power_grid_01,
            "Snapshots with Illicit Values, eps=-0.05": snapshots_illicit_power_grid_m005,
            "Snapshots with Illicit Values, eps=-0.1": snapshots_illicit_power_grid_m01,
            "Violation Count per Snapshot": violation_count,

            # Costs
            "Current Cost": current_cost,
            "Voltage Cost": voltage_cost,
            "Reactive Cost": reactive_cost,
            "Joule Cost": joule_cost,
            "Cost": cost,

            # Object disconnections
            "Line N-1": line_n1,
            "Line N-2": line_n2,
            "Branch In Service Count": branch_in_service_count,
            "Generators N-1": gen_n1,
            "Generators N-2": gen_n2,
            "Generators In Service Count": generator_in_service_count,
            "Line in Service": line_in_service,
            "Transformer in Service": trafo_in_service,
            "Gen in Service": gen_in_service,
        }

    def run_powerflow(self, power_grid):
        """AC-PowerFlow implementation of Pandapower. Enforces reactive limits.

        Overrides run_powerflow of abstract base class.
        """
        pp.runpp(power_grid, init='results', enforce_q_lims=True, delta_q=0.)

    def load_power_grid(self, filepath):
        """Loads a power grid in memory.

        Overrides load_power_grid of abstract base class.
        """
        return pp.from_json(filepath)


def generation_voltage_setpoint(power_grid):
    """Voltage set points in per-unit at all generators and ext_grids."""
    gen_on = power_grid.gen.in_service
    gen_power_grid = power_grid.gen.vm_pu.loc[gen_on].values
    gen_names = power_grid.gen.name.loc[gen_on].values
    ext_grid_on = power_grid.ext_grid.in_service
    ext_grid_power_grid = power_grid.ext_grid.vm_pu.loc[ext_grid_on].values
    ext_grid_names = power_grid.ext_grid.name.loc[ext_grid_on].values
    return np.concatenate([gen_power_grid, ext_grid_power_grid]), np.concatenate([gen_names, ext_grid_names])


def line_joule_losses(power_grid):
    """Joule losses in MW at all transmission lines."""
    return power_grid.res_line.pl_mw.values, power_grid.line.name.values


def trafo_joule_losses(power_grid):
    """Joule losses in MW at all transformer."""
    return power_grid.res_trafo.pl_mw.values, power_grid.trafo.name.values


def total_joule_losses(power_grid):
    """Total Joule losses in MW summed over the power grid."""
    return np.sum(power_grid.res_line.pl_mw.values) + np.sum(power_grid.res_trafo.pl_mw.values), '0'


def normalized_joule_losses(power_grid):
    """Total Joule losses summed over the power grid, divided by the total consumption."""
    total_joule = np.sum(power_grid.res_line.pl_mw.values) + np.sum(power_grid.res_trafo.pl_mw.values)
    total_load = np.sum(power_grid.load.p_mw.values)
    return total_joule / total_load, '0'


def shunt_steps(power_grid):
    """Shunt steps."""
    steps = power_grid.shunt.step.values * 1.
    names = power_grid.shunt.name.values
    return steps, names


def shunt_steps_normalized(power_grid):
    """Shunt steps divided by max step."""
    steps = power_grid.shunt.step.values
    max_steps = power_grid.shunt.max_step.values
    names = power_grid.shunt.name.values
    return steps / max_steps, names


def load_active_power(power_grid):
    """Active power load."""
    return power_grid.load.p_mw.values, power_grid.load.name.values


def load_total_active_power(power_grid):
    """Sum of active load per snapshot."""
    return np.nansum(power_grid.load.p_mw.values), '0'


def load_reactive_power(power_grid):
    """Reactive power load."""
    return power_grid.load.q_mvar.values, power_grid.load.name.values


def load_total_reactive_power(power_grid):
    """Sum of reactive power load per snapshot."""
    return np.nansum(power_grid.load.q_mvar.values), '0'


def load_power_factor(power_grid):
    """Load power factor."""
    p = power_grid.load.p_mw.values
    q = power_grid.load.q_mvar.values
    s = np.sqrt(p**2 + q**2)
    pf = p / s
    return pf, power_grid.load.name.values


def bus_voltage(power_grid):
    """Bus voltages in per-unit."""
    return power_grid.res_bus.vm_pu.values, power_grid.bus.name.values


def bus_normalized_voltage(power_grid):
    """Bus voltages normalized by their min-max range. (0=min, 1=max)"""
    v = power_grid.res_bus.vm_pu.values
    v_min = power_grid.bus.min_vm_pu.values
    v_max = power_grid.bus.max_vm_pu.values
    return (v - v_min) / (v_max - v_min + 1e-4), power_grid.bus.name.values


def bus_over_voltage(power_grid):
    """Buses whose voltages are above their maximal authorized value."""
    v_normalized, bus_name = bus_normalized_voltage(power_grid)
    return v_normalized > 1., bus_name


def bus_under_voltage(power_grid):
    """Buses whose voltages are below their minimal authorized value."""
    v_normalized, bus_name = bus_normalized_voltage(power_grid)
    return v_normalized < 0., bus_name


def bus_illicit_voltage(power_grid):
    """Buses whose voltages are out of their authorized range."""
    v_over, bus_name = bus_over_voltage(power_grid)
    v_under, bus_name = bus_under_voltage(power_grid)
    return v_over | v_under, bus_name


def bus_illicit_voltage_005(power_grid):
    """Buses whose voltages are out of their authorized range, with 5% less on both sides."""
    v_normalized, bus_name = bus_normalized_voltage(power_grid)
    return (v_normalized < 0.05) | (v_normalized > 0.95), bus_name


def bus_illicit_voltage_01(power_grid):
    """Buses whose voltages are out of their authorized range, with 1O% less on both sides."""
    v_normalized, bus_name = bus_normalized_voltage(power_grid)
    return (v_normalized < 0.1) | (v_normalized > 0.9), bus_name

def bus_illicit_voltage_025(power_grid):
    """Buses whose voltages are out of their authorized range, with 1O% less on both sides."""
    v_normalized, bus_name = bus_normalized_voltage(power_grid)
    return (v_normalized < 0.25) | (v_normalized > 0.75), bus_name


def bus_illicit_voltage_m005(power_grid):
    """Buses whose voltages are out of their authorized range, with 5% more on both sides."""
    v_normalized, bus_name = bus_normalized_voltage(power_grid)
    return (v_normalized < -0.05) | (v_normalized > 1.05), bus_name


def bus_illicit_voltage_m01(power_grid):
    """Buses whose voltages are out of their authorized range, with 1O% more on both sides."""
    v_normalized, bus_name = bus_normalized_voltage(power_grid)
    return (v_normalized < -0.1) | (v_normalized > 1.1), bus_name


def snapshots_illicit_voltage(power_grid):
    """Snapshots with at least one illicit voltage."""
    illicit_bus_voltages, _ = bus_illicit_voltage(power_grid)
    return illicit_bus_voltages.any(), '0'


def snapshots_illicit_voltage_005(power_grid):
    """Snapshots with at least one illicit voltage, with a range 5% smaller on both sides."""
    illicit_bus_voltages, _ = bus_illicit_voltage_005(power_grid)
    return illicit_bus_voltages.any(), '0'


def snapshots_illicit_voltage_01(power_grid):
    """Snapshots with at least one illicit voltage, with a range 10% smaller on both sides."""
    illicit_bus_voltages, _ = bus_illicit_voltage_01(power_grid)
    return illicit_bus_voltages.any(), '0'

def snapshots_illicit_voltage_025(power_grid):
    """Snapshots with at least one illicit voltage, with a range 10% smaller on both sides."""
    illicit_bus_voltages, _ = bus_illicit_voltage_025(power_grid)
    return illicit_bus_voltages.any(), '0'


def snapshots_illicit_voltage_m005(power_grid):
    """Snapshots with at least one illicit voltage, with a range 5% smaller on both sides."""
    illicit_bus_voltages, _ = bus_illicit_voltage_m005(power_grid)
    return illicit_bus_voltages.any(), '0'


def snapshots_illicit_voltage_m01(power_grid):
    """Snapshots with at least one illicit voltage, with a range 10% smaller on both sides."""
    illicit_bus_voltages, _ = bus_illicit_voltage_m01(power_grid)
    return illicit_bus_voltages.any(), '0'


def voltage_violation_count(power_grid):
    """Counts the amount of voltage violations in each snapshot."""
    illicit_voltages, _ = bus_illicit_voltage(power_grid)
    return np.sum(illicit_voltages) * 1., '0'


def line_loading_percent(power_grid):
    """Line loading percentage, 100 corresponds to a fully loaded line."""
    return power_grid.res_line.loading_percent.values, power_grid.line.name.values


def trafo_loading_percent(power_grid):
    """Trafo loading percentage, 100 corresponds to a fully loaded line."""
    return power_grid.res_trafo.loading_percent.values, power_grid.trafo.name.values


def branch_normalized_current(power_grid):
    """Branch normalized current."""
    line = power_grid.res_line.loading_percent.values / 100.
    trafo = power_grid.res_trafo.loading_percent.values / 100.
    return np.concatenate([line, trafo]), np.concatenate([power_grid.line.name.values, power_grid.trafo.name.values])


def branch_illicit_current(power_grid):
    """Branches with illicit currents w.r.t. their thermal limits."""
    i_normalized, branch_name = branch_normalized_current(power_grid)
    return i_normalized > 1., branch_name


def branch_illicit_current_005(power_grid):
    """Branches with illicit currents w.r.t. 95% of their thermal limits."""
    i_normalized, branch_name = branch_normalized_current(power_grid)
    return i_normalized > 0.95, branch_name


def branch_illicit_current_01(power_grid):
    """Branches with illicit currents w.r.t. 90% of their thermal limits."""
    i_normalized, branch_name = branch_normalized_current(power_grid)
    return i_normalized > 0.9, branch_name


def branch_illicit_current_m005(power_grid):
    """Branches with illicit currents w.r.t. 105% of their thermal limits."""
    i_normalized, branch_name = branch_normalized_current(power_grid)
    return i_normalized > 1.05, branch_name


def branch_illicit_current_m01(power_grid):
    """Branches with illicit currents w.r.t. 110% of their thermal limits."""
    i_normalized, branch_name = branch_normalized_current(power_grid)
    return i_normalized > 1.1, branch_name


def snapshots_illicit_current(power_grid):
    """Snapshots with at least one illicit current."""
    illicit_current, _ = branch_illicit_current(power_grid)
    return illicit_current.any(), "0"


def snapshots_illicit_current_005(power_grid):
    """Snapshots with at least one illicit current, with a range 5% smaller on both sides."""
    illicit_current, _ = branch_illicit_current_005(power_grid)
    return illicit_current.any(), "0"


def snapshots_illicit_current_01(power_grid):
    """Snapshots with at least one illicit current, with a range 10% smaller on both sides."""
    illicit_current, _ = branch_illicit_current_01(power_grid)
    return illicit_current.any(), "0"


def snapshots_illicit_current_m005(power_grid):
    """Snapshots with at least one illicit current, with a range 5% smaller on both sides."""
    illicit_current, _ = branch_illicit_current_m005(power_grid)
    return illicit_current.any(), "0"


def snapshots_illicit_current_m01(power_grid):
    """Snapshots with at least one illicit current, with a range 10% smaller on both sides."""
    illicit_current, _ = branch_illicit_current_m01(power_grid)
    return illicit_current.any(), "0"


def current_violation_count(power_grid):
    """Counts the amount of current violations in each snapshot."""
    illicit_currents, _ = branch_illicit_current(power_grid)
    return np.sum(illicit_currents) * 1., '0'


def generator_active_power(power_grid):
    """Generator active power in MW."""
    return np.concatenate([power_grid.res_gen.p_mw.values, power_grid.res_ext_grid.p_mw.values]), \
        np.concatenate([power_grid.gen.name.values, power_grid.ext_grid.name.values])

def generator_total_active_power(power_grid):
    """Total generator active power in MW."""
    return np.nansum(np.concatenate([power_grid.res_gen.p_mw.values, power_grid.res_ext_grid.p_mw.values])), '0'

def generator_reactive_power(power_grid):
    """Generator reactive power in MVAr."""
    return np.concatenate([power_grid.res_gen.q_mvar.values, power_grid.res_ext_grid.q_mvar.values]), \
        np.concatenate([power_grid.gen.name.values, power_grid.ext_grid.name.values])


def generator_total_reactive_power(power_grid):
    """Total generator reactive power in MVAr."""
    return np.nansum(np.concatenate([power_grid.res_gen.q_mvar.values, power_grid.res_ext_grid.q_mvar.values])), '0'


def generator_normalized_reactive_power(power_grid):
    """Generator reactive power normalized by their min-max range. (0=min, 1=max)"""
    q = np.concatenate([power_grid.res_gen.q_mvar.values, power_grid.res_ext_grid.q_mvar.values])
    q_min = np.concatenate([power_grid.gen.min_q_mvar.values, power_grid.ext_grid.min_q_mvar.values])
    q_max = np.concatenate([power_grid.gen.max_q_mvar.values, power_grid.ext_grid.max_q_mvar.values])
    return (q - q_min) / (q_max - q_min), np.concatenate([power_grid.gen.name.values, power_grid.ext_grid.name.values])


def generator_over_reactive_power(power_grid):
    """Generators with a reactive power larger than their maximal authorized value."""
    q_normalized, gen_name = generator_normalized_reactive_power(power_grid)
    return q_normalized > 1., gen_name


def generator_under_reactive_power(power_grid):
    """Generators with a reactive power smaller than their minimal authorized value."""
    q_normalized, gen_name = generator_normalized_reactive_power(power_grid)
    return q_normalized < 0., gen_name


def generator_illicit_reactive_power(power_grid):
    """Generators with reactive power out of their authorized value."""
    q_normalized, gen_name = generator_normalized_reactive_power(power_grid)
    return (q_normalized < 0.) | (q_normalized > 1.), gen_name


def generator_illicit_reactive_power_005(power_grid):
    """Generators with reactive power out of their authorized value, with a range 5% smaller on both sides."""
    q_normalized, gen_name = generator_normalized_reactive_power(power_grid)
    return (q_normalized < 0.05) | (q_normalized > 0.95), gen_name


def generator_illicit_reactive_power_01(power_grid):
    """Generators with reactive power out of their authorized value, with a range 10% smaller on both sides."""
    q_normalized, gen_name = generator_normalized_reactive_power(power_grid)
    return (q_normalized < 0.1) | (q_normalized > 0.9), gen_name


def generator_illicit_reactive_power_m005(power_grid):
    """Generators with reactive power out of their authorized value, with a range 5% larger on both sides."""
    q_normalized, gen_name = generator_normalized_reactive_power(power_grid)
    return (q_normalized < -0.05) | (q_normalized > 1.05), gen_name


def generator_illicit_reactive_power_m01(power_grid):
    """Generators with reactive power out of their authorized value, with a range 10% larger on both sides."""
    q_normalized, gen_name = generator_normalized_reactive_power(power_grid)
    return (q_normalized < -0.1) | (q_normalized > 1.1), gen_name


def snapshots_illicit_reactive_power(power_grid):
    """Snapshots with at least one illicit reactive power."""
    illicit_reactive_power, _ = generator_illicit_reactive_power(power_grid)
    return illicit_reactive_power.any(), "0"


def snapshots_illicit_reactive_power_005(power_grid):
    """Snapshots with at least one illicit reactive power, with a range 5% smaller on both sides."""
    illicit_reactive_power, _ = generator_illicit_reactive_power_005(power_grid)
    return illicit_reactive_power.any(), "0"


def snapshots_illicit_reactive_power_01(power_grid):
    """Snapshots with at least one illicit reactive power, with a range 10% smaller on both sides."""
    illicit_reactive_power, _ = generator_illicit_reactive_power_01(power_grid)
    return illicit_reactive_power.any(), "0"


def reactive_violation_count(power_grid):
    """Counts the amount of reactive violations in each snapshot."""
    illicit_reactive, _ = generator_illicit_reactive_power(power_grid)
    return np.sum(illicit_reactive) * 1., '0'


def snapshots_illicit_reactive_power_m005(power_grid):
    """Snapshots with at least one illicit reactive power, with a range 5% smaller on both sides."""
    illicit_reactive_power, _ = generator_illicit_reactive_power_m005(power_grid)
    return illicit_reactive_power.any(), "0"


def snapshots_illicit_reactive_power_m01(power_grid):
    """Snapshots with at least one illicit reactive power, with a range 10% smaller on both sides."""
    illicit_reactive_power, _ = generator_illicit_reactive_power_m01(power_grid)
    return illicit_reactive_power.any(), "0"


def snapshots_illicit_power_grid(power_grid):
    """Snapshot with at least one illicit value."""
    v, _ = snapshots_illicit_voltage(power_grid)
    i, _ = snapshots_illicit_current(power_grid)
    q, _ = snapshots_illicit_reactive_power(power_grid)
    return v | i | q, '0'


def snapshots_illicit_power_grid_005(power_grid):
    """Snapshot with at least one illicit value, with a range 5% smaller on both sides."""
    v, _ = snapshots_illicit_voltage_005(power_grid)
    i, _ = snapshots_illicit_current_005(power_grid)
    q, _ = snapshots_illicit_reactive_power_005(power_grid)
    return v | i | q, '0'


def snapshots_illicit_power_grid_01(power_grid):
    """Snapshot with at least one illicit value, with a range 1O% smaller on both sides."""
    v, _ = snapshots_illicit_voltage_01(power_grid)
    i, _ = snapshots_illicit_current_01(power_grid)
    q, _ = snapshots_illicit_reactive_power_01(power_grid)
    return v | i | q, '0'


def snapshots_illicit_power_grid_m005(power_grid):
    """Snapshot with at least one illicit value, with a range 5% smaller on both sides."""
    v, _ = snapshots_illicit_voltage_m005(power_grid)
    i, _ = snapshots_illicit_current_m005(power_grid)
    q, _ = snapshots_illicit_reactive_power_m005(power_grid)
    return v | i | q, '0'


def snapshots_illicit_power_grid_m01(power_grid):
    """Snapshot with at least one illicit value, with a range 1O% smaller on both sides."""
    v, _ = snapshots_illicit_voltage_m01(power_grid)
    i, _ = snapshots_illicit_current_m01(power_grid)
    q, _ = snapshots_illicit_reactive_power_m01(power_grid)
    return v | i | q, '0'


def violation_count(power_grid):
    """Counts the total amount of violations per snapshot."""
    current_count, _ = current_violation_count(power_grid)
    voltage_count, _ = voltage_violation_count(power_grid)
    reactive_count, _ = reactive_violation_count(power_grid)
    return current_count * 1. + voltage_count * 1. + reactive_count * 1., '0'


def current_cost(power_grid):
    """Current cost for each snapshot, using epsilon as threshold. Only in_service objects are considered."""
    epsilon = 0.1

    line_in_service_ = power_grid.line.in_service.values
    line_normalized_currents = power_grid.res_line.loading_percent.loc[line_in_service_].values / 100.
    line_penalized_currents = np.maximum(0, line_normalized_currents -1 + 2 * epsilon)

    trafo_in_service_ = power_grid.trafo.in_service.values
    trafo_normalized_currents = power_grid.res_trafo.loading_percent.loc[trafo_in_service_].values / 100.
    trafo_penalized_currents = np.maximum(0, trafo_normalized_currents - 1 + 2 * epsilon)

    penalized_currents = np.concatenate([line_penalized_currents, trafo_penalized_currents])
    return np.mean(penalized_currents**2), '0'


def voltage_cost(power_grid):
    """Voltage cost for each snapshot, using epsilon as threshold. Only in_service objects are considered."""
    epsilon = 0.1

    bus_in_service_ = power_grid.bus.in_service.values
    bus_voltage_ = power_grid.res_bus.vm_pu.loc[bus_in_service_].values
    bus_max_voltage = power_grid.bus.max_vm_pu.loc[bus_in_service_].values
    bus_min_voltage = power_grid.bus.min_vm_pu.loc[bus_in_service_].values
    bus_normalized_voltage_ = (bus_voltage_ - bus_min_voltage) / (bus_max_voltage - bus_min_voltage)

    bus_over_voltage_ = np.maximum(0, bus_normalized_voltage_ - 1 + epsilon)
    bus_under_voltage_ = np.maximum(0, epsilon - bus_normalized_voltage_)

    return np.mean(bus_over_voltage_**2 + bus_under_voltage_**2), '0'


def reactive_cost(power_grid):
    """Reactive cost for each snapshot, using epsilon as threshold. Only in_service objects are considered."""
    epsilon = 0.5

    gen_in_service_ = power_grid.gen.in_service.values
    gen_q_mvar = power_grid.res_gen.q_mvar.loc[gen_in_service_].values
    gen_max_q_mvar = power_grid.gen.max_q_mvar.loc[gen_in_service_].values
    gen_min_q_mvar = power_grid.gen.min_q_mvar.loc[gen_in_service_].values
    gen_normalized_q_mvar = (gen_q_mvar - gen_min_q_mvar) / (gen_max_q_mvar - gen_min_q_mvar)

    gen_over_reactive = np.maximum(0, gen_normalized_q_mvar - 1 + epsilon)
    gen_under_reactive = np.maximum(0, epsilon - gen_normalized_q_mvar)

    return np.mean(gen_over_reactive**2 + gen_under_reactive**2), '0'


def joule_cost(power_grid):
    """Normalized joule losses for each snapshot. Divided by the total load."""
    line_in_service_ = power_grid.line.in_service.values
    line_pl_mw = power_grid.res_line.pl_mw.loc[line_in_service_].values

    trafo_in_service_ = power_grid.trafo.in_service.values
    trafo_pl_mw = power_grid.res_trafo.pl_mw.loc[trafo_in_service_].values

    load_in_service_ = power_grid.load.in_service.values
    load_p_mw = power_grid.res_load.p_mw.loc[load_in_service_].values

    return (np.sum(line_pl_mw) + np.sum(trafo_pl_mw)) / np.sum(load_p_mw), '0'


def cost(power_grid):
    """Aggregated cost for each snapshot."""
    beta = 1.
    lambda_I = 1.
    lambda_V = 1.

    c_J, _ = joule_cost(power_grid)
    c_Q, _ = reactive_cost(power_grid)
    c_I, _ = current_cost(power_grid)
    c_V, _ = voltage_cost(power_grid)

    return c_J + beta * c_Q + lambda_I * c_I + lambda_V * c_V, '0'


def line_n1(power_grid):
    """Snapshots with 1 disconnected line."""
    df = power_grid.line.in_service.values
    false_count = len(df) - df.sum()
    return false_count == 1, '0'


def line_n2(power_grid):
    """Snapshots with 2 disconnected lines."""
    df = power_grid.line.in_service.values
    false_count = len(df) - df.sum()
    return false_count == 2, '0'


def branch_in_service_count(power_grid):
    """Counts the amount of branches in service per snapshot."""
    line_in_service_count = np.sum(power_grid.line.in_service.values) * 1.0
    trafo_in_service_count = np.sum(power_grid.trafo.in_service.values) * 1.0
    return line_in_service_count + trafo_in_service_count, '0'


def gen_n1(power_grid):
    """Snapshots with 1 disconnected generator."""
    df = power_grid.gen.in_service.values
    false_count = len(df) - df.sum()
    return false_count == 1, '0'


def gen_n2(power_grid):
    """Snapshots with 2 disconnected generators."""
    df = power_grid.gen.in_service.values
    false_count = len(df) - df.sum()
    return false_count == 2, '0'

def generator_in_service_count(power_grid):
    """Counts the amount of generators that are in service."""
    return np.sum(power_grid.gen.in_service.values) * 1.0, '0'


def line_in_service(power_grid):
    """Lines that are in service."""
    return power_grid.line.in_service.values, power_grid.line.name.values


def trafo_in_service(power_grid):
    """Transformers that are in service."""
    return power_grid.trafo.in_service.values, power_grid.trafo.name.values


def gen_in_service(power_grid):
    """Generators that are in service."""
    return power_grid.gen.in_service.values, power_grid.gen.name.values
