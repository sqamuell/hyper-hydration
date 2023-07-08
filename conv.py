
import pickle
import uuid
import json


with open("rbfoptstate.txt", "rb") as file:
    data = pickle.load(file)

# Access the unmarshalled data
stateDict = {}

for i, posVal in enumerate(data.all_node_pos):
    id = str(uuid.uuid4())
    stateDict[id] = {
        "objectives": {"obj": data.all_node_val[i]},
        "params": {}
    }
    for i, pos in enumerate(posVal):
        stateDict[id]["params"][i] = pos

print(json.dumps(stateDict, indent=4))


# print(data.all_node_pos[0])
# print(data.all_node_val[0])
# print(vars(data))
