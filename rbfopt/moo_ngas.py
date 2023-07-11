import numpy as np
from pymoo.core.problem import ElementwiseProblem
import sys
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.util.display.column import Column
from pymoo.util.display.output import Output
from pymoo.termination import get_termination
from pymoo.visualization.scatter import Scatter
from pymoo.core.callback import Callback
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.algorithms.moo.moead import MOEAD

sys.path.append("../")

import numpy as np
import rbfopt
import subprocess

import os

os.environ["OMP_NUM_THREADS"] = "1"

from run_simulation import evaluate_bottle
from create_log_file import addRun, save


class BottleWithOpening(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=31,
            n_obj=2,
            xl=[
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.3,
            ],
            xu=[
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
            ],
        )

        self.itercount = 0

    def _evaluate(self, x, out, *args, **kwargs):
        self.itercount += 1
        value = evaluate_bottle(x, self.itercount)
        # value = self.itercount
        out["F"] = np.column_stack([value, x[-1]])


class MyOutput(Output):
    def __init__(self):
        super().__init__()
        self.x_mean = Column("x_mean", width=13)
        self.x_std = Column("x_std", width=13)
        self.columns += [self.x_mean, self.x_std]

    def update(self, algorithm):
        super().update(algorithm)

        self.x_mean.set(np.mean(algorithm.pop.get("X")))
        self.x_std.set(np.std(algorithm.pop.get("X")))


class MyCallback(Callback):
    def __init__(self) -> None:
        super().__init__()

    def notify(self, algorithm):
        objectives = algorithm.pop.get("F")

        for i, objective in enumerate(objectives):
            addRun(objective=objective, params=algorithm.pop.get("X")[i])


problem = BottleWithOpening()

ref_dirs = get_reference_directions("das-dennis", 2, n_partitions=10)

algorithm = MOEAD(ref_dirs, n_neighbors=15, prob_neighbor_mating=0.7)
termination = get_termination("n_gen", 30)

res = minimize(
    problem=problem,
    algorithm=algorithm,
    output=MyOutput(),
    callback=MyCallback(),
    termination=termination,
    seed=1,
    verbose=True,
)

save("moead", False)

Scatter().add(res.F).show()
