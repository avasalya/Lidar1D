#!/usr/bin/env python3
__author__ = "Ashesh Vasalya"

import numpy as numpy
import matplotlib.pyplot as plt

from libs.lidarutils import VisualizeRandomFlightPathAndSweep, logHandle


if __name__ == "__main__":
    plt.ion()
    plt.show()

    # Define the dimensions (meters) of the house
    width = 20.0
    length = 30.0

    # Define the dimensions of each room
    roomWidth = 5.0
    roomLength = 6.0

    # Calculate the number of rooms that can fit in the house
    roomsWidth = int(width // roomWidth)
    roomsLength = int(length // roomLength)

    # Generate the layout of the house
    numSamples = 360
    positionsList = []
    anglesList = []
    distancesList = []

    logHandle.log.debug("Generate some random data to simulate LIDAR measurements")
    for roomWidth in range(roomsWidth):
        for roomLength in range(roomsLength):
            # Random drone waypoints
            xPos = roomWidth * roomWidth + numpy.random.rand() * 2.0
            yPos = roomLength * roomLength + numpy.random.rand() * 2.0
            positionsList.append([xPos, yPos])

            # Random angle samples 0 to 360
            anglesList.append(numpy.random.randint(0, numSamples, numSamples))

            # Random distances in meters
            distancesList.append(numpy.random.random_sample(numSamples))

    logHandle.log.debug("Plot the drone path and LIDAR data")
    VisualizeRandomFlightPathAndSweep(positionsList, anglesList, distancesList)
