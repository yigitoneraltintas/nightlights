#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:47:46 2021


checks a linestring (wkt, csv) if it's in a polygon (wkt, another csv), 
if so calculates how much percent of that transect inside the polygon.


@author: yigit
"""
#%% libs
from shapely.wkt import loads
from pyproj import Geod
import pandas as pd

#%% import polygons (geojson)
df_polygons = pd.read_csv("wuerzburg_4pixels_51_52_53_54.csv")
df = pd.read_csv("nightlights-transect.csv")

#%%
#for würzburg create a new df
#only take rows with unique_ids betweeen 49004 and 49005. (würzburg's city code is 4.)
#for potsdam for example: unique_ids betweeen 49001 and 49002 (potsdam's city code is 1.)
df_wuerzburg = df.loc[(df['unique_id'] >= 4900400000 ) & (df['unique_id'] < 4900500000)]

#reset index for better function iteration
df_wuerzburg = df_wuerzburg.reset_index(drop=True)


#%%
#since our linestrings in wgs84
geod = Geod(ellps="WGS84")

#actual function, usage of shapely.wkt
#loads wkt_geometry and applies wgs84 projection
def calculate_length(transects):
    return geod.geometry_length(loads(transects))

#%%
#let's calculate transect_lengths for all dataframe

df_wuerzburg["transect_lengths"] = [calculate_length(x) for x in df_wuerzburg["geometry"]] # in meters
#df["transect_lengths_inside the polygon"] = 
#%%
#calculate transecth length inside the polygon

def calculate_intersect(transects, polygons):
    a = loads(transects)
    a_length = geod.geometry_length(a)
    b = loads(polygons)
    c = loads((a & b).wkt)
    c_length = geod.geometry_length(c)
    percent = (c_length / a_length) * 100
    
    return percent




#%%

# Iterating over two columns, use `zip`
#result = [f(x, y) for x, y in zip(df['col1'], df['col2'])]


df_wuerzburg["transect_percent"] = [calculate_intersect(x,y) for x,y in zip(df_wuerzburg["geometry"], df_polygons["WKT"])] 


#df_wuerzburg["transect_percent"] = df_wuerzburg.apply(lambda row: calculate_intersect(df_wuerzburg["geometry"], df_polygons["WKT"]), axis=1)
#%%
#problem is if it's completely out of boundaries it'll raise and error
#if it's fully inside or partially inside it will return a percent value.
a = loads(df_wuerzburg["geometry"][278])#linestring
a_length = geod.geometry_length(a)#linestring length
b = loads(df_polygons["WKT"][0])#polygon
c = loads((a & b).wkt) # & operator is the intersection
c_length = geod.geometry_length(c)#linestring length after intersection
percent = (c_length / a_length) * 100

#%%



a = loads(df_wuerzburg["geometry"][0])
a_length = geod.geometry_length(a)
b = loads(df_polygons["WKT"][0])
c = loads((a & b).wkt)
c_length = geod.geometry_length(c)
percent = (c_length / a_length) * 100
    
    
    




#%%

geod.geometry_length(loads(df["geometry"][0]))
a = loads(df["geometry"][0]).intersection(loads(df_polygons["WKT"][0]))
