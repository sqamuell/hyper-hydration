import numpy as np
from cmaes import CMA
import uuid
import json
import numpy as np

import subprocess
import sys
import datetime

sys.path.append("../")

from create_log_file import addRun, save
from run_simulation import evaluate_bottle


bounds = np.array(
    [
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
    ]
)

optimizer = CMA(
    mean=np.zeros(30),
    sigma=1.3,
    # population_size=5,
    bounds=bounds,
)

for generation in range(50):
    solutions = []
    for population in range(optimizer.population_size):
        x = optimizer.ask()
        value = evaluate_bottle(x, str(generation) + "_" + str(population))

        solutions.append((x, value))

        addRun(value, x)

    optimizer.tell(solutions)

save("cmaes")
