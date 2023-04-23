# Drone flight mapping and localization using 2D Lidar

## `lidar_analysis.py`
> This script is designed to read flight path and LiDAR measurement files and extract and visualize data from them. It takes command-line arguments using `argparse` module, and the functionality of the script depends on the arguments passed.

### Required Arguments
- `--flightPath`: A path to a file containing flight path coordinates.
- `--lidarPoints`: A path to a file containing LiDAR measurements.

### Optional Arguments
- `--show`: Display the visualizations in a window. Default is `False`.
- `--sweepsInIsolation`: Visualize LiDAR data for each sweep separately. Default is `False`.
- `--allSweepsCombined`: Visualize all drone locations along with each sweep's measurements. Default is `False`.

### Functionality
- Check if required input arguments are present and valid files.
- Read flight path and LiDAR measurements from files.
- Extract measurements from each sweep.
- Combine sweep ID, drone position, and LiDAR measurements.
- Visualize LiDAR data per sweeps.
- Visualize all drone locations along with each sweep's measurements.

### Usage
`python lidar_analysis.py --flightPath <pathToFlightPath.csv> --lidarPoints <pathToLidarData.csv> [--show] [--sweepsInIsolation] [--allSweepsCombined]`

- `--flightPath`: Path to the flight path coordinates file.
- `--lidarPoints`: Path to the LiDAR measurements file.
- `--show`: Display the visualizations in a window.
- `--sweepsInIsolation`: Visualize LiDAR data for each sweep separately.
- `--allSweepsCombined`: Visualize all drone locations along with each sweep's measurements.

- example: `python3 lidar_analysis.py --flightPath ./data/FlightPath.csv --lidarPoints ./data/LIDARPoints.csv --show --sweepsInIsolation --allSweepsCombined`

# Results
## TASK 1:
### Create a program to provide an appropriate visualization of the drone’s path and the LIDAR data. Ideally, the display should be able to show 1 sweep (1 scan ID) of data in isolation as well as all the sweeps combined together. This can be on separate displays or on the same display (with individual sweeps shown by highlighting for example)
> ## Individual sweeps
![sweepID_0](output/sweepID_0.png)
![sweepID_1](output/sweepID_1.png)
![sweepID_2](output/sweepID_2.png)
![sweepID_3](output/sweepID_3.png)
![sweepID_4](output/sweepID_4.png)
![sweepID_5](output/sweepID_5.png)
![sweepID_6](output/sweepID_6.png)
![sweepID_7](output/sweepID_7.png)
![sweepID_8](output/sweepID_8.png)
![sweepID_9](output/sweepID_9.png)
![sweepID_10](output/sweepID_10.png)
![sweepID_11](output/sweepID_11.png)
![sweepID_12](output/sweepID_12.png)
![sweepID_13](output/sweepID_13.png)
![sweepID_14](output/sweepID_14.png)
![sweepID_15](output/sweepID_15.png)
![sweepID_16](output/sweepID_16.png)
![sweepID_17](output/sweepID_17.png)
![sweepID_18](output/sweepID_18.png)
![sweepID_19](output/sweepID_19.png)
![sweepID_20](output/sweepID_20.png)
![sweepID_21](output/sweepID_21.png)
![sweepID_22](output/sweepID_22.png)
![sweepID_23](output/sweepID_23.png)
![sweepID_24](output/sweepID_24.png)
![sweepID_25](output/sweepID_25.png)
![sweepID_26](output/sweepID_26.png)
![sweepID_27](output/sweepID_27.png)
![sweepID_28](output/sweepID_28.png)
![sweepID_29](output/sweepID_29.png)
![sweepID_30](output/sweepID_30.png)
![sweepID_31](output/sweepID_31.png)
![sweepID_32](output/sweepID_32.png)
![sweepID_33](output/sweepID_33.png)

> ## All sweeps combined with flight path
![flightPathWombinedScans](output/dronePathAndScans.png)
