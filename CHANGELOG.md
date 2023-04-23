# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2023-04-23
## Changed
- Refactor whole project structure in order to test individual functionalities.
- Moved all helper functions to `libs/lidarutils.py`
- Split `lidar_analysis.py` into `main.py` and `lidarutils.py`
- `lidarutils.py` contains all the required utilites and data extraction logics.
- `main.py` is the starting point to read and visualize the data from `FlightPath.csv` and `LIDARPoints.csv`
- Redesign logging based on the original design by guys from the internet. Made it into a standalone Class to have shared usage across the whole pipeline.
- README updated with instructions on project structure and library usage. some libraries are opensource and credit goes to respective original authors.

[2.0.0]: https://github.com/avasalya/Lidar1D/releases/tag/v2.0.0

## [1.3.0] - 2023-04-23

## Added
- Moved mappig library to a new location libs/
- Custom logger library added
- `VisualizeAllSweepsWithDronePath()` function added to combine and visualize flight path and all lidar measurements.
- Updated README, added output data from `VisualizeMeasurementsPerSweep()`.
- Added optional argument `--sweepsInIsolation` Visualize LiDAR data for each sweep separately. Default is `False`.
- Added optional argument `--allSweepsCombined` Visualize all drone locations along with each sweep's measurements. Default is `False`.
- Added output of Task 1, to visualize all data in isolation and combined from all scans.

## Changed
- Replaced usage of `prints` with standard `logging`.
- Renamed `lidar1D.py` to `lidar_analysis.py`.
- Updated README, added detailed docuementation on the usage of `lidar_analysis.py`.
- Doctstring of several functions updated to match consistent style format.
- Use random colors to visualize flight path.
- Draw each sweep figures in background on idle.

## Removed
- Removed `try and except` on `KeyboardInterrupt` from `VisualizeMeasurementsPerSweep()`.

[1.3.0]: https://github.com/avasalya/Lidar1D/releases/tag/v1.3.0

## [1.2.0] - 2023-04-22

## Added
- `VisualizeMeasurementsPerSweep()` function to visualize lidar measurements and grid map per sweep.
- OpenSource library added `https://atsushisakai.github.io/PythonRobotics` to compute grid map from lidar sweep data.
- Output files from `VisualizeMeasurementsPerSweep()` added to output folder.

## Changed
- Fixed usage and crashing of matplotlib at the end of program.
- README updated with output results to visualize each sweep data.

[1.2.0]: https://github.com/avasalya/Lidar1D/releases/tag/v1.2.0

## [1.1.1] - 2023-04-21

### Added
- Combined sweepID, drone position and lidar measurement data.
- Added support to visualize data using matplotlib.

## [1.1.0] - 2023-04-21

### Added
- `GetUnitConversionScale()` function to get conversion factor between distance units.
- `ExtractSweepsFromMeasurements()` function to extract individual lidar sweeps from measurements data.

### Changed
- README updated to add usage of `--show` flag.

[1.1.0]: https://github.com/avasalya/Lidar1D/releases/tag/v1.1.0

## [1.0.1] - 2023-04-21

### Changed
 - "Black" formatter applied to `lidar1D.py`

## [1.0.0] - 2023-04-21

### Added
- Initial version of the Drone mapping and localization using 1D Lidar project.
- `ReadFile()` function to open and read a CSV file.
- `GetLidarMeasurementsFromFile()` function to read a lidar measurements file and return arrays of angles and distances.
- `GetFlightPathFromFile()` function to read a flight path file and return arrays of sweep IDs and path coordinates.
- `main()` function to read flight path and LiDAR measurement files.

### Changed
- None

### Removed
- None

[1.0.0]: https://github.com/avasalya/Lidar1D/releases/tag/v1.0.0