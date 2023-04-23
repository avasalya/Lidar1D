#!/usr/bin/env python3
__author__ = "Ashesh Vasalya"
import os
import sys
import argparse
import matplotlib.pyplot as plt


from libs.lidarutils import (
    GetFlightPathFromFile,
    GetLidarMeasurementsFromFile,
    ExtractSweepsFromMeasurements,
    VisualizeMeasurementsPerSweep,
    VisualizeAllSweepsWithDronePath,
    logHandle,
)


DESCRIPTION = "Drone mapping and localization using 1D Lidar"


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

    if args.show:
        plt.ion()
        plt.show()

    # Read flight path and LiDAR measurements from files
    sweepIDs, pathCoordinates = GetFlightPathFromFile(args.flightPath)
    angles, distances = GetLidarMeasurementsFromFile(args.lidarPoints)

    # Extract measurements from each sweep
    lidarSweepsList = ExtractSweepsFromMeasurements(angles, distances)

    # Combine sweepID, drone position and lidar measurements
    logHandle.log.debug("Combine flight path position per sweep with lidar measurements.")
    for sweepID in sweepIDs:
        lidarSweepsList[sweepID].update(
            {"sweepID": sweepID, "coordinates": pathCoordinates[sweepID]}
        )

    # Visualize Lidar data per sweeps
    if args.sweepsInIsolation:
        VisualizeMeasurementsPerSweep(lidarSweepsList=lidarSweepsList, show=args.show)

    # Visualize all drone locations along with each sweep measurements
    if args.allSweepsCombined:
        VisualizeAllSweepsWithDronePath(lidarSweepsList=lidarSweepsList, show=args.show)


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
    parser.add_argument(
        "--sweepsInIsolation",
        help="flag to visualization all sweeps in isolation, --show must be set to true with this flag",
        action="store_true",
    )
    parser.add_argument(
        "--allSweepsCombined",
        help="flag to visualization all sweeps combined, --show must be set to true with this flag",
        action="store_true",
    )
    args = parser.parse_args()

    main(args)
    logHandle.log.debug("******    end of program, exiting.  *******")
