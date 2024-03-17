import xarray as xr
import pandas as pd

# Load NetCDF file
ds = xr.open_dataset('seNorge2018_2020.nc')

# Desired latitude and longitude values
desired_lat = 60.479235
desired_lon = 8.660653

# Find nearest latitude and longitude indices
lat_idx = abs(ds.latitude - desired_lat).argmin().item()
lon_idx = abs(ds.longitude - desired_lon).argmin().item()

# Extract variables for the nearest latitude and longitude
tg = ds['tg'][:, lat_idx, lon_idx].values
rr = ds['rr'][:, lat_idx, lon_idx].values

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

