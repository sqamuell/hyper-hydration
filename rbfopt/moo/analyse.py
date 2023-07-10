# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 2023

@author: ICD/CA
"""


import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import pygmo as pg
import random
random.seed(5)

CONST_PATH = r'./'

bolMinimize = True

fig_style ='seaborn-whitegrid'

def createObjectivesDF():
    """
    This function reads all log files from the CONST_PATH and 
    generate a data frame of objectives for each algorithm used.
    all data frames are stored in a dictionary where the keys are the algorithm names
    """
    files = []
    allObjectives = {}
    
    for file in os.listdir(CONST_PATH):
    	if file.endswith(".json"):
            files.append(file)
    
    #check for size of logs file and set minfile to the smallest size
    count = []
    for i, file in enumerate(files): 
        with open(CONST_PATH + file, 'r') as f:
            data = json.load(f)
            count.append(len(list(data.keys())))
            #print (list(data.keys())[0])
            objectiveNames = list(data[list(data.keys())[0]]['objectives'].keys())
    
    for objName in sorted(objectiveNames):
        allObjectives[objName] = []
        
    minfile = min(count)
    #read all log files and store them in a dictionary of data frames
    for file in files:
        with open(CONST_PATH + file, 'r') as f:
            data = json.load(f)
            keys = list(data.keys())
            keys.sort (key = lambda x:data[x]['time'],reverse=False)
            for j,key in enumerate(keys):
                for objName in data[key]['objectives'].keys():
                    allObjectives[objName].append((data[key]['objectives'][objName]))       
                algoName = file.split('_')[0]
    #return allObjectives,files  
    allObjectivesDf = pd.DataFrame(allObjectives)
    return allObjectivesDf,files,minfile

def findMinAndMaxPoints(objectivesList):
    # Note: Pygmo Ideal and Nadir can yield different results! (Report bug)
    '''Returns the min and max points for a list of sets of objectives'''        
    
    minPoint = np.array([min(objectivesList[objective]) for objective in objectivesList.keys()])
    maxPoint = np.array([max(objectivesList[objective]) for objective in objectivesList.keys()])
       
    print(f"MinPoint {minPoint[0],minPoint[1]}")
    print(f"MaxPoint {maxPoint[0],maxPoint[1]}")
    
    return minPoint, maxPoint

def normalizePoint(objectives, ideal_point, max_point):
    '''Normalize objectives based on the ideal (smallest) point 
    and the max (largest point).
    Ideal and max are unaffaect by minimization or maximization.
    Ideal and max should be supplied as numpy arrays.'''       
    range_point = np.array(max_point - ideal_point)
    normPoint = (np.array(objectives) - ideal_point) / range_point
    
    for obj in normPoint:
        assert(obj >= 0 and obj <= 1), f"\nObectives {objectives} \nNormalized {normPoint} \nMin {ideal_point} \nMax {max_point} \nRange {range_point}"
    
    return normPoint

def calculateHypervolume(objectivesList, ideal_point, max_point, bolMinimize, bolNormalized):
    '''Calculate the current hypervolume.'''    
    
    # Negate values for maximization
    if bolMinimize == False:
        minObjectivesList = []
        # When objectives are normalized, invert them
        for objs in objectivesList:
            minObjectivesList.append(list(map(lambda y : 1 - y, objs)))
    else:
        minObjectivesList = objectivesList
        
    # Choose reference point
    # When objectives are normalized, the reference is 1, 1, 1, ...
    ref_point = [1] * len(ideal_point)

    hv = pg.hypervolume(minObjectivesList)
    #ref_point = hv.refpoint(offset=0.1)
    return hv.compute(ref_point)

def findParetoIs(objectivesList, bolMinimize):
    '''Returns a list of booleans corresponsing to sets of objectives.
    True is nondominates, False is dominated'''
    
    # Negate values for maximization
    if bolMinimize == False:
        minObjectivesList = []
         
        for objs in objectivesList:
            minObjectivesList.append(list(map(lambda y : y * -1, objs)))
    else:
        minObjectivesList = objectivesList
        
    # Dc is a list with domination counts, 0 == non-dominated
    ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(minObjectivesList)
    
    # Fill list with booleans
    nondominatedIs = []
    
    for count in dc:
        if count == 0:
            nondominatedIs.append(True)
        else:
            nondominatedIs.append(False)
    	
    return nondominatedIs

def processLogFile(file,bolMinimize, ideal_point, max_point):
    
    parametersList = []
    objectivesList = []
    
    normObjectivesList = []
    volume = []
    
    with open(CONST_PATH + file, 'r') as f:
        data = json.load(f)

        keys = list(data.keys())
        keys.sort (key = lambda x:data[x]['time'],reverse=False)

        for i,key in enumerate(keys):
            objectiveNames = sorted(data[key]['objectives'].keys())
            objs = [data[key]['objectives'][objName] for objName in objectiveNames]
            params = [data[key]['params'][paraName] for paraName in sorted(data[key]['params'].keys())]
            ob_arr = [np.array(objs)]
            normObjectivesList.append(normalizePoint(objs, ideal_point, max_point))
            hv = (calculateHypervolume(normObjectivesList, ideal_point, max_point, bolMinimize,True))

            parametersList.append(params)
            objectivesList.append(objs)
            volume.append(hv)
         
        nondominatedIs = findParetoIs(objectivesList, bolMinimize)
     
    return [objectivesList, volume, nondominatedIs, parametersList,objectiveNames]
    
def getParetoDf(parameters, objectivesList, nondominatedIs,objNames, paretoDf = None, solverNames = None):    
    '''Returns a data frame per solver with the achieved Pareto fronts'''
    # First values is parameter string, then come values with objectives
    
    paretoValues = []
    
    for i, bol in enumerate(nondominatedIs):
        if bol == True and solverNames is None:
            paretoValues.append([parameters[i], *objectivesList[i]])
        elif bol == True:
            paretoValues.append([parameters[i], *objectivesList[i], solverNames[i]])
    
    # Sort the values by the first objective to form a continous front
    paretoValues = sorted(paretoValues, key = lambda paretoValue: paretoValue[1])
    
    
    newParetoDf = pd.DataFrame(paretoValues)
    
    # Generate column labels
    objN = len(objectivesList[0])
    
    if paretoDf is None:
        runI = 1
    else:
        columnN = len(paretoDf.columns)        
        runI = int(columnN / (objN + 1) + 1)
    
    columns = [f'Params{runI}']
    
    # Run index and Obj index
    for i in range(objN):
        columns.append(f'{objNames[i]}_RunNumber{runI}')
        
    # Solver names for best Pareto front
    if solverNames is not None:
        columns.append('Solver')
     
    newParetoDf.columns = columns 
    
    # Start new data frame for new solver
    if paretoDf is None:
        paretoDf = newParetoDf
    # Add to exisiting data frame
    else:
        paretoDf = pd.concat([paretoDf, newParetoDf], axis=1)
    
    #print(paretoDf[:5])
    return paretoDf       
   
def processHypervolumeConvergence(hypervolumeDict,bolMinimize):
    '''Calculates the median hypervolume per function evaluation and solver.
    Returns data frame with the median hypervolume for each iteration and per solver'''
    print("\nProcessing convergence ...")
     
    # Median hypervolumes per iterations and solver
    keys = hypervolumeDict.keys()
    solvers = keys
    allMedians= [hypervolumeDict[hvDf].median(axis = 1).tolist() for hvDf in keys]
    
    finalMedians = [median[-1] for median in allMedians]
    
    # Sort by performance    
    if bolMinimize is True:
        allMedians = [sorted(median,reverse=False) for median in allMedians]
    else:
        allMedians = [sorted(median,reverse=True) for median in allMedians]
    
    # Create dataframe with labelled columns 
    mediansDf = pd.DataFrame(allMedians).transpose()

    mediansDf.columns = solvers
    
    # Print last 5 rows
    print(mediansDf.tail(5))
    
    return mediansDf

def processHypervolumeRobustness(hypervolumeDict,bolMinimize):
    '''Returns data frame with final hypervolumes for each run and per solver.'''
    print("\nProcessing variance ...")
    results = []
    variances = []       
    
    keys = hypervolumeDict.keys()
    for i,key in enumerate(keys):
        if bolMinimize:
            lastRow = hypervolumeDict[key].iloc[0]
            result = lastRow.tolist()
            result.sort(reverse=False)
        else:
            lastRow = hypervolumeDict[key].iloc[-1]
            result = lastRow.tolist()
            result.sort(reverse=True)
        variances.append(lastRow.var()) # Variance for console
        
        results.append(result)
        
    medians = [sum(results[i])/len(results[i]) for i in range(len(results))]
    
    # Print variance 
    varsDf = pd.DataFrame(results).transpose()
    varsDf.columns = keys
    print('\nVariance')
    print(varsDf.transpose())

    return varsDf, medians
    
def plotData(plotType,data,save=False,fig_size=(8, 6),figDPI = 300,title=None,xLabel=None,yLabel=None,colors=None,ax = None):
    
    if title==None:
        title="myPlot"
    
    if plotType=="lineplot":
        plt.figure()
        data.plot.line(
            figsize=fig_size,
            title = title,
            xlabel=xLabel,
            ylabel=yLabel,
            color = colors)
    
    elif plotType=="boxplot":
        plt.figure()
        ax = data.plot(kind='box', figsize=fig_size,color = colors)
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        ax.set_title(title)

    if save:
        plt.savefig(CONST_PATH + title+'.png', dpi = figDPI)

def getMedianRunIs(resultsDf):
    '''Returns the index of the median run per solver.'''
    solvers = resultsDf.columns    
    mediansDf = resultsDf.median(axis = 0)
    assert mediansDf.size == len(solvers), f'Number of medians ({mediansDf.size}) doesnt match number of solvers({len(solvers)})'
    
    print('\nMedians')
    print(mediansDf.to_string())
    
    # Subtract median and find smallest difference
    indices = [abs(resultsDf[solver] - mediansDf[solver]).idxmin() for solver in solvers]
    
    print(f'\nMedian runs {indices}')
    return indices

def plotParetoFront(paretoDfs,bestDf,frontIs,solversColor,bolMinimize,save=False):
    plt.figure()
    matplotlib.style.use(fig_style)
    ax = None
    i = 0
    for key,paretoDf in paretoDfs.items():
        # Find number of runs
        frontN = 0
        
        for columnLabel in paretoDf.columns:
            if len(columnLabel) > 6 and columnLabel[:6] == 'Params':
                frontN += 1
         
        # Find number of objectives
        objN = int(len(paretoDf.columns) / frontN) - 1
        indexes = [i for i in range(1 + ((objN + 1) * frontIs[i]),(1 + ((objN + 1) * frontIs[i]))+objN,1)]
        pDf = paretoDf.iloc[:, indexes]

        ax = pDf.plot.line(
            x = 0,
            y = 1,
            ax = ax,
            color = solversColor[i],
            label = key)
        
        pDf.plot.scatter(
            x = 0,
            y = 1,
            ax = ax,
            color = 'white',
            edgecolors = solversColor[i])
        
        i+=1
    
    bestDf.plot.line(
        figsize=(12.56, 4),
        x = 1,
        y = 2,
        ax = ax,
        color = 'black',
        label = 'Best-known',
        dashes = (4,3))
    # Plots points
    bestDf.plot.scatter(
        x = 1,
        y = 2,
        ax = ax,
        title = "Pareto Front",
        color = 'white',
        xlabel = 'Obj--'+list(bestDf.keys())[1].split('_')[0], 
        ylabel = 'Obj--'+list(bestDf.keys())[2].split('_')[0],
        edgecolors = 'black')
    
    if bolMinimize is False:
        ax.invert_xaxis()
        ax.invert_yaxis()
    
    if save:
        plt.savefig(CONST_PATH + 'Pareto.png', dpi = 300)

    plt.show()

if __name__ == "__main__":
    
    hypervolumeDict = {}
    
    allObjectivesDf,filesNames,minRunCount = createObjectivesDF()

    ideal_point, max_point = findMinAndMaxPoints(allObjectivesDf)
    
    sNames = [filesNames[i].split('_')[0] for i in range(len(filesNames))]
    objNames = [filesNames[i].split('_')[0] for i in range(len(filesNames))]
    parameters = []
    multiObjs = []
    solvers = []    
    paretoDfs = {}

    
    for file in filesNames:
        
        solverName = file.split('_')[0]
         
        objectivesList, volume, nondominatedIs, parametersList,objNames = processLogFile(file,bolMinimize,ideal_point, max_point)
        if solverName not in list(hypervolumeDict.keys()):
            paretoDf = getParetoDf(parametersList,objectivesList,nondominatedIs,objNames)
            hypervolumeDict[solverName] = pd.DataFrame()
            hypervolumeDict[solverName][file.split('.')[0]] = volume
        else:
           paretoDf = getParetoDf(parametersList,objectivesList,nondominatedIs,objNames,paretoDf = paretoDf)
           hypervolumeDict[solverName][file.split('.')[0]] = volume
        
        sNames.remove(solverName)
        if solverName not in sNames:
            solvers.append(solverName) 
            paretoDfs[solverName]=paretoDf
            
        parameters.extend(parametersList)
        multiObjs.extend(objectivesList)
           
        
    solversColor = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(solvers))]
    mediansDf = processHypervolumeConvergence(hypervolumeDict,bolMinimize)
    plotData("lineplot",mediansDf,True,title="Convergence",xLabel="Function Evaluations",yLabel="Objective",colors = solversColor)
    
    varsDf, bestMedians = processHypervolumeRobustness(hypervolumeDict,bolMinimize)
    plotData("boxplot",varsDf,True,title="Robustness",xLabel="Final Results",yLabel="Objective")
        
    frontIs = getMedianRunIs(varsDf)
    totalEvals = len(filesNames) * minRunCount
    print(f"\nEvaluations: {totalEvals}, Parameters: {len(parameters[0])}, Objectives: {len(multiObjs[0])}, Solver Names: {set(solvers)}")
    print("Calculating best-known front ...")
    
    bolsNondom = findParetoIs(multiObjs, bolMinimize)
    bestDf = getParetoDf(parameters, multiObjs, bolsNondom,objNames, None, None)
    
    plotParetoFront(paretoDfs,bestDf,frontIs,solversColor,bolMinimize,save = True)

