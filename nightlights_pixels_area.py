#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 12:42:50 2021

reads polygons from csv, calculates their area.

@author: yigit
"""
#%% libs
from shapely.wkt import loads
from pyproj import Geod
import pandas as pd

#%% import polygons (wkt) (our table untouched)
df = pd.read_csv("transects_pixel_values_and_unique_ids.csv")

#slice complete pixels
df_completed = df[df['status'].str.match("complete")]

#drop unnecessary columns
df = df.drop(columns=['country #', 'cities count#', "project_area",
                      'last unique_id',"Unnamed: 8","Unnamed: 9", "Unnamed: 10"])

#%%
#since our polygons in wgs84
geod = Geod(ellps="WGS84")

#%% define the function. return absolute value of "first return value" from geometry_area function.
def calculate_area(polygons):
    return abs(geod.geometry_area_perimeter(loads(polygons))[0])

#%% calculate for every polygon
df["area_in_sqm"] = [calculate_area(x) for x in df["pixel_wkt"]]
df_completed["area_in_sqm"] = [calculate_area(x) for x in df_completed["pixel_wkt"]]

#%%rearrange some columns
df = df[["pixel_value", "pixel_id", "status","area_in_sqm","pixel_wkt"]]
df_completed = df_completed[["pixel_value", "pixel_id", "status","area_in_sqm","pixel_wkt"]]

#%% sum values in km squared for both total and complete pixels
total = df['area_in_sqm'].sum()
total_completed = df_completed['area_in_sqm'].sum()
print("all pixels in square meters",(total))
print("all pixels in square kilometers",(total/1e6))
print("completed in square meters",(total_completed))
print("completed in square kilometers",(total_completed/1e6))