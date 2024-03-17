import xarray as xr
import pandas as pd
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Earth radius in kilometers
    r = 6371.0
    
    # Distance in kilometers
    return c * r

# Load NetCDF file
ds = xr.open_dataset('seNorge2018_2020.nc')

# Desired latitude and longitude values
desired_lat = 60.479235
desired_lon = 8.660653

# Calculate distances to all latitudes and longitudes in the dataset
distances = haversine(desired_lat, desired_lon, ds.latitude, ds.longitude)

# Find the index of the minimum distance
idx_min = np.argmin(distances)

# Extract variables for the nearest latitude and longitude
tg = ds['tg'][:, idx_min].values
rr = ds['rr'][:, idx_min].values

# Extract time variable and format it
time = pd.to_datetime(ds['time'].values).strftime('%Y-%m-%d')

# Create DataFrame
df = pd.DataFrame({
    'time': time,
    'tg': tg,
    'rr': rr,
})

# Save DataFrame to CSV
df.to_csv('extracted_data.csv', index=False)

