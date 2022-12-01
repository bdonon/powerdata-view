from panoramix.problems.interface import AbstractProblem
from panoramix.problems.pandapower import PandaPowerVoltageControl


def get_problem(identifier):
    if identifier == 'PandaPowerVoltageControl':
        return PandaPowerVoltageControl()
    else:
        raise NotImplementedError
