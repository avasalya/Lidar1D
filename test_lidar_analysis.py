#!/usr/bin/env python3
__author__ = "Ashesh Vasalya"

import numpy
import pytest

from libs.lidarutils import ExtractSweepsFromMeasurements


class TestExtractSweepsFromMeasurements:
    """Test class for ExtractSweepsFromMeasurements function"""

    def test_empty_arrays(self):
        """Test function to ensure the function raises an AssertionError
        when empty arrays are passed as input.
        """
        with pytest.raises(AssertionError):
            angles = numpy.array([])
            distances = numpy.array([])
            ExtractSweepsFromMeasurements(angles, distances)

    def test_different_array_lengths(self):
        """Test function to ensure the function raises an AssertionError
        when arrays of different lengths are passed as input.
        """
        with pytest.raises(AssertionError):
            angles = numpy.array([0, 90, 180])
            distances = numpy.array([1, 2])
            ExtractSweepsFromMeasurements(angles, distances)

    def test_angles_outside_range(self):
        """Test function to ensure the function raises an AssertionError
        when the angles array contains values outside the range [0, 360).
        """
        with pytest.raises(AssertionError):
            angles = numpy.array([0, 90, 360, 450])
            distances = numpy.array([1, 2, 3, 4])
            ExtractSweepsFromMeasurements(angles, distances)

    def test_non_numeric_values(self):
        """Test function to ensure the function raises a TypeError
        when non-numeric values are passed as input.
        """
        with pytest.raises(TypeError):
            angles = numpy.array([0, 90, 180, "270"])
            distances = numpy.array([1, 2, 3, 4])
            ExtractSweepsFromMeasurements(angles, distances)

    def test_negative_values(self):
        """Test function to ensure the function raises an AssertionError
        when the distances array contains negative values.
        """
        with pytest.raises(AssertionError):
            angles = numpy.array([0, 90, 180, 270])
            distances = numpy.array([1, 2, -3, 4])
            ExtractSweepsFromMeasurements(angles, distances)

    def test_nan_values(self):
        """Test function to ensure the function raises a ValueError
        when NaN values are passed as input.
        """
        with pytest.raises(Exception):
            angles = numpy.array([0, 90, numpy.nan, 270])
            distances = numpy.array([1, 2, 3, 4])
            ExtractSweepsFromMeasurements(angles, distances)

    def test_inf_values(self):
        """Test function to ensure the function raises a ValueError
        when Inf values are passed as input.
        """
        with pytest.raises(Exception):
            angles = numpy.array([0, 90, numpy.inf, 270])
            distances = numpy.array([1, 2, 3, 4])
            ExtractSweepsFromMeasurements(angles, distances)
