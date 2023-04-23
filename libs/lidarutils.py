#!/usr/bin/env python3
__author__ = "Ashesh Vasalya"

import os
import csv
import numpy

import matplotlib.pyplot as plt

from .mapping import lidar_to_grid_map
from . import loghandler

logHandle = loghandler.LogHandler()


def ReadFile(fileName):
    """
    Opens and reads a CSV file.

    Args:
        fileName (str): The name of the CSV file to be read.

    Returns:
        csv.reader: A CSV reader object that can be used to iterate over the rows in the file.

    Raises:
        AssertionError: If the input filename is None, empty, or invalid.
    """

    # Check if fileName is None or empty
    assert fileName, "No filename provided."

    # Check if file exists and is not a directory
    assert os.path.exists(fileName), f"File '{fileName}' not found."
    assert os.path.isfile(fileName), f"'{fileName}' is not a file."

    fileHandler = open(fileName, "r")
    data = csv.reader(fileHandler)
    return data


def GetLidarMeasurementsFromFile(lidarPoints):
    """
    Reads a lidar measurements file and returns arrays of angles and distances.

    Args:
        lidarPoints (str): The name of the file containing the lidar measurements.

    Returns:
        tuple: A tuple of two numpy arrays:
            - angles: an array of the angles at which measurements were taken
            - distances: an array of the distances returned by the lidar for each angle

    Raises:
        AssertionError: If the input filename is None, empty, or invalid.
    """

    # Check if lidarPoints is None or empty
    assert lidarPoints, "No lidarPoints filename provided."

    # Check if file exists and is not a directory
    assert os.path.exists(lidarPoints), f"Lidar points file '{lidarPoints}' not found."
    assert os.path.isfile(lidarPoints), f"'{lidarPoints}' is not a file."

    # Read the lidar measurements from the file
    measurements = ReadFile(lidarPoints)

    # Parse the measurements into angles and distances
    angles = []
    distances = []
    for measurement in measurements:
        angles.append(float(measurement[0]))
        distances.append(float(measurement[1]))

    # Convert the angles and distances to numpy arrays
    angles = numpy.array(angles)
    distances = numpy.array(distances)

    logHandle.log.debug(
        f"In total, the drone collected {len(angles)} samples from all sweeps."
    )

    # Return the arrays of angles and distances
    return angles, distances


def GetFlightPathFromFile(flightPath):
    """
    Reads a flight path file and returns arrays of sweep IDs and path coordinates.

    Args:
        flightPath (str): The name of the file containing the flight path.

    Returns:
        tuple: A tuple of two numpy arrays:
            - sweepIDs: an array of the sweep IDs
            - pathCoordinates: an array of the path coordinates

    Raises:
        AssertionError: If the input filename is None, empty, or invalid.
    """
    # Check if flightPath is None or empty
    assert flightPath, "No flight path filename provided."

    # Check if file exists and is not a directory
    assert os.path.exists(flightPath), f"Flight path file '{flightPath}' not found."
    assert os.path.isfile(flightPath), f"'{flightPath}' is not a file."

    logHandle.log.debug(f"Reading flight coordinates from {flightPath}")
    pathPoints = ReadFile(flightPath)

    # Parse the flight path into sweep IDs and path coordinates
    pointsList = []
    for points in pathPoints:
        pointsList.append(points)

    sweepIDs = numpy.array(pointsList[::2], dtype="uint8")[:, 0]
    pathCoordinates = numpy.array(pointsList[1::2], dtype="float32")

    # Print the sweep ID and location for each point in the flight path
    for sweepID, point in zip(sweepIDs, pathCoordinates):
        logHandle.log.info(f"At sweep {sweepID}: drone was at coordinates {point}")

    # Return the arrays of sweep IDs and path coordinates
    return sweepIDs, pathCoordinates


def GetUnitConversionScale(inputUnit, outputUnit):
    """
    Converts between different units of distance.

    Args:
        inputUnit (str): The unit of distance to convert from.
        outputUnit (str): The unit of distance to convert to.

    Returns:
        float: The scale factor to convert from inputUnit to outputUnit.

    Raises:
        AssertionError: If inputUnit or outputUnit is not a valid unit of distance.
    """

    unitsDict = {"m": 1, "cm": 100, "mm": 1000}

    # Ensure inputUnit is a valid unit of distance
    assert inputUnit in unitsDict.keys(), "Invalid inputUnit: {}".format(inputUnit)

    # Ensure outputUnit is a valid unit of distance
    assert outputUnit in unitsDict.keys(), "Invalid outputUnit: {}".format(outputUnit)

    # Return the scale factor to convert from inputUnit to outputUnit
    return unitsDict[outputUnit] / unitsDict[inputUnit]


def ExtractSweepsFromMeasurements(angles, distances):
    """
    Extracts lidar sweeps from measurements.

    Args:
        angles (numpy.ndarray): 1D array of angles in degrees.
        distances (numpy.ndarray): 1D array of distances.

    Returns:
        lidarSweepsList (list): List[Dict[str, numpy.ndarray]]
        A list of dictionaries containing the LIDAR sweeps' information.
        Each dictionary should contain keys "sweepID", "coordinates", "angles", and "distances".

    Raises:
        AssertionError: If the input arrays are empty or not 1D.
        AssertionError: If the length of the input arrays do not match.
        AssertionError: If the angles array contains values outside the range [0, 360).

    """

    # Check input arrays are valid
    assert len(angles.shape) == 1, "angles array should be 1D"
    assert len(distances.shape) == 1, "distances array should be 1D"
    assert (
        angles.shape == distances.shape
    ), "angles and distances arrays should have the same length"
    assert len(angles) > 0, "angles array should not be empty"
    assert len(distances) > 0, "distances array should not be empty"
    assert (distances >= 0).all(), "distances should be positive"
    assert (angles >= 0).all() and (
        angles <= 360
    ).all(), "angles should be in the range [0, 360]"

    # statistically extract total samples per sweep
    allZeroCrossingPoints = numpy.where(numpy.round(angles) == 0)[0]
    possibleSamplesLength = numpy.diff(allZeroCrossingPoints)
    sampleBins, sampleValues = numpy.histogram(possibleSamplesLength)
    numSamples = sampleValues[numpy.argmax(sampleBins)]

    # we rely on the fact that our lidar sensor is not perfect,
    # and can have few samples more or less per sweep
    possibleNumSamples = [
        possibleNumSamples for possibleNumSamples in [-2, -1, 0, 1, 2]
    ] + numSamples

    numSweeps = 0
    sweepSamplesLengthList = []
    for distance in distances:
        if distance in possibleNumSamples:
            logHandle.log.info(
                "At sweep={}, numSamples={}".format(numSweeps, int(distance))
            )
            numSweeps += 1
            sweepSamplesLengthList.append(int(distance))
    sweepSamplesLengthList = numpy.array(sweepSamplesLengthList)

    logHandle.log.debug("extract each sweep measurement data and create list per sweep")
    lidarSweepsList = []
    for sweepID in range(numSweeps):
        minIndex = (
            sweepSamplesLengthList[:sweepID].sum() + sweepID + 1 if sweepID > 0 else 0
        )
        maxIndex = sweepSamplesLengthList[: (sweepID + 1)].sum() + sweepID + 1
        logHandle.log.info(
            "For Sweep={} data ranges from minIndex:maxIndex {}:{}".format(
                sweepID, minIndex, maxIndex
            )
        )

        sweepDataDict = {}
        sweepDataDict["angles"] = angles[minIndex:maxIndex]
        unitConversionFactor = GetUnitConversionScale("mm", "m")
        sweepDataDict["distances"] = distances[minIndex:maxIndex] * unitConversionFactor
        lidarSweepsList.append(sweepDataDict)

    return lidarSweepsList


def VisualizeMeasurementsPerSweep(
    lidarSweepsList,
    sampling=2,
    xy_resolution=0.01,
    show=False,
    dumpViz=False,
):
    """
    Visualizes lidar measurements per sweep.

    Args:
        lidarSweepsList (list): List of dictionaries.
        Containing the angles and distances of each lidar sweep.
        sampling (int): Sampling interval for displaying lidar measurements.
        xy_resolution (float): Resolution of the grid map.
        show (bool): Whether or not to display the generated plots.
        dumpViz (bool): If True, save the visualization to a file.

    Raises:
        AssertionError: If lidarSweepsList is empty or not a list.
        AssertionError: If sampling is not a positive integer.
        AssertionError: If xy_resolution is not a positive float.

    """
    assert (
        isinstance(lidarSweepsList, list) and len(lidarSweepsList) > 0
    ), "lidarSweepsList should be a non-empty list"
    assert (
        isinstance(sampling, int) and sampling > 0
    ), "sampling should be a positive integer"
    assert (
        isinstance(xy_resolution, float) and xy_resolution > 0
    ), "xy_resolution should be a positive float"

    numSweeps = len(lidarSweepsList)

    for sweepID in range(numSweeps):
        logHandle.log.debug(
            "Computing lidar measurements and occupancy map from sweepID={}".format(
                sweepID
            )
        )
        # convert the Lidar measurements to x, y coordinates
        angles = lidarSweepsList[sweepID]["angles"] * (numpy.pi / 180)
        distances = lidarSweepsList[sweepID]["distances"]
        ox = (distances) * numpy.sin(angles)
        oy = (distances) * numpy.cos(angles)

        gridMap = lidar_to_grid_map.generate_ray_casting_grid_map(
            ox, oy, xy_resolution, sweepID, True
        )[0]

        if show:
            logHandle.log.info(
                "Preparing visualizing grid map and Lidar Measurement map of sweepID={}".format(
                    sweepID
                )
            )
            fig = plt.figure(sweepID, figsize=(10, 5))
            plt.subplot(121)
            plt.title("gridMap=%i" % sweepID)
            plt.imshow(gridMap, cmap="RdYlGn_r")
            plt.colorbar()
            plt.draw()
            fig.canvas.draw_idle()
            plt.subplot(122)
            plt.title("lidarMeasurementMap=%i" % sweepID)
            plt.plot(
                [oy[::sampling], numpy.zeros(numpy.size(oy[::sampling]))],
                [ox[::sampling], numpy.zeros(numpy.size(ox[::sampling]))],
                "ro-",
            )
            plt.plot(0, 0, "ob")
            bottom, top = plt.ylim()
            plt.ylim((top, bottom))
            plt.draw()
            fig.canvas.draw_idle()

            plt.pause(0.001)
            if dumpViz:
                plt.savefig(os.path.join("output", "sweepID_{}.png".format(sweepID)))
    if show:
        input("Press [enter] to continue or exit.")


def VisualizeAllSweepsWithDronePath(
    lidarSweepsList,
    sampling=2,
    show=False,
    dumpViz=False,
):
    """
    Visualizes all the LIDAR sweeps in the given list along with the drone's flight path.

    Args:
        lidarSweepsList (list): List of LiDAR sweep dictionaries.
        sampling (int): Downsample factor for lidar sweep visualization.
        show (bool): If True, show the visualization window.
        dumpViz (bool): If True, dump visualization frames to disk.
    """
    if show:
        logHandle.log.debug("Visualizing all flight path and all sweeps measurements")
        fig, ax = plt.subplots(figsize=(15, 8))
        randomState = numpy.random.RandomState(3)
        for sweepID in range(len(lidarSweepsList)):
            position = lidarSweepsList[sweepID]["coordinates"]
            angles = lidarSweepsList[sweepID]["angles"] * (numpy.pi / 180)
            distances = lidarSweepsList[sweepID]["distances"]
            # Plot the LIDAR data
            x = position[0] + distances[::sampling] * numpy.cos(angles[::sampling])
            y = position[1] + distances[::sampling] * numpy.sin(angles[::sampling])
            ax.plot(x, y, "ro", linewidth=2, markersize=1)

            # Plot the drone position
            color = tuple(
                (randomState.random(), randomState.random(), randomState.random())
            )
            ax.plot(position[0], position[1], color=color, marker="o")
            ax.annotate(
                f"P:{sweepID}",
                xy=position,
                xytext=(-20, 20),
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

            # Connect wayPoints
            if sweepID > 0:
                startPos = lidarSweepsList[sweepID - 1]["coordinates"]
                endPos = position
                ax.plot(
                    [startPos[0], endPos[0]],
                    [startPos[1], endPos[1]],
                    color=color,
                )

        # Add labels and legend
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_xlim((0, 25))
        ax.set_ylim((-15, 30))
        ax.set_title("Drone Path and LIDAR Data")
        ax.legend(["LIDAR data"])
        fig.canvas.draw_idle()
        plt.pause(0.001)
        if dumpViz:
            plt.savefig(os.path.join("output", "dronePathAndScans.png"))

        input("Press [enter] to exit.")


def VisualizeRandomFlightPathAndSweep(positions, angles, distances, sampling=6):
    """
    Plot the drone flight path and simulated LIDAR measurements on a 2D graph.

    Args:
        positions (list): List of 2D arrays representing drone positions.
        angles (list): List of 2D arrays representing LIDAR angles in degrees.
        distances (list): List of 2D arrays representing LIDAR distances.
        sampling (int): Sampling rate for plotting LIDAR data. Defaults to 6.

    Returns:
        None
    """

    # Check inputs are valid
    assert isinstance(positions, list), "positions should be a list"
    assert isinstance(angles, list), "angles should be a list"
    assert isinstance(distances, list), "distances should be a list"
    assert (
        len(positions) == len(angles) == len(distances)
    ), "inputs should have the same length"

    fig, ax = plt.subplots(figsize=(15, 8))

    logHandle.log.info("preparing to plot flight path and sweep measurements.")
    randomState = numpy.random.RandomState(3)
    for index, position in enumerate(positions):
        color = tuple(
            (randomState.random(), randomState.random(), randomState.random())
        )

        # Plot the LIDAR data
        xPos = position[0] + distances[index][::sampling] * numpy.cos(
            angles[index][::sampling]
        )
        yPos = position[1] + distances[index][::sampling] * numpy.sin(
            angles[index][::sampling]
        )
        ax.scatter(xPos, yPos, color=color, marker="o", linewidths=1)

        # Plot the drone position
        ax.scatter(position[0], position[1], color="black", marker="o", linewidths=5)
        ax.annotate(
            f"P={index}",
            xy=position,
            xytext=(-20, 20),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

        # Connect wayPoints
        if index > 0:
            startPos = positions[index - 1]
            endPos = positions[index]
            ax.plot(
                [startPos[0], endPos[0]],
                [startPos[1], endPos[1]],
                color=color,
            )

    # Add labels and legend
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Drone Path and LIDAR Data")
    ax.legend(["LIDAR data"])
    plt.draw()
    plt.pause(0.001)
    input("Press [enter] to exit.")
