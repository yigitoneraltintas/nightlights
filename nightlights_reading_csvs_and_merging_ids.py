#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 17:07:31 2021

Program to read in the Nachtlichter data into Pandas data frames, drop
columns that aren't needed, rename various variables, and then average
over the surveys to have one line per survey (mainly filled with zeros)

@author: yigit
"""

#%%

import pandas as pd

#%%pd.read_csv

# root_directory="/Users/kyba/python/Nachtlichter/"
# datadate = '20211217'

# datafile = root_directory+'input_data/'+datadate+'/nightlights-light-source.csv'
# survey_inp_file = root_directory+'temp_data/list_of_surveys.dat'
# lights_out_file = root_directory+'temp_data/light_summary.dat'


# df_survey = pd.read_csv(root_directory+'input_data/'+datadate+"/nightlights-survey.csv")
# df_source = pd.read_csv(root_directory+'input_data/'+datadate+"/nightlights-light-source.csv")
# df_transects = pd.read_csv(root_directory+'input_data/'+datadate+"/nightlights-transect.csv")
# #df_var_names = pd.read_csv("var_names.csv", header=None)
df_survey = pd.read_csv("nightlights-survey.csv")
df_source = pd.read_csv("nightlights-light-source.csv")
df_transects = pd.read_csv("nightlights-transect.csv")
df_var_names = pd.read_csv("var_names.csv", header=None)
 
#%%assign column headers for four of the csv's
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

#df_var_names.columns = ['names'] 

#%%
#dropping some unnecassery columns 
df_source.drop(columns=['individual_id', 'created_at', "type_value", "colour_value",
                        "brightness_value", "variant_value","status"],inplace=True, axis=1)

df_survey.drop(columns=['created_at', 'start_time', 'end_time',
       'street_lights_relative_height', 'street_lights_relative_height_value',
       'vehicle_frequency', 'vehicle_frequency_value',
       'motion_sensor_activity', 'motion_sensor_activity_value','user_username'],inplace=True, axis=1)

df_transects.drop(columns=['created_at', 'status', 'name',
       'user_generated', 'completed', 'user_username'],inplace=True, axis=1)

#%%drop flagged
df_survey = df_survey[~df_survey["status"].str.contains("FLAGGED")]
df_source = df_source.merge(df_survey,on="survey_id")
df_source = df_source.merge(df_transects,on="transect_id")

#print unique_types (all light categories)
#print(df_source["type"].unique())
#%%
df_source = df_source[['survey_id', 'unique_id', 'transect_id', 'count', 'user_username', 'status', 'type',
       'colour', 'brightness', 'variant',"geometry"]]


#Replace long names with shorter codes
#df_source.replace('videoscreens','vs',inplace=True)
#df_source.replace('bollards','bo',inplace=True)

df_source.replace('streetlights',      'SL',inplace=True)
df_source.replace('trafficlights',     'Traf',inplace=True)
df_source.replace('privatewindows',    'Wpri',inplace=True)
df_source.replace('commercialwindows', 'Wcom',inplace=True)
df_source.replace('mountedlights',     'Mtd',inplace=True)
df_source.replace('housenumber',       'Hnm',inplace=True)
df_source.replace('facadelighting',    'Fac',inplace=True)
df_source.replace('floodlights',       'Fld',inplace=True)
df_source.replace('pathlighting',      'Pth',inplace=True)
df_source.replace('bollards',          'Bol',inplace=True)
df_source.replace('orientationlights', 'Ori',inplace=True)
df_source.replace('canopylights',      'Can',inplace=True)
df_source.replace('illuminatedsignext','illS',inplace=True)
df_source.replace('selfluminoussign',  'slfS',inplace=True)
df_source.replace('videoscreens',      'Vid',inplace=True)
df_source.replace('lightstrings',      'Str',inplace=True)
df_source.replace('gardendecorations', 'Gar',inplace=True)
df_source.replace('other',             'Oth',inplace=True)

df_source.replace('orange',             'Org',inplace=True)
df_source.replace('white',              'Whi',inplace=True)

df_source.replace('dim',                'Dim',inplace=True)
df_source.replace('normal',             'Nor',inplace=True)
df_source.replace('bright',             'Bri',inplace=True)

df_source.replace('partly_shielded',    'Part',inplace=True)
df_source.replace('full_cutoff',        'Full',inplace=True)
df_source.replace('globe_style',        'Glob',inplace=True)
df_source.replace('no_shield',          'Glob',inplace=True)  #Floodlight class was called "no_shield"

df_source.replace('small',              'Sml',inplace=True)
df_source.replace('medium',             'Med',inplace=True)
df_source.replace('large',              'Lrg',inplace=True)
df_source.replace('extreme',            'Ext',inplace=True)


#Replace the nans with "na"

df_source[['type','colour','brightness','variant']] = df_source[['type','colour','brightness','variant']].fillna('na')

#Generate unique names for each type

df_source['lightsourceindex'] = df_source[['type','colour','brightness','variant']].agg('-'.join, axis=1)

#Recast the data in a wide format, fill missing values with zero

df_wide=df_source.pivot_table(index=['transect_id','survey_id'], columns='lightsourceindex', values='count', fill_value=0).reset_index()


#Compute the average over the surveys
df_wide_agg=df_source.pivot_table(index=['transect_id'], aggfunc='mean', columns='lightsourceindex', values='count', fill_value=0).reset_index()


len(df_source['lightsourceindex'].unique())

