import argparse
import xarray as xr
import numpy as np
import pandas as pd
import os
import re

LOCATIONS = {
    '423': (60.389069, 7.552627),
    '547': (61.784950, 7.414164),
    '362': (59.398596, 6.931038),
    '64': (59.200001, 6.944359),
    '397': (59.887709, 7.471728),
    '815': (61.283674, 8.134310),
}

def get_sorted_wrf_files(folder):
    # Get all files in the folder
    files = os.listdir(folder)

    # Define a regex pattern for matching the desired file format
    pattern = re.compile(r'wrfout_d02_(\d{4})-(\d{2})-(\d{2})_(\d{3})')

    # Filter files matching the pattern
    wrf_files = [file for file in files if pattern.match(file)]

    # Sort the files based on their names
    sorted_wrf_files = sorted(wrf_files, key=lambda x: pattern.match(x).groups())

    # Return the sorted files with full paths
    return [os.path.join(folder, file) for file in sorted_wrf_files]

def extract_data(nc_file, lat, lon, variables):
    # Open the NetCDF file using xarray
    ds = xr.open_dataset(nc_file)

    # Extract latitude and longitude
    latitude = ds['lat'].values
    longitude = ds['lon'].values

    # Calculate distances from the specified point
    distances = np.sqrt((latitude - lat)**2 + (longitude - lon)**2)

    # Find the index of the minimum distance
    min_index = np.unravel_index(np.argmin(distances), distances.shape)

    # Extract variable data
    data = {}
    for variable in variables:
        if variable in ds.variables:
            # Extract variable data at the nearest latitude and longitude
            data[variable] = ds[variable].values[:, min_index[0], min_index[1]]

    # Extract time data
    time = pd.to_datetime(ds['time'].values).strftime('%Y-%m-%d')

    # Close the xarray dataset
    ds.close()

    return time, latitude[min_index], longitude[min_index], data

def main():
    parser = argparse.ArgumentParser(description='Extract data from NetCDF file and export to CSV.')
    parser.add_argument('nc_file', type=str, help='Path to the NetCDF file (seNorge2018_2020.nc)')
    parser.add_argument('-v', '--variables', type=str, help='Comma-separated list of variables', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output folder name', default='output')

    args = parser.parse_args()

    # Extract data for each location
    for location_name, (lat, lon) in LOCATIONS.items():
        # Extract data from the specified NetCDF file for the current location
        time, _, _, data = extract_data(args.nc_file, lat, lon, args.variables.split(','))

        # Create a DataFrame
        df = pd.DataFrame({'time': time, **data})

        # Create the output folder if it doesn't exist
        output_folder = os.path.join(args.output)
        os.makedirs(output_folder, exist_ok=True)

        # Write DataFrame to CSV
        output_file = os.path.join(output_folder, f'output_{location_name}.csv')
        df.to_csv(output_file, index=False)

        print(f"Data for {location_name} exported to {output_file}")

if __name__ == '__main__':
    main()

