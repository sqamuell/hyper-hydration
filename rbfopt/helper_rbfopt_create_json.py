import pickle
import uuid
import json
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
rel_path = "../logs/rbfoptstate.txt"
abs_file_path = os.path.join(script_dir, rel_path)

print(abs_file_path)

with open(abs_file_path, "rb") as file:
    data = pickle.load(file)

# Access the unmarshalled data
stateDict = {}

# print(vars(data))

for i, posVal in enumerate(data.all_node_pos):
    id = str(uuid.uuid4())
    stateDict[id] = {
        "objectives": {"obj": data.all_node_val[i]},
        "params": {},
        "time": i,
    }
    for i, pos in enumerate(posVal):
        stateDict[id]["params"][i] = pos

print(json.dumps(stateDict, indent=4))
