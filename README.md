# nc2csv_Norway
#I have a netcdf files and I convert netcdf to csv files for a specific positions 


#Step 1 & 2
#Extract data from netcdf temperature and precipitation for 5 polygons covering time-period 2020,2021,2022,2023 (4 years)

# here is the link of the netcdf files Climate for Norway 
https://thredds.met.no/thredds/catalog/senorge/seNorge_2018/Archive/catalog.html

# here how to run the program line by line 
python 3tfile.py -o out -v tg,rr seNorge2018_2020.nc
