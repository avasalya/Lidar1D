#!/usr/bin/env python3
__author__ = "Ashesh Vasalya"

import numpy as numpy
import matplotlib.pyplot as plt

from libs import loghandler

logHandle = loghandler.LogHandler()


def GenerateRandomFlightPathAndSweep(positions, angles, distances):
    """
    Plot the drone flight path and simulated LIDAR measurements on a 2D graph.

    Args:
        positions (numpy.ndarray): Array of drone positions of shape (numSamples, 2).
        angles (numpy.ndarray): Array of LIDAR measurement angles in radians of length numSamples.
        distances (numpy.ndarray): Array of simulated LIDAR measurement distances of length numSamples.

    Returns:
        None.

    Raises:
        ValueError: If the input arrays are not of the correct shape and length.

    Examples:
        >>> positions = numpy.array([[0, 0], [1, 1], [2, 2]])
        >>> angles = numpy.array([0, 0.5 * numpy.pi, numpy.pi])
        >>> distances = numpy.array([1, 2, 1])
        >>> GenerateRandomFlightPathAndSweep(positions, angles, distances)

    """
    if (
        not isinstance(positions, numpy.ndarray)
        or not isinstance(angles, numpy.ndarray)
        or not isinstance(distances, numpy.ndarray)
    ):
        raise ValueError("Inputs must be numpy ndarrays.")
    if positions.shape[1] != 2:
        raise ValueError("Positions array must have shape (numSamples, 2).")
    if angles.shape[0] != distances.shape[0]:
        raise ValueError("Angles and distances arrays must have the same length.")

    logHandle.log.info("preparing to plot flight path and sweep measurements.")
    for index, position in enumerate(positions):
        # Plot the drone position
        ax.scatter(position[0], position[1], color="black", marker="o")
        ax.annotate(
            f"Position {index}",
            xy=position,
            xytext=(-20, 20),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

        # Plot the LIDAR data
        x = position[0] + distances * numpy.cos(angles)
        y = position[1] + distances * numpy.sin(angles)
        ax.plot(x, y, color="blue")

    # Add labels and legend
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Drone Path and LIDAR Data")
    ax.legend(["LIDAR data"])
    plt.draw()
    plt.pause(0.001)
    input("Press [enter] to exit.")


if __name__ == "__main__":
    logHandle.log.debug("Generate some random data to simulate LIDAR measurements")
    numSamples = 100
    angles = numpy.linspace(0, 2 * numpy.pi, numSamples, endpoint=False)
    distances = numpy.random.rand(numSamples)

    logHandle.log.debug("Generate some random drone positions")
    num_positions = 10
    positions = numpy.random.rand(num_positions, 2) * 10

    logHandle.log.debug("Plot the drone path and LIDAR data")
    plt.ion()
    plt.show()
    fig, ax = plt.subplots()

    GenerateRandomFlightPathAndSweep(positions, angles, distances)
