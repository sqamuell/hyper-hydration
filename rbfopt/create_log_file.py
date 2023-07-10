import uuid
import json
import numpy as np
import datetime

stateDict = {}


def addRun(objective, params):
    id = str(uuid.uuid4())

    objectives = {}

    if type(objective) is float or type(objective) is int:
        objectives = {"obj": objective}
    else:
        objectives = {"time": objective[0], "opening": objective[1]}

    stateDict[id] = {
        "objectives": objectives,
        "params": {},
        "time": str(datetime.datetime.now()),
    }
    for i, param in enumerate(params):
        stateDict[id]["params"][i] = param


def save(name, soo=True):
    json_object = json.dumps(stateDict, indent=4)

    # Writing to sample.json
    with open(name + "_1.json", "w") as outfile:
        outfile.write(json_object)
