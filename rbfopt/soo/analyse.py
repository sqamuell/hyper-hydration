# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 19:54:44 2022

@author: ICD/CA
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import json

CONST_PATH = r"./"


def createObjectivesDF():
    """
    This function reads all log files from the CONST_PATH and
    generates a data frame of objectives for each algorithm used.
    all data frames are stored in a dictionary where the keys are the algorithm names
    """
    files = []
    objeectiveDataFrames = {}

    for file in os.listdir(CONST_PATH):
        if file.endswith(".json"):
            files.append(file)

    # check for size of logs file and set minfile to the smallest size
    count = []
    for i, file in enumerate(files):
        with open(CONST_PATH + file, "r") as f:
            data = json.load(f)
            count.append(len(list(data.keys())))
    minfile = min(count)

    # read all log files and store them in a dictionary of data frames
    for file in files:
        with open(CONST_PATH + file, "r") as f:
            data = json.load(f)
            objectivesList = []
            keys = list(data.keys())
            keys.sort(key=lambda x: data[x]["time"], reverse=False)
            for j, key in enumerate(keys):
                if j < minfile:
                    for objName in data[key]["objectives"].keys():
                        objectivesList.append(data[key]["objectives"][objName])
                algoName = file.split("_")[0]
            objectivesList.sort(reverse=False)
            if algoName not in objeectiveDataFrames.keys():
                objeectiveDataFrames[algoName] = pd.DataFrame()
                objeectiveDataFrames[algoName][file.split(".")[0]] = objectivesList
            else:
                objeectiveDataFrames[algoName][file.split(".")[0]] = objectivesList
    return objeectiveDataFrames


def processConvergence(objectiveDf, bolMinimize):
    """Calculates the median objective per function evaluation and solver.
    Returns data frame with the median objective for each iteration and per solver"""
    print("\nProcessing convergence ...")

    # Median objective per iterations and solver
    keys = objectiveDf.keys()

    print(objectiveDf)

    solvers = keys
    allMedians = [objectiveDf[hvDf].median(axis=1).tolist() for hvDf in keys]

    # Sort by performance
    if bolMinimize is True:
        allMedians = [sorted(median, reverse=True) for median in allMedians]
    else:
        allMedians = [sorted(median, reverse=False) for median in allMedians]

    # Create dataframe with labelled columns
    mediansDf = pd.DataFrame(allMedians).transpose()

    mediansDf.columns = solvers

    # Print last 5 rows
    print(mediansDf.tail(5))

    return mediansDf


def processRobustness(objectiveDf, bolMinimize):
    """Returns data frame with variance and median per solver."""
    print("\nProcessing variance ...")
    results = []
    variances = []

    keys = objectiveDf.keys()
    for i, key in enumerate(keys):
        if bolMinimize:
            lastRow = objectiveDf[key].iloc[0]
            result = lastRow.tolist()
            result.sort(reverse=False)
        else:
            lastRow = objectiveDf[key].iloc[-1]
            result = lastRow.tolist()
            result.sort(reverse=True)
        variances.append(lastRow.var())  # Variance for console

        results.append(result)

    medians = [sum(results[i]) / len(results[i]) for i in range(len(results))]

    # Print variance
    varsDf = pd.DataFrame(results).transpose()
    varsDf.columns = keys
    print("\nVariance")
    print(varsDf.transpose())

    return varsDf, medians


def plotData(
    plotType,
    data,
    save=False,
    fig_size=(8, 6),
    figDPI=300,
    title=None,
    xLabel=None,
    yLabel=None,
):
    if title == None:
        title = "myPlot"

    if plotType == "lineplot":
        plt.figure()
        data.plot.line(figsize=fig_size, title=title, xlabel=xLabel, ylabel=yLabel)

    elif plotType == "boxplot":
        plt.figure()
        ax = data.plot(kind="box", figsize=fig_size)
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        ax.set_title(title)

    if save:
        plt.savefig(CONST_PATH + title + ".png", dpi=figDPI)

    plt.show()


if __name__ == "__main__":
    objectivesDfs = createObjectivesDF()

    mediansDf = processConvergence(objectivesDfs, True)
    plotData(
        "lineplot",
        mediansDf,
        False,
        title="Convergence",
        xLabel="Function Evaluations",
        yLabel="Objective",
    )

    varsDf, bestMedians = processRobustness(objectivesDfs, True)
    plotData(
        "boxplot",
        varsDf,
        False,
        title="Robustness",
        xLabel="Final Results",
        yLabel="Objective",
    )
