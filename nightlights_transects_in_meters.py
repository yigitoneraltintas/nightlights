#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 11:45:02 2021

@author: yigit altintas
"""
#%%
import pandas as pd
from shapely.wkt import loads
from pyproj import Geod
#%%
#read data
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
def calculate_length(geometry):
    return geod.geometry_length(loads(geometry))

#%%
#create a new column with transect_lengths function
df_wuerzburg["transect_lengths_in_meter"] = [calculate_length(x) for x in df_wuerzburg["geometry"]]

#%%
#let's try calculating transect_lengths function for all dataframe
df["transect_lengths_in_meter"] = [calculate_length(x) for x in df["geometry"]]
#%%
#to .csv
df.to_csv("nightlights-transect-with-lengths.csv",index=False)

