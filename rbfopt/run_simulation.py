import datetime
import json
import subprocess
import sys
import uuid

import numpy as np
from cmaes import CMA

sys.path.append("../")

from create_bottle import create_bottle


def evaluate_bottle(x, iterCount):
    bottle_filename = create_bottle(x, str(iterCount))

    command = ["../FluidX3D/bin/FluidX3D.exe", bottle_filename]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return result.returncode
