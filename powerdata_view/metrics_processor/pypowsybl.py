from abc import ABC
import pypowsybl as pp
import numpy as np
from powerdata_view.metrics_processor.interface import MetricsProcessorInterface


class PyPowSyblMetricsProcessor(MetricsProcessorInterface, ABC):
    """Metrics Processor that relies on `PyPowSybl <https://pypowsybl.readthedocs.io>`_."""

    metrics_dict = {}

    def __init__(self):
        super().__init__()
        self.metrics_dict = {

            # Voltage set points
            "Generation Voltage Set Points (p.u.)": generation_voltage_setpoint,

            # Joule losses
            "Line Joule Losses (MW)": line_joule_losses,
            "Two Windings Transformers Joule Losses (MW)": two_windings_trafo_joule_losses,
            "Three Windings Transformers Joule Losses (MW)": three_windings_trafo_joule_losses,
            "Total Joule Losses (MW)": total_joule_losses,
            "Normalized Joule Losses": normalized_joule_losses,

            # Shunt actions
            "Shunt Section Count": shunt_section_count,
            "Shunt Section Count Normalized": shunt_section_count_normalized,

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
            "Two Windings Transformer Loading Percent (%)": two_wt_loading_percent,
            "Three Windings Transformer Loading Percent (%)": three_wt_loading_percent,
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
            "Line in Service": line_in_service,
            "Two Windings Transformer in Service": two_wt_in_service,
            "Three Windings Transformer in Service": three_wt_in_service,
            "Generators in Service": generators_in_service,
            "Line in Service Count": line_in_service_count,
            "Two Windings Transformer in Service Count": two_wt_in_service_count,
            "Three Windings Transformer in Service Count": three_wt_in_service_count,
            "Generators in Service Count": generators_in_service_count,
        }

    def run_powerflow(self, power_grid):
        """AC-PowerFlow implementation of PyPowSybl. Enforces reactive limits.

        Overrides run_powerflow of abstract base class.
        """
        _ = pp.loadflow.run_ac(power_grid)

    def load_power_grid(self, filepath):
        """Loads a power grid in memory.

        Overrides load_power_grid of abstract base class.
        """
        return pp.network.load(filepath)


def generation_voltage_setpoint(power_grid):
    """Voltage set points in per-unit at all generators and ext_grids."""
    per_unit_grid = pp.perunit.per_unit_view(power_grid)
    gen_table = per_unit_grid.get_generators()
    gen_on = gen_table.loc[gen_table.connected.values]
    gen_vm_pu = gen_on.target_v.values
    gen_name = gen_on.index.values
    return gen_vm_pu, gen_name


def line_joule_losses(power_grid):
    """Joule losses in MW at all transmission lines."""
    line_table = power_grid.get_lines()
    line_joule_losses = line_table.p1.values + line_table.p2.values
    line_name = line_table.index.values
    return line_joule_losses, line_name


def two_windings_trafo_joule_losses(power_grid):
    """Joule losses in MW at all 2 windings transformers."""
    trafo_table = power_grid.get_2_windings_transformers()
    trafo_joule_losses = trafo_table.p1.values + trafo_table.p2.values
    trafo_name = trafo_table.index.values
    return trafo_joule_losses, trafo_name


def three_windings_trafo_joule_losses(power_grid):
    """Joule losses in MW at all 3 windings transformers."""
    trafo_table = power_grid.get_3_windings_transformers()
    trafo_joule_losses = trafo_table.p1.values + trafo_table.p2.values
    trafo_name = trafo_table.index.values
    return trafo_joule_losses, trafo_name


def total_joule_losses(power_grid):
    """Total Joule losses in MW summed over the power grid."""
    line_joule, _ = line_joule_losses(power_grid)
    two_wt_joule, _ = two_windings_trafo_joule_losses(power_grid)
    three_wt_joule, _ = three_windings_trafo_joule_losses(power_grid)
    return np.sum(line_joule) + np.sum(two_wt_joule) + np.sum(three_wt_joule), '0'


def normalized_joule_losses(power_grid):
    """Total Joule losses summed over the power grid, divided by the total consumption."""
    total_joule, _ = total_joule_losses(power_grid)
    load_table = power_grid.get_loads()
    total_load = np.sum(load_table.p.values)
    return total_joule / total_load, '0'


def shunt_section_count(power_grid):
    """Shunt steps."""
    shunt_table = power_grid.get_shunt_compensators()
    section_count = shunt_table.section_count.values * 1.0
    shunt_name = shunt_table.index.values
    return section_count, shunt_name


def shunt_section_count_normalized(power_grid):
    """Shunt steps divided by max step."""
    shunt_table = power_grid.get_shunt_compensators()
    section_count = shunt_table.section_count.values
    max_section_count = shunt_table.max_section_count.values
    shunt_name = shunt_table.index.values
    return section_count / max_section_count, shunt_name


def load_active_power(power_grid):
    """Active power load."""
    load_table = power_grid.get_loads()
    return load_table.p.values, load_table.index.values


def load_total_active_power(power_grid):
    """Sum of active load per snapshot."""
    load_table = power_grid.get_loads()
    return np.sum(load_table.p.values), '0'


def load_reactive_power(power_grid):
    """Reactive power load."""
    load_table = power_grid.get_loads()
    return load_table.q.values, load_table.index.values


def load_total_reactive_power(power_grid):
    """Sum of reactive power load per snapshot."""
    load_table = power_grid.get_loads()
    return np.sum(load_table.q.values), '0'


def load_power_factor(power_grid):
    """Load power factor."""
    load_table = power_grid.get_loads()
    p = load_table.p.values
    q = load_table.q.values
    s = np.sqrt(p**2 + q**2)
    pf = p / s
    return pf, load_table.index.values


def bus_voltage(power_grid):
    """Bus voltages in per-unit."""
    per_unit_grid = pp.perunit.per_unit_view(power_grid)
    bus_table = per_unit_grid.get_buses()
    return bus_table.v_mag.values, bus_table.index.values


def bus_normalized_voltage(power_grid):
    """Bus voltages normalized by their min-max range. (0=min, 1=max)"""
    per_unit_grid = pp.perunit.per_unit_view(power_grid)
    voltage_level_table = per_unit_grid.get_voltage_levels()
    bus_table = per_unit_grid.get_buses()
    v = bus_table.v_mag.values
    v_min = voltage_level_table.loc[bus_table.voltage_level_id.values].low_voltage_limit.values
    v_max = voltage_level_table.loc[bus_table.voltage_level_id.values].high_voltage_limit.values
    return (v - v_min) / (v_max - v_min), bus_table.index.values


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
    operational_limits_table = power_grid.get_operational_limits()
    line_table = power_grid.get_lines()
    i_max_table = operational_limits_table.loc[line_table.index.values]
    i1 = line_table.i1.values
    i1_max = i_max_table[i_max_table.side=="ONE"].value.values
    i2 = line_table.i2.values
    i2_max = i_max_table[i_max_table.side=="TWO"].value.values
    return 100 * np.maximum(np.abs(i1/i1_max), np.abs(i2/i2_max)), line_table.index.values


def two_wt_loading_percent(power_grid):
    """Two windings transformer loading percentage, 100 corresponds to a fully loaded line."""
    operational_limits_table = power_grid.get_operational_limits()
    line_table = power_grid.get_2_windings_transformers()
    i_max_table = operational_limits_table.loc[line_table.index.values]
    i1 = line_table.i1.values
    i1_max = i_max_table[i_max_table.side == "ONE"].value.values
    i2 = line_table.i2.values
    i2_max = i_max_table[i_max_table.side == "TWO"].value.values
    return 100 * np.maximum(np.abs(i1 / i1_max), np.abs(i2 / i2_max)), line_table.index.values


def three_wt_loading_percent(power_grid):
    """Three windings transformer loading percentage, 100 corresponds to a fully loaded line."""
    operational_limits_table = power_grid.get_operational_limits()
    line_table = power_grid.get_3_windings_transformers()
    i_max_table = operational_limits_table.loc[line_table.index.values]
    i1 = line_table.i1.values
    i1_max = i_max_table[i_max_table.side == "ONE"].value.values
    i2 = line_table.i2.values
    i2_max = i_max_table[i_max_table.side == "TWO"].value.values
    return 100 * np.maximum(np.abs(i1 / i1_max), np.abs(i2 / i2_max)), line_table.index.values


def branch_normalized_current(power_grid):
    """Branch normalized current."""
    line_percentage, line_name = line_loading_percent(power_grid)
    two_wt_percentage, two_wt_name = two_wt_loading_percent(power_grid)
    three_wt_percentage, three_wt_name = three_wt_loading_percent(power_grid)

    current = np.concatenate([line_percentage, two_wt_percentage, three_wt_percentage]) / 100.
    name = np.concatenate([line_name, two_wt_name, three_wt_name])

    return current, name


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
    return np.sum(illicit_currents), '0'


def generator_active_power(power_grid):
    """Generator active power in MW."""
    gen_table = power_grid.get_generators()
    return gen_table.p.values, gen_table.index.values


def generator_total_active_power(power_grid):
    """Total generator active power in MW."""
    gen_table = power_grid.get_generators()
    return np.sum(gen_table.p.values), '0'


def generator_reactive_power(power_grid):
    """Generator reactive power in MVAr."""
    gen_table = power_grid.get_generators()
    return gen_table.q.values, gen_table.index.values


def generator_total_reactive_power(power_grid):
    """Total generator reactive power in MVAr."""
    gen_table = power_grid.get_generators()
    return np.sum(gen_table.q.values), '0'


def generator_normalized_reactive_power(power_grid):
    """Generator reactive power normalized by their min-max range. (0=min, 1=max)"""
    gen_table = power_grid.get_generators(all_attributes=True)
    q = gen_table.q.values
    q_min = gen_table.min_q_at_p.values
    q_max = gen_table.max_q_at_p.values
    return (-q - q_min) / (q_max - q_min), gen_table.index.values


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
    return np.sum(illicit_reactive), '0'


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
    return current_count + voltage_count + reactive_count, '0'


def current_cost(power_grid):
    """Current cost for each snapshot, using epsilon as threshold. Only in_service objects are considered."""
    epsilon = 0.1

    branch_current, _ = branch_normalized_current(power_grid)
    penalized_currents = np.maximum(0, branch_current - 1 + 2 * epsilon)
    return np.mean(penalized_currents**2), '0'


def voltage_cost(power_grid):
    """Voltage cost for each snapshot, using epsilon as threshold. Only in_service objects are considered."""
    epsilon = 0.1

    voltage, _ = bus_normalized_voltage(power_grid)
    bus_over_voltage_ = np.maximum(0, voltage - 1 + epsilon)
    bus_under_voltage_ = np.maximum(0, epsilon - voltage)

    return np.mean(bus_over_voltage_**2 + bus_under_voltage_**2), '0'


def reactive_cost(power_grid):
    """Reactive cost for each snapshot, using epsilon as threshold. Only in_service objects are considered."""
    epsilon = 0.5

    reactive_power, _ = generator_normalized_reactive_power(power_grid)

    gen_over_reactive = np.maximum(0, reactive_power - 1 + epsilon)
    gen_under_reactive = np.maximum(0, epsilon - reactive_power)

    return np.mean(gen_over_reactive**2 + gen_under_reactive**2), '0'


def joule_cost(power_grid):
    """Normalized joule losses for each snapshot. Divided by the total load."""
    return normalized_joule_losses(power_grid)
    # line_in_service_ = power_grid.line.in_service.values
    # line_pl_mw = power_grid.res_line.pl_mw.loc[line_in_service_].values
    #
    # trafo_in_service_ = power_grid.trafo.in_service.values
    # trafo_pl_mw = power_grid.res_trafo.pl_mw.loc[trafo_in_service_].values
    #
    # load_in_service_ = power_grid.load.in_service.values
    # load_p_mw = power_grid.res_load.p_mw.loc[load_in_service_].values
    #
    # return (np.sum(line_pl_mw) + np.sum(trafo_pl_mw)) / np.sum(load_p_mw), '0'
#

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


def line_in_service(power_grid):
    """Lines that are in service."""
    line_table = power_grid.get_lines()
    return (line_table.connected1 | line_table.connected2).values , line_table.index.values


def two_wt_in_service(power_grid):
    """Two windings transformers that are in service."""
    two_wt_table = power_grid.get_2_windings_transformers()
    return (two_wt_table.connected1 | two_wt_table.connected2).values , two_wt_table.index.values


def three_wt_in_service(power_grid):
    """Three windings transformers that are in service."""
    three_wt_table = power_grid.get_3_windings_transformers()
    return (three_wt_table.connected1 | three_wt_table.connected2).values , three_wt_table.index.values


def generators_in_service(power_grid):
    """Generators that are in service."""
    gen_table = power_grid.get_generators()
    return gen_table.connected.values , gen_table.index.values


def line_in_service_count(power_grid):
    """Counts lines that are in service."""
    line_table = power_grid.get_lines()
    return np.sum((line_table.connected1 | line_table.connected2).values)*1., '0'


def two_wt_in_service_count(power_grid):
    """Counts two windings transformers that are in service."""
    two_wt_table = power_grid.get_2_windings_transformers()
    return np.sum((two_wt_table.connected1 | two_wt_table.connected2).values)*1., '0'


def three_wt_in_service_count(power_grid):
    """Counts three windings transformers that are in service."""
    three_wt_table = power_grid.get_3_windings_transformers()
    return np.sum((three_wt_table.connected1 | three_wt_table.connected2).values)*1. , '0'


def generators_in_service_count(power_grid):
    """Counts generators that are in service."""
    gen_table = power_grid.get_generators()
    return np.sum(gen_table.connected.values)*1., '0'
