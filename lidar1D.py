import os
import sys
import csv
import numpy
import argparse

DESCRIPTION = "Drone mapping and localization using 1D Lidar"


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

    # Print a message indicating how many samples were collected
    print(f"In total, the drone collected {len(angles)} samples from all sweeps.")

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

    # Read the flight path from the file
    print(f"Reading flight coordinates from {flightPath}")
    pathPoints = ReadFile(flightPath)

    # Parse the flight path into sweep IDs and path coordinates
    pointsList = []
    for points in pathPoints:
        pointsList.append(points)

    sweepIDs = numpy.array(pointsList[::2], dtype="uint8")[:, 0]
    pathCoordinates = numpy.array(pointsList[1::2], dtype="float32")

    # Print the sweep ID and location for each point in the flight path
    for sweepID, point in zip(sweepIDs, pathCoordinates):
        print(f"At sweep {sweepID}: drone was at location {point}")

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
        lidarSweepsList (list): List of dictionaries containing the angles and distances of each lidar sweep.

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
            print("At sweep={}, numSamples={}".format(numSweeps, int(distance)))
            numSweeps += 1
            sweepSamplesLengthList.append(int(distance))
    sweepSamplesLengthList = numpy.array(sweepSamplesLengthList)

    lidarSweepsList = []
    for sweepID in range(numSweeps):
        minIndex = (
            sweepSamplesLengthList[:sweepID].sum() + sweepID + 1 if sweepID > 0 else 0
        )
        maxIndex = sweepSamplesLengthList[: (sweepID + 1)].sum() + sweepID + 1
        print(
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


def main(args):
    """
    Reads flight path and LiDAR measurement files.

    Args:
        args (argparse.Namespace): A namespace object containing command-line arguments.

    Raises:
        AssertionError: If any required input arguments are missing or invalid.
    """

    # Check if flightPath and lidarPoints arguments are provided and valid files
    assert hasattr(args, "flightPath"), "The 'flightPath' argument is missing."
    assert args.flightPath, "No flight path filename provided."
    assert os.path.exists(
        args.flightPath
    ), f"Flight path file '{args.flightPath}' not found."
    assert os.path.isfile(args.flightPath), f"'{args.flightPath}' is not a file."

    assert hasattr(args, "lidarPoints"), "The 'lidarPoints' argument is missing."
    assert args.lidarPoints, "No LiDAR measurement filename provided."
    assert os.path.exists(
        args.lidarPoints
    ), f"LiDAR measurement file '{args.lidarPoints}' not found."
    assert os.path.isfile(args.lidarPoints), f"'{args.lidarPoints}' is not a file."

    # Read flight path and LiDAR measurements from files
    sweepIDs, pathCoordinates = GetFlightPathFromFile(args.flightPath)
    angles, distances = GetLidarMeasurementsFromFile(args.lidarPoints)

    # Extract measurements from each sweep
    lidarSweepsList = ExtractSweepsFromMeasurements(angles, distances)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description=DESCRIPTION,
        epilog="python3 lidar1D.py --flightPath <flight_path_file> --lidarPoints <lidar_measurements_file> --show",
    )
    parser.add_argument("--flightPath", help="path to flight path .csv file", type=str)
    parser.add_argument(
        "--lidarPoints", help="path to lidar measurements .csv file", type=str
    )
    parser.add_argument(
        "--show", help="flag to enable visualization", action="store_true"
    )
    args = parser.parse_args()
    main(args)
