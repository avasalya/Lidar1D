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

    fileHandler = open(fileName, 'r')
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

    sweepIDs = numpy.array(pointsList[::2], dtype='uint8')[:, 0]
    pathCoordinates = numpy.array(pointsList[1::2], dtype='float32')

    # Print the sweep ID and location for each point in the flight path
    for sweepID, point in zip(sweepIDs, pathCoordinates):
        print(f"At sweep {sweepID}: drone was at location {point}")

    # Return the arrays of sweep IDs and path coordinates
    return sweepIDs, pathCoordinates


def main(args):
    """
    Reads flight path and LiDAR measurement files.

    Args:
        args (argparse.Namespace): A namespace object containing command-line arguments.

    Raises:
        AssertionError: If any required input arguments are missing or invalid.
    """

    # Check if flightPath and lidarPoints arguments are provided and valid files
    assert hasattr(args, 'flightPath'), "The 'flightPath' argument is missing."
    assert args.flightPath, "No flight path filename provided."
    assert os.path.exists(args.flightPath), f"Flight path file '{args.flightPath}' not found."
    assert os.path.isfile(args.flightPath), f"'{args.flightPath}' is not a file."

    assert hasattr(args, 'lidarPoints'), "The 'lidarPoints' argument is missing."
    assert args.lidarPoints, "No LiDAR measurement filename provided."
    assert os.path.exists(args.lidarPoints), f"LiDAR measurement file '{args.lidarPoints}' not found."
    assert os.path.isfile(args.lidarPoints), f"'{args.lidarPoints}' is not a file."

    # Read flight path and LiDAR measurements from files
    sweepIDs, pathCoordinates = GetFlightPathFromFile(args.flightPath)
    angles, distances = GetLidarMeasurementsFromFile(args.lidarPoints)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION, epilog='python3 lidar1D.py --flightPath <flight_path_file> --lidarPoints <lidar_measurements_file> --show')
    parser.add_argument("--flightPath", help="path to flight path .csv file", type=str)
    parser.add_argument("--lidarPoints", help="path to lidar measurements .csv file", type=str)
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()
    main(args)
