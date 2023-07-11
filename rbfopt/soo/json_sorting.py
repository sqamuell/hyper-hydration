import json
import numpy

file_path = "C:/Users/danhw/Desktop/1_ITECH/3.CIA/A1/hyper-hydration/rbfopt/soo/random_1.json"


# Step 1: Read the JSON file and load its contents into a Python object
with open(file_path) as file:
    data = json.load(file)

sorted_data = sorted(data.items(), key=lambda x: x[1]['objectives']['obj'])

# Step 3: Write the sorted data back to a JSON file
# sorted_data_dict = {k: v for k, v in sorted_data}

# with open(save_path, 'w') as file:
#     json.dump(sorted_data_dict, file, indent=4)


a = list(sorted_data)[0][1]["params"]
params = []

# print(a)
for b in a.values():
    params.append(b)

print(params)

# sorted_data_dict = {k: v for k, v in sorted_data[0]}

# print(sorted_data_dict)
