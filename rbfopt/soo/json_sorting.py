# import json
# import numpy

# rbf = "C:/Users/danhw/Desktop/1_ITECH/3.CIA/A1/hyper-hydration/rbfopt/soo/rbfopt_1.json" 
# cmaes = "C:/Users/danhw/Desktop/1_ITECH/3.CIA/A1/hyper-hydration/rbfopt/soo/cmaes_1.json"
# random = "C:/Users/danhw/Desktop/1_ITECH/3.CIA/A1/hyper-hydration/rbfopt/soo/random_1.json"


# # Step 1: Read the JSON file and load its contents into a Python object
# with open(random) as file:
#     data = json.load(file)

# sorted_data = sorted(data.items(), key=lambda x: x[1]['objectives']['obj'])

# # Step 3: Write the sorted data back to a JSON file
# # sorted_data_dict = {k: v for k, v in sorted_data}

# # with open(save_path, 'w') as file:
# #     json.dump(sorted_data_dict, file, indent=4)


# a = list(sorted_data)[0][1]["params"]
# print(list(sorted_data)[0][1]["objectives"]["obj"])
# params = []

# # print(a)
# for b in a.values():
#     params.append(b)

#print(params)

# sorted_data_dict = {k: v for k, v in sorted_data[0]}

# print(sorted_data_dict)

#-----------moo
import json
import numpy

moead = "C:/Users/danhw/Desktop/1_ITECH/3.CIA/A1/hyper-hydration/rbfopt/moo/moead_1.json"
nsga2 = "C:/Users/danhw/Desktop/1_ITECH/3.CIA/A1/hyper-hydration/rbfopt/moo/nsga2_1.json"
nsga3 = "C:/Users/danhw/Desktop/1_ITECH/3.CIA/A1/hyper-hydration/rbfopt/moo/nsga3_1.json"

# Step 1: Read the JSON file and load its contents into a Python object
with open(nsga3) as file:
    data = json.load(file)

def sorting_function(item):
    objectives = item['objectives']
    time = objectives['time']
    opening = objectives['opening']
    return time * opening

sorted_data = sorted(data.items(), key=lambda x: sorting_function(x[1]))


a = list(sorted_data)[0][1]["objectives"]

print (a)

# params = []

# for b in a.values():
#     params.append(b)

# print (params)

# sorted_data_dict = {k: v for k, v in sorted_data[0]}

# print(sorted_data_dict)
