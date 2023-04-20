
# Lidar1D
Drone mapping and localization using 1D Lidar

## To Run

```
python3 lidar1D.py --help
usage: lidar1D.py [-h] [--flightPath FLIGHTPATH] [--lidarPoints LIDARPOINTS] [--show]

Drone mapping and localization using 1D Lidar

optional arguments:
  -h, --help            show this help message and exit
  --flightPath FLIGHTPATH
                        path to flight path .csv file
  --lidarPoints LIDARPOINTS
                        path to lidar measurements .csv file
  --show

python3 lidar1D.py --flightPath <flight_path_file> --lidarPoints <lidar_measurements_file> --show
```