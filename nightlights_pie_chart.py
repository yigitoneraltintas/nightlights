#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:52:42 2021

@author: yigit
reads all three csv's from the NB app's download button at the top right side of the page. 
https://lichter.nachtlicht-buehne.de
categories them and creates pie chart for a given WKT polygon. 

"""
#%%importing libs
import pandas as pd
import geopandas as gpd
import numpy as np
import shapely.wkt
import matplotlib.pyplot as plt

#%%pd.read_csv
df_survey = pd.read_csv("nightlights-survey.csv")
df_source = pd.read_csv("nightlights-light-source.csv")
df_transects = pd.read_csv("nightlights-transect.csv")

#%%assign column headersfor three of the csv's
df_transects.columns = ['transect_id','created_at','geometry','status','unique_id',
                        'name','user_generated', 'completed', 'user_username' ]

df_survey.columns = ['survey_id','created_at', 'status', 'start_time', 'end_time',
        'street_lights_relative_height', 'street_lights_relative_height_value',
        'vehicle_frequency', 'vehicle_frequency_value',
        'motion_sensor_activity', 'motion_sensor_activity_value', 'transect_id',
        'user_username']

df_source.columns = ['individual_id', 'created_at', 'status', 'type', 'type_value', 'count', 'colour',
       'colour_value', 'brightness', 'brightness_value', 'variant',
       'variant_value', 'survey_id', 'user_username']
#%%removing nans from df_source. 3773 rows to 37783 rows
df_source.dropna(subset = ["survey_id"], inplace=True)

#dropping some unnecassery columns 
df_source.drop(columns=['individual_id', 'created_at',"status",'type_value','colour',
       'colour_value', 'brightness', 'brightness_value', 'variant',
       'variant_value', 'user_username'],inplace=True, axis=1)

#%%change float to int64
# print("before:",df_source['survey_id'].dtype)
# df_source['survey_id'] = df_source['survey_id'].astype('int64')
# print("after:",df_source['survey_id'].dtype)

#print unique_types (all light categories)
print(df_source["type"].unique())

#%%our main categories, no need to run, just for info
# streetlights = ["streetlights"]
# area = ["mountedlights","litdoorway","pathlighting","bollards","orientationlights",
#         "canopylights","housenumber"]
# private_windows = ["privatewindows"]
# commercial_windows = ["commercialwindows"]
# decorative = ["facadelighting","floodlights","lightstrings","gardendecorations"]
# signs = ["illuminatedsignext","selfluminoussign","videoscreen"]
# other = ["other","trafficlights"]

#%%creates categorized and sum calculated df. 
df_result = df_source.assign(
    
     street_lights = np.where(df_source['type']=='streetlights',df_source["count"],0),
     private_windows = np.where(df_source['type']=='privatewindows',df_source["count"],0),
     commercial_windows = np.where(df_source['type']=='commercialwindows',df_source["count"],0),
     
     other = np.where((df_source['type']=='other') |
                      (df_source['type']=='trafficlights')
                      ,df_source["count"],0),
     
     signs = np.where((df_source['type']=='illuminatedsignext') |
                      (df_source['type']=='selfluminoussign')|
                      (df_source['type']=='videoscreens')
                      ,df_source["count"],0),
     
     decorative = np.where((df_source['type']=='facadelighting') |
                      (df_source['type']=='floodlights')|
                      (df_source['type']=='lightstrings')|
                      (df_source['type']=='gardendecorations')
                      ,df_source["count"],0),
     
     area = np.where((df_source['type']=='mountedlights') |
                      (df_source['type']=='litdoorway')|
                      (df_source['type']=='pathlighting')|
                      (df_source['type']=='bollards')|
                      (df_source['type']=='orientationlights')|
                      (df_source['type']=='canopylights')|
                      (df_source['type']=='housenumber')
                      ,df_source["count"],0)
     
     ).groupby('survey_id').agg({'street_lights':sum, 
                                 'private_windows':sum, 
                                 "commercial_windows": sum,
                                 "other":sum,
                                 "signs":sum,
                                 "decorative":sum,
                                 "area":sum})

#%%creates a total(sum) column after categorization.
df_result['total'] =  df_result[['street_lights', 'private_windows', "commercial_windows",
                           "other","signs","decorative","area" ]].sum(axis=1)
df_result.reset_index(level=0, inplace=True)

#%% drop duplicates (didn't do it for now, because, the approch might not be right )
# result2 = result[['street_lights', 'private_windows', 'commercial_windows', 'other',
#        'signs', 'decorative', 'area', 'total']].drop_duplicates()
# result2.reset_index(level=0, inplace=True)

#%%
#dropping some unnecassery columns
df_survey.drop(columns=['created_at', 'status', 'start_time', 'end_time',
       'street_lights_relative_height', 'street_lights_relative_height_value',
       'vehicle_frequency', 'vehicle_frequency_value',
       'motion_sensor_activity', 'motion_sensor_activity_value',
       'user_username'],inplace=True, axis=1)

#dropping some unnecassery columns
df_transects.drop(columns=['created_at', 'status', 'name',
       'user_generated', 'completed', 'user_username'],inplace=True, axis=1)


#%% transfers df_survey to df_result where survey_id on both equals!
df_result = df_result.merge(df_survey,on="survey_id")

#rename columns
df_result = df_result[["survey_id","transect_id",'street_lights', 'private_windows', "commercial_windows",
                             "other","signs","decorative","area","total" ]]
#%% transfers df_transects to df_result where transect_id on both equals!
df_result = df_result.merge(df_transects,on="transect_id")

#rename columns
df_result = df_result[['survey_id', 'transect_id','unique_id', 'street_lights', 'private_windows',
       'commercial_windows', 'other', 'signs', 'decorative', 'area', 'total',
       'geometry' ]]

#%% transform geometry column to GeoSeries of gpd
df_result['geometry'] = gpd.GeoSeries.from_wkt(df_result['geometry'])

#idk what below line does actually but it kinda required
df_geo = gpd.GeoDataFrame(df_result, geometry='geometry')
#%%calculate "city" stats with a given polygon

#pass any WKT polygon here (like below, or any geometry for that matter), 
#of course it better have some transects in it, check the app's website.
city = shapely.wkt.loads("MultiPolygon (((12.41525787489443999 51.3095441308201714, 12.38004864119655224 51.30979782134517109, 12.38558816721413791 51.32908061030641278, 12.41120764454499081 51.32817168986019141, 12.41525787489443999 51.3095441308201714)))	")		


df_geo["city"] = df_geo.within(city)
df_city = df_geo.loc[df_geo['city'] == True]
#%%creates a pie chart with the pre_defined colors and categories.

data = df_city.loc[:, 'street_lights':'area']
my_labels = ['Straßenlichter', 'Fenster', 'Schaufenster', 'Sonstiges',
       'Schilder', 'Dekorativ', 'Flächenbeleuchtung']
my_labels_eng = ['Street lights', 'Private Windows', 'Commercial Windows', 'Others',
       'Signs', 'Decorative', 'Area Lighting']
colors = ['#E4E814','#C3D3DA','#808A8E','#D5CFAF',"#4388D6","#49CD5B","#E78F1E"]
plt.subplots(figsize = (8,8))
#change below title for the city you chose...
plt.title('Leipzig',y=1.15,fontweight='bold',fontsize=20)
#change to my_labels_eng below to change to english labels on chart
plt.pie(data.sum(),labels=my_labels,colors=colors,autopct='%1.1f%%', 
        startangle=90,pctdistance=1.15, labeldistance=1.26)
plt.axis('equal')
#change below name for the city you chose...
#plt.savefig('leipzig.png', bbox_inches='tight', dpi=600)
#%% save df_result.csv
df_city.to_csv("df_leipzig.csv",index=True)
