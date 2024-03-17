import xarray as xr
import pandas as pd

# Load NetCDF file
ds = xr.open_dataset('seNorge2018_2020.nc')

# Extract variables
time = ds['time'].values
latitude = ds['latitude'].values
longitude = ds['longitude'].values
tg = ds['tg'].values
rr = ds['rr'].values

# Extract units from variable attributes
units = {
    'time': ds['time'].attrs.get('units', ''),
    'latitude': ds['latitude'].attrs.get('units', ''),
    'longitude': ds['longitude'].attrs.get('units', ''),
    'tg': ds['tg'].attrs.get('units', ''),
    'rr': ds['rr'].attrs.get('units', ''),
}

# Repeat latitude and longitude to match the length of other arrays
latitude_repeated = latitude.repeat(tg.shape[0]).reshape(tg.shape)
longitude_repeated = longitude.repeat(tg.shape[0]).reshape(tg.shape)

# Create a DataFrame with units in the header
header = f"time ({units['time']}), latitude ({units['latitude']}), longitude ({units['longitude']}), tg ({units['tg']}), rr ({units['rr']})"
df = pd.DataFrame({
    'time': time,
    'latitude': latitude_repeated.flatten(),
    'longitude': longitude_repeated.flatten(),
    'tg': tg.flatten(),
    'rr': rr.flatten(),
})

# Save DataFrame to CSV
df.to_csv('extracted_data.csv', index=False, header=header)

