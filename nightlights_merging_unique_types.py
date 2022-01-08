#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 23:07:43 2021

@author: yigit
"""

#%%

import pandas as pd
import numpy as np

#%%pd.read_csv
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

df_var_names.columns = ['names'] 

#%%
#dropping some unnecassery columns 
df_source.drop(columns=['individual_id', 'created_at', "type_value", "colour_value",
                        "brightness_value", "variant_value","status"],inplace=True, axis=1)

df_survey.drop(columns=['created_at', 'start_time', 'end_time',
       'street_lights_relative_height', 'street_lights_relative_height_value',
       'vehicle_frequency', 'vehicle_frequency_value',
       'motion_sensor_activity', 'motion_sensor_activity_value','user_username'],inplace=True, axis=1)

#dropping some unnecassery columns
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

#%%


result = []
print(df_var_names["names"].str.split('_').str[0])
print(df_var_names["names"].str.split('_').str[5])

#%%



# if df_var_names["names"].str.split('_').str[0] != "NaN":
#     print(df_var_names["names"].str.split('_').str[0])
    

#%%
# for i in df_var_names["names"]:
#     print(df_var_names["names"].str.split('_').str[0])
    
#%%
df_source["colour"] = df_source["colour"].astype('category')
#obj_df.dtypes

#%%
df_source["colour_cat"] = df_source["colour"].cat.codes
#df_source.head()





#df_source["colour_value"] = np.where(df_source.loc[df_source["colour"] == "white",df_source["colour_value"]0])
    
#df_source["type_index"] = 7

#df_source.loc[df_source["color_value"]] == "white"
#df_source["colour_value"] = np.where(df_source["colour"]=="orange"),"1")


#%%


#%%df_result columns


df_result = df_source.assign(
    
    
     ###
     streetlights_FCO_Wh_Di = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='full_cutoff') &
                                 (df_source['colour']=='white') &
                                 (df_source['brightness']=='dim')
                                 ,df_source["count"],0),
     
     streetlights_FCO_Wh_No = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='full_cutoff') &
                                 (df_source['colour']=='white') &
                                 (df_source['brightness']=='normal')
                                 ,df_source["count"],0),
     
     streetlights_FCO_Wh_Br = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='full_cutoff') &
                                 (df_source['colour']=='white') &
                                 (df_source['brightness']=='bright')
                                 ,df_source["count"],0),
     
     
     ###
     streetlights_FCO_Or_Di = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='full_cutoff') &
                                 (df_source['colour']=='orange') &
                                 (df_source['brightness']=='dim')
                                 ,df_source["count"],0),
     
     streetlights_FCO_Or_No = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='full_cutoff') &
                                 (df_source['colour']=='orange') &
                                 (df_source['brightness']=='normal')
                                 ,df_source["count"],0),
     
     streetlights_FCO_Or_Br = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='full_cutoff') &
                                 (df_source['colour']=='orange') &
                                 (df_source['brightness']=='bright')
                                 ,df_source["count"],0),
     
     
     ###
     streetlights_FCO_Ot_Di = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='full_cutoff') &
                                 (df_source['colour']=='other') &
                                 (df_source['brightness']=='dim')
                                 ,df_source["count"],0),
     
     streetlights_FCO_Ot_No = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='full_cutoff') &
                                 (df_source['colour']=='other') &
                                 (df_source['brightness']=='normal')
                                 ,df_source["count"],0),
     
     streetlights_FCO_Ot_Br = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='full_cutoff') &
                                 (df_source['colour']=='other') &
                                 (df_source['brightness']=='bright')
                                 ,df_source["count"],0),
     
     
     ###
     streetlights_PS_Wh_Di = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='partly_shielded') &
                                 (df_source['colour']=='white') &
                                 (df_source['brightness']=='dim')
                                 ,df_source["count"],0),
     
     streetlights_PS_Wh_No = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='partly_shielded') &
                                 (df_source['colour']=='white') &
                                 (df_source['brightness']=='normal')
                                 ,df_source["count"],0),
     
     streetlights_PS_Wh_Br = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='partly_shielded') &
                                 (df_source['colour']=='white') &
                                 (df_source['brightness']=='bright')
                                 ,df_source["count"],0),
     
     
     ###
     streetlights_PS_Or_Di = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='partly_shielded') &
                                 (df_source['colour']=='orange') &
                                 (df_source['brightness']=='dim')
                                 ,df_source["count"],0),
     
     streetlights_PS_Or_No = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='partly_shielded') &
                                 (df_source['colour']=='orange') &
                                 (df_source['brightness']=='normal')
                                 ,df_source["count"],0),
     
     streetlights_PS_Or_Br = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='partly_shielded') &
                                 (df_source['colour']=='orange') &
                                 (df_source['brightness']=='bright')
                                 ,df_source["count"],0),
     
     
     ###
     streetlights_PS_Ot_Di = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='partly_shielded') &
                                 (df_source['colour']=='other') &
                                 (df_source['brightness']=='dim')
                                 ,df_source["count"],0),
     
     streetlights_PS_Ot_No = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='partly_shielded') &
                                 (df_source['colour']=='other') &
                                 (df_source['brightness']=='normal')
                                 ,df_source["count"],0),
     
     streetlights_PS_Ot_Br = np.where((df_source['type']=='streetlights') &
                                 (df_source['variant']=='partly_shielded') &
                                 (df_source['colour']=='other') &
                                 (df_source['brightness']=='bright')
                                 ,df_source["count"],0),
     
     
    ###
    streetlights_GL_Wh_Di = np.where((df_source['type']=='streetlights') &
                                (df_source['variant']=='globe_style') &
                                (df_source['colour']=='white') &
                                (df_source['brightness']=='dim')
                                ,df_source["count"],0),
    
    streetlights_GL_Wh_No = np.where((df_source['type']=='streetlights') &
                                (df_source['variant']=='globe_style') &
                                (df_source['colour']=='white') &
                                (df_source['brightness']=='normal')
                                ,df_source["count"],0),
    
    streetlights_GL_Wh_Br = np.where((df_source['type']=='streetlights') &
                                (df_source['variant']=='globe_style') &
                                (df_source['colour']=='white') &
                                (df_source['brightness']=='bright')
                                ,df_source["count"],0),
    
    
    ###
    streetlights_GL_Or_Di = np.where((df_source['type']=='streetlights') &
                                (df_source['variant']=='globe_style') &
                                (df_source['colour']=='orange') &
                                (df_source['brightness']=='dim')
                                ,df_source["count"],0),
    
    streetlights_GL_Or_No = np.where((df_source['type']=='streetlights') &
                                (df_source['variant']=='globe_style') &
                                (df_source['colour']=='orange') &
                                (df_source['brightness']=='normal')
                                ,df_source["count"],0),
    
    streetlights_GL_Or_Br = np.where((df_source['type']=='streetlights') &
                                (df_source['variant']=='globe_style') &
                                (df_source['colour']=='orange') &
                                (df_source['brightness']=='bright')
                                ,df_source["count"],0),
    

    ###
    streetlights_GL_Ot_Di = np.where((df_source['type']=='streetlights') &
                                (df_source['variant']=='globe_style') &
                                (df_source['colour']=='other') &
                                (df_source['brightness']=='dim')
                                ,df_source["count"],0),
    
    streetlights_GL_Ot_No = np.where((df_source['type']=='streetlights') &
                                (df_source['variant']=='globe_style') &
                                (df_source['colour']=='other') &
                                (df_source['brightness']=='normal')
                                ,df_source["count"],0),
    
    streetlights_GL_Ot_Br = np.where((df_source['type']=='streetlights') &
                                (df_source['variant']=='globe_style') &
                                (df_source['colour']=='other') &
                                (df_source['brightness']=='bright')
                                ,df_source["count"],0),


     

     
     ).groupby('survey_id').agg({'streetlights_FCO_Wh_Di':sum, 
                                 'streetlights_FCO_Wh_No':sum, 
                                 "streetlights_FCO_Wh_Br":sum,
                                 "streetlights_FCO_Or_Di":sum,
                                 "streetlights_FCO_Or_No":sum,
                                 'streetlights_FCO_Or_Br':sum, 
                                 'streetlights_FCO_Ot_Di':sum, 
                                 "streetlights_FCO_Ot_No":sum,
                                 "streetlights_FCO_Ot_Br":sum,
                                 "streetlights_PS_Wh_Di":sum,
                                 'streetlights_PS_Wh_No':sum, 
                                 "streetlights_PS_Wh_Br":sum,
                                 "streetlights_PS_Or_Di":sum,
                                 'streetlights_PS_Or_No':sum, 
                                 "streetlights_PS_Or_Br":sum,
                                 "streetlights_PS_Ot_Di":sum,
                                 'streetlights_PS_Ot_No':sum, 
                                 "streetlights_PS_Ot_Br":sum,
                                 "streetlights_GL_Wh_Di":sum,
                                 'streetlights_GL_Wh_No':sum, 
                                 "streetlights_GL_Wh_Br":sum,
                                 "streetlights_GL_Or_Di":sum,
                                 "streetlights_GL_Or_No":sum,
                                 'streetlights_GL_Or_Br':sum, 
                                 "streetlights_GL_Ot_Di":sum,
                                 "streetlights_GL_Ot_No":sum,
                                 "streetlights_GL_Ot_Br":sum})
                                       
                                 


#%%create df_var_names
#streetlights

# types = df_source["type"].unique().tolist()
# direction = ["FCO", "PS", "GL"]
# size = ["Sm","Me","La","Ex"]
# colour = ["Wh","Or","Ot"]
# brightness = ["Di", "No", "Br"]



types = df_source["type"].unique().tolist()
direction = ["nan"]
size = ["Sm","Me","La","Ex"]
colour = ["Wh","Or","Ot"]
brightness = ["Di", "No", "Br"]

names =[]
for a in types:
    for b in direction:
        for c in size:
            for d in colour:
                for e in brightness:
                    print(a,"_",b,"_",c,"_",d,"_",e,sep = '')#,end=' ')
  
# df_var_names = pd.read_csv("var_names.csv", header=None)
# df_var_names.columns = ['names']                
# p_windows = df_var_names[df_var_names['names'].str.contains('streetlights')]
# p_windows = p_windows['names'].str.replace('_nan', '')

