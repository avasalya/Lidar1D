#!/usr/bin/env python3
__author__ = "Ashesh Vasalya"
import sys
import argparse
import numpy
import matplotlib.pyplot as plt

from libs.lidarutils import VisualizeRandomFlightPathAndSweep, logHandle

DESCRIPTION = "Generate new LIDARDPoints data based on a new room layout and new plausible flight plan."


def main(args):
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

    if args.show:
        logHandle.log.debug("Plot the drone path and LIDAR data")
        VisualizeRandomFlightPathAndSweep(positionsList, anglesList, distancesList)

    logHandle.log.debug("Save LIDAR data to LIDARPoints.csv")
    WriteRandomFlightPathAndSweepData(anglesList, distancesList)


def WriteRandomFlightPathAndSweepData(anglesList, distancesList):
    """
    Converts the LIDARPoints data into a dictionary and saves it into a CSV file named LIDARPoints.csv.

    Args:
        anglesList (list): A list of angles of LIDAR sweeps.
        distancesList (list): A list of distances of LIDAR sweeps.

    Returns:
        None

    Raises:
        TypeError: If anglesList or distancesList is not a list or if they are empty lists.
    """
    # Assert that the input arguments are lists and are not empty
    assert (
        isinstance(anglesList, list) and len(anglesList) > 0
    ), "anglesList must be a non-empty list"
    assert (
        isinstance(distancesList, list) and len(distancesList) > 0
    ), "distancesList must be a non-empty list"

    lidarSweepsList = []
    for sweepID in range(len(anglesList)):
        sweepDict = {}
        for index in anglesList[sweepID]:
            sweepDict["sweepID"] = sweepID
            sweepDict["angles"] = anglesList[sweepID][index]
            sweepDict["distances"] = distancesList[sweepID][index]
            lidarSweepsList.append(sweepDict)

    # Assert that the converted data is not an empty list
    assert len(lidarSweepsList) > 0, "LIDARPoints data is empty"

    with open("LIDARPoints.csv", "w") as f:
        for sweepID in range(len(lidarSweepsList)):
            for key in lidarSweepsList[sweepID].keys():
                f.write("%s,%s\n" % (key, lidarSweepsList[sweepID][key]))

    # Assert that the CSV file was created and is not empty
    with open("LIDARPoints.csv", "r") as f:
        csv_data = f.read().splitlines()
        assert len(csv_data) > 0, "CSV file is empty"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description=DESCRIPTION,
    )
    parser.add_argument(
        "--show", help="flag to enable visualization", action="store_true"
    )

    args = parser.parse_args()

    if args.show:
        plt.ion()
        plt.show()

    main(args)
    logHandle.log.debug("******    end of program, exiting.  *******")
