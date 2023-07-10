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

params = np.random.rand(500, 30)

for i, param in enumerate(params):
    value = evaluate_bottle(param, i)

    addRun(value, param)


save("random")
