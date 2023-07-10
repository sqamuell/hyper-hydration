from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import sys

sys.path.append("../")

import numpy as np
import rbfopt
import subprocess

import os

os.environ["OMP_NUM_THREADS"] = "1"

from create_bottle import create_bottle

bottle_filename = create_bottle(
    [
        0.6022995468440653,
        0.09276005589014916,
        0.20973719869240806,
        0.7552273432334666,
        0.49146383824623113,
        0.1392360441789956,
        0.9056805977725262,
        0.30217957160389275,
        0.6203749463605711,
        0.43272010490276475,
        0.38523830567787065,
        0.29103923918675195,
        0.7369437716042325,
        0.3867876679675839,
        0.19586324156070137,
        0.23395631752862273,
        0.11773353668236376,
        0.16958407252529,
        0.28996302492913,
        0.28455020755836036,
        0.0957164293335879,
        0.046133107695340604,
        0.8172089936219297,
        0.3852154980534722,
        0.5501060584125244,
        0.1905756342820127,
        0.3712973147381059,
        0.5207979911909925,
        0.12273297293783143,
        0.05442722595636815,
    ],
    "best",
)

command = ["../FluidX3D/bin/FluidX3D.exe", bottle_filename]

result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print(result.returncode)
