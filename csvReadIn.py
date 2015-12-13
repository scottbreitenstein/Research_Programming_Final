# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import colors
from tkinter import filedialog


def load_csv():
    """Prompts the user to find a csv to load in"""
    file_path = filedialog.askopenfilename()
    data = np.loadtxt(open(file_path, "rb"), delimiter=",")
    return data


def list_uncertainties(data):
    """Returns a list of uncertainties mined from a coordAmp dataset"""
    maxUncertainty = .3
    uncertainties = []
    for row in data:
        for uncertainty in row[4::8]:
            if uncertainty < maxUncertainty:
                uncertainties.append(uncertainty)
    return uncertainties


def make_coordAmp_dataframe(npArray):
    """Creates a labelled dataframe for the coordAmp dataset"""
    columnNames = []
    i = 0
    for cells in npArray[0, ::8]:
        i = i+1
        columnNameCycle = ['xPos {}'.format(i), 'yPos {}'.format(i),
                           'zPos {}'.format(i), 'amplitude {}'.format(i),
                           'xUncertainty {}'.format(i),
                           'yUncertainty {}'.format(i),
                           'zUncertainty {}'.format(i),
                           'ampUncertainty {}'.format(i)]
        columnNames = columnNames+columnNameCycle
    infoFrame = pd.DataFrame(npArray, index=range(0, npArray.shape[0]),
                             columns=columnNames)
    return infoFrame


def make_seq_dataframe(npArray):
    """Creates a labelled dataframe for the SeqOfEvents dataset"""
    columnNames = ['Frame Index', 'Start/End', 'Track Index', 'Merge/Split']
    infoFrame = pd.DataFrame(npArray, index=range(0, npArray.shape[0]),
                             columns=columnNames)
    return infoFrame


def make_featIndx_dataframe(npArray):
    """Creates a labelled dataframe for the featIndx dataset"""
    columnNames = []
    i = 0
    for columns in npArray[0]:
        i = i+1
        currentName = 'Frame {}'.format(i)
        columnNames.append(currentName)
    infoFrame = pd.DataFrame(npArray, index=range(0, npArray.shape[0]),
                             columns=columnNames)
    return infoFrame


# def uncertainty_mask(coordAmp, uncertaintyThreshold=.3):
#    xUncertainties = coordAmp.loc[:, 'xUncertainty 1'::8]
#    yUncertainties = coordAmp.loc[:, 'yUncertainty 1'::8]
#    xMask = xUncertainties[xUncertainties < uncertaintyThreshold] = True
#    yMask = yUncertainties[yUncertainties < uncertaintyThreshold] = True

def plot_points(coordAmp):
    """Plots all the individual points in a coordAmp file"""
    xValues = coordAmp.loc[:, 'xPos 1'::8]
    yValues = coordAmp.loc[:, 'yPos 1'::8]
    plt.scatter(xValues, yValues)
    plt.show()


def plot_track(coordAmp, track):
    """Plots a single track from a coordAmp file"""
    xPositions = coordAmp.loc[track].loc['xPos 1'::8]
    yPositions = coordAmp.loc[track].loc['yPos 1'::8]
    coordinates = zip(xPositions, yPositions)
    plt.scatter(xPositions, yPositions)
    plt.plot(xPositions, yPositions)
#    plt.xlim(0,300)
#    plt.ylim(0,300)
#    plt.show()


def plot_all_tracks(coordAmp):
    """Plots all the tracks from a coordAmp file"""
    for track in range(1, coordAmp.shape[0]):
        xPositions = coordAmp.loc[track].loc['xPos 1'::8]
        yPositions = coordAmp.loc[track].loc['yPos 1'::8]
#        plt.scatter(xPositions,yPositions)
        plt.plot(xPositions, yPositions)
#    plt.xlim(50,80)
#    plt.ylim(50,80)
    plt.show()

def find_average_positions(coordAmp):
    """Finds the average positions of each track in a coordAmp file and returns
    them as a list of tuples"""
    averagePositions = []
    for track in range(1, coordAmp.shape[0]):
        xPositions = coordAmp.loc[track].loc['xPos 1'::8]
        yPositions = coordAmp.loc[track].loc['yPos 1'::8]
        averagePositions.append((xPositions.mean(),yPositions.mean()))
    return averagePositions
    
def find_track_starts(coordAmp):
    """Finds the beginning positions of each track and returns them as a list 
    of tuples"""
    trackStarts = []    
    for track in range(1, coordAmp.shape[0]):
        xPositions = coordAmp.loc[track].loc['xPos 1'::8]
        yPositions = coordAmp.loc[track].loc['yPos 1'::8]
        frame = 0
        xPosition = np.nan
        while (np.isnan(xPosition)):
            xPosition = xPositions[frame]
            frame = frame + 1
        trackStarts.append((xPositions[frame], yPositions[frame]))
    return trackStarts
        
def plot_mean_vectors(coordAmp):
    """Plots the vectors of average motion"""
    tails = find_track_starts(coordAmp)
    heads = find_average_positions(coordAmp)
    tailArray = np.array(tails)    
    headArray = np.array(heads)
    vectors = list(headArray - tailArray)
    x,y = zip(*tails)
    u,v = zip(*vectors)
    plt.figure()
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    ax.quiver(x,y,u,v,angles='xy', scale_units='xy', scale=1)
    ax.set_xlim([60,80])
    ax.set_ylim([180,200])
    plt.draw()
    plt.show()
  
def plot_density_heatmap(coordAmp):
    """Plots a heatmap of particle density using the average position of the
    particles"""
    average_pos = find_average_positions(coordAmp)
    xpos,ypos = zip(*average_pos)
    heatmap,xedges,yedges = np.histogram2d(ypos, xpos, bins=25)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    plt.imshow(heatmap, extent=extent, origin = 'lower')