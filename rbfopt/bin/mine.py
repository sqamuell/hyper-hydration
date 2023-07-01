
# settings = rbfopt.RbfoptSettings(minlp_solver_path="C:\Users\danhw\Desktop\1_ITECH\3. CIA\A1\rbfopt\bin\bonmin.exe",
# nlp_solver_path="C:\Users\danhw\Desktop\1_ITECH\3. CIA\A1\rbfopt\bin\ipopt.exe")

python rbfopt_cl_interface.py --minlp_solver_path='C:/Users/danhw/Desktop/1_ITECH/3.CIA/A1/rbfopt/bin/bonmin.exe' branin


import rbfopt
import numpy as np
def obj_funct(x):
    return x[0]*x[1] - x[2]

bb = rbfopt.RbfoptUserBlackBox(3, np.array([0] * 3), np.array([10] * 3), np.array(['R', 'I', 'R']), obj_funct)
function = 
settings = rbfopt.RbfoptSettings(max_evaluations=50)
alg = rbfopt.RbfoptAlgorithm(settings, bb)

objval, x, itercount, evalcount, fast_evalcount = alg.optimize()