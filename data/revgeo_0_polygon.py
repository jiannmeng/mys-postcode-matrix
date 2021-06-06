import json
from shapely.geometry import shape, Point
import datetime
from datetime import date, time
import time
import numpy as np
import pandas as pd

path_mysj = 'D:/Users/ectheve/Downloads/MySJ_SFTP/'
df = pd.read_csv(path_mysj + 'vax/vax_reg_2021-03-05.txt', sep='|', usecols=['LAT','LONG'], nrows=1000)
df.columns = ['lat', 'lon']

with open('json_dist_new.json') as f: districts = json.load(f)
# file also kept at https://raw.githubusercontent.com/Thevesh/Display/master/districts.json

def reverse_geocode(lon,lat):
    point = Point(lon, lat) # lon/lat
    for feature in districts['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point): return (feature['properties'])['dp_baru'].title()
        # if polygon.contains(point): return [(feature['properties'])['ADM1_EN'], (feature['properties'])['ADM2_EN']]

    return 'None'

# df = pd.read_csv('cases_coords.csv', parse_dates=['date_reg', 'date_true'], dayfirst=True)
# df = df[df['date_reg'].dt.date > date(2021,1,31)]
# df= df[['lon', 'lat']]

time_start = time.time()
df['district'] = df.apply(lambda x: reverse_geocode(x['lon'], x['lat']), axis = 1)
df.drop(['lon', 'lat'], axis = 1, inplace=True)
# df = df.groupby(['district']).size().reset_index()
# df.columns = ['district', 'cases']
# df.to_csv('cases_geocoded.csv', index = False)
print('----- Code ran in ' + "{:.3f}".format(time.time() - time_start) + ' seconds -----')