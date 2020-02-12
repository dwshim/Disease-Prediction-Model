# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 2019

@author: sec001_group3
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

path = "C:/Users/wooki/Desktop/COMP309/Dataset"
filename = 'Bicycle_Thefts.csv'
fullpath = os.path.join(path,filename)
dfc_bk_thefts = pd.read_csv(fullpath)

dfc_bk_thefts.isnull().sum()/len(dfc_bk_thefts)*100


## data grouping
## class information
dfc_bk_thefts['Status'].unique()
dfc_bk_thefts['Status'].value_counts()
dfc_bk_thefts['Status'].value_counts()/len(dfc_bk_thefts)*100
dfc_bk_thefts_rd=dfc_bk_thefts[(dfc_bk_thefts['Status']!='UNKNOWN')]

''' ------------------------------------- Class Information ----------------------------------------------- '''

dfc_class_rd=dfc_bk_thefts_rd[['Status']]
#import numpy as np
dfc_class_rd['Status']=np.where(dfc_class_rd['Status'] =='STOLEN', 0, dfc_class_rd['Status'])
dfc_class_rd['Status']=np.where(dfc_class_rd['Status'] =='RECOVERED', 1, dfc_class_rd['Status'])
dfc_class_rd.head()
dfc_class_rd.dtypes
dfc_class_rd=dfc_class_rd.astype({'Status':'int'})
dfc_class_rd.dtypes



''' ------------------------------------- Primary_Offence Information ----------------------------------------------- '''


dfc_crime_rd = pd.read_csv(fullpath)
dfc_crime_rd.columns.values

print(dfc_crime_rd['Primary_Offence'].value_counts())
dfc_crime_rd.shape
dfc_crime_rd.describe()
dfc_crime_rd.dtypes
dfc_crime_rd.head(5)

dfc_crime_rd=dfc_crime_rd[(dfc_crime_rd['Status']!='UNKNOWN')]

print(dfc_crime_rd['Primary_Offence'].unique())
print(dfc_crime_rd['Primary_Offence'].value_counts())
dfc_crime_rd.isnull().sum()

dfc_crime_rd_s=dfc_crime_rd[dfc_crime_rd.Status=='STOLEN']
dfc_crime_rd_r=dfc_crime_rd[dfc_crime_rd.Status=='RECOVERED']
print(dfc_crime_rd_s['Primary_Offence'].value_counts()/len(dfc_crime_rd_s)*100)
print(dfc_crime_rd_r['Primary_Offence'].value_counts()/len(dfc_crime_rd_r)*100)


dfc_crime_rd['Primary_Offence']=np.where((dfc_crime_rd['Primary_Offence'] !='THEFT UNDER')&
            (dfc_crime_rd['Primary_Offence'] !='THEFT UNDER - BICYCLE')&
            (dfc_crime_rd['Primary_Offence'] !='B&E')&
            (dfc_crime_rd['Primary_Offence'] !='THEFT OF EBIKE UNDER $5000')&
            (dfc_crime_rd['Primary_Offence'] !='POSSESSION PROPERTY OBC UNDER')&
            (dfc_crime_rd['Primary_Offence'] !='PROPERTY - FOUND')&
            (dfc_crime_rd['Primary_Offence'] !='FTC PROBATION ORDER')
            ,'OT', dfc_crime_rd['Primary_Offence'])


pd.crosstab(dfc_crime_rd.Primary_Offence,dfc_crime_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Crime')
plt.xlabel('Type of Crime')
plt.ylabel('Frequency of Crime')

pd.crosstab(dfc_crime_rd.Primary_Offence,dfc_crime_rd.Status).plot(kind='bar', colors=['darkorange'])
plt.title('Event Frequency for Crime')
plt.xlabel('Type of Crime')
plt.ylabel('Frequency of Crime')

pd.crosstab(dfc_crime_rd.Primary_Offence,dfc_crime_rd.Status).plot(kind='bar', colors=['darkblue'])
plt.title('Event Frequency for Crime')
plt.xlabel('Type of Crime')
plt.ylabel('Frequency of Crime')


''' ------------------------------------- Location Information ----------------------------------------------- '''

# Location Information

dfc_location_rd=dfc_bk_thefts_rd[['X', 'Y', 'Division', 'City', 'Location_Type', 'Premise_Type', 'Hood_ID', 'Neighbourhood', 'Lat', 'Long','Status']]
pd.set_option('display.max_columns',30)
dfc_location_rd.head()
dfc_location_rd_s=dfc_location_rd[dfc_location_rd.Status=='STOLEN']
dfc_location_rd_r=dfc_location_rd[dfc_location_rd.Status=='RECOVERED']

dfc_location_rd['compare_x']=np.where(dfc_location_rd['X']==dfc_location_rd['Long'],'true','false')
dfc_location_rd['compare_y']=np.where(dfc_location_rd['Y']==dfc_location_rd['Lat'],'true','false')
dfc_location_rd['compare_x'].value_counts()
dfc_location_rd['compare_y'].value_counts()

## no linear relationship

## clustering information
#import seaborn as sns
df_coordinates_rd=dfc_location_rd[['Long','Lat']]
df_coordinates_rd.plot(kind='scatter',x='Long',y='Lat',title='Total',figsize=(10,5))

df_coordinates_rd_s=dfc_location_rd[dfc_location_rd.Status=='STOLEN']
df_coordinates_rd_r=dfc_location_rd[dfc_location_rd.Status=='RECOVERED']

df_coordinates_rd_s.plot(kind='scatter',x='Long',y='Lat',title='STOLEN',figsize=(10,5))
df_coordinates_rd_r.plot(kind='scatter',x='Long',y='Lat',title='RECOVERED',figsize=(10,5))


from sklearn.cluster import KMeans
def elbow(df_coordinates_rd):
    sse = []
    for i in range(1,31):
        km=KMeans(n_clusters=i, init='k-means++', random_state=0)
        km.fit(df_coordinates_rd)
        sse.append(km.inertia_)
        
    plt.plot(range(1,31), sse, marker='o')
    plt.xlabel('cluster number')
    plt.ylabel('sse')
    plt.show()
elbow(df_coordinates_rd)

## populate KMeans method
model=KMeans(n_clusters=7)
model.fit(df_coordinates_rd)

## add cluster values to the original dataframe
md=pd.Series(model.labels_)
df_coordinates_rd['clust']=md
len(df_coordinates_rd)
print('values   count(%)')
df_coordinates_rd['clust'].value_counts()/len(df_coordinates_rd)*100


## histogram of clusters
plt.title('Histogram of Clusters')
plt.xlabel('Cluster')
plt.ylabel('Frequency')
plt.hist(df_coordinates_rd['clust'],color='#86bf91')

## grouping by mean value of each cluster
df_crd_clst_mean=df_coordinates_rd.groupby('clust').mean()
df_coordinates_rd.groupby('clust').mean()
sns.pairplot(df_crd_clst_mean)
df_crd_clst_mean.plot(kind='scatter',x='Long',y='Lat')


## homogeneous values
print('values   count(%)')
dfc_location_rd['City'].value_counts()/len(dfc_location_rd)*100

## similar meaning values
#import matplotlib.pyplot as plt
#pd.crosstab(dfc_location_rd.Division,dfc_location_rd.Status)
from itertools import cycle, islice
bar_colors = list(islice(cycle(['orange']), None, len(dfc_location_rd_s)))

pd.crosstab(dfc_location_rd.Division,dfc_location_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Division')
plt.xlabel('Division')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_location_rd_s.Division,dfc_location_rd_s.Status).plot(kind='bar', colors=['darkorange'])
plt.title('Event Frequency for Division')
plt.xlabel('Division')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_location_rd_r.Division,dfc_location_rd_r.Status).plot(kind='bar')
plt.title('Event Frequency for Division')
plt.xlabel('Division')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_location_rd.Hood_ID,dfc_location_rd.Status)
pd.crosstab(dfc_location_rd.Hood_ID,dfc_location_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Hood_ID')
plt.xlabel('Hood_ID')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_location_rd.Hood_ID,dfc_location_rd.Status)
pd.crosstab(dfc_location_rd_s.Hood_ID,dfc_location_rd_s.Status).plot(kind='bar', colors=bar_colors)
plt.title('Event Frequency for Hood_ID')
plt.xlabel('Hood_ID')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_location_rd.Hood_ID,dfc_location_rd.Status)
pd.crosstab(dfc_location_rd_r.Hood_ID,dfc_location_rd_r.Status).plot(kind='bar')
plt.title('Event Frequency for Hood_ID')
plt.xlabel('Hood_ID')
plt.ylabel('Frequency of Event')
## check the correlations 
#import seaborn as sns
x=dfc_location_rd[['Hood_ID','Division']]
sns.pairplot(x)

## value classification
print('values                                                                      count(%)')
dfc_location_rd['Location_Type'].value_counts()/len(dfc_location_rd)*100
pd.crosstab(dfc_location_rd.Location_Type,dfc_location_rd.Status).plot(kind='barh')
plt.title('Event Frequency for Location_Type')
plt.xlabel('Frequency of Event')
plt.ylabel('Location_Type')

dfc_location_rd['Premise_Type'].value_counts()/len(dfc_location_rd)*100
pd.crosstab(dfc_location_rd.Premise_Type,dfc_location_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Premise_Type')
plt.xlabel('Premise_Type')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_location_rd_s.Premise_Type,dfc_location_rd.Status).plot(kind='bar', colors=['orange'] )
plt.title('Event Frequency for Premise_Type')
plt.xlabel('Premise_Type')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_location_rd_r.Premise_Type,dfc_location_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Premise_Type')
plt.xlabel('Premise_Type')
plt.ylabel('Frequency of Event')
## data transformation
## value classification
#import numpy as np
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Apartment (Rooming House, Condo)', 'private_apartment', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Single Home, House (Attach Garage, Cottage, Mobile)', 'private_house', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Private Property (Pool, Shed, Detached Garage)', 'private_property', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Bar / Restaurant', 'commercial', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Streets, Roads, Highways (Bicycle Path, Private Road)', 'public_street', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Convenience Stores', 'commercial', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Parking Lots (Apt., Commercial Or Non-Commercial)', 'public_parking', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Other Commercial / Corporate Places (For Profit, Warehouse, Corp. Bldg', 'commercial_property', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Construction Site (Warehouse, Trailer, Shed)', 'private', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Gas Station (Self, Full, Attached Convenience)', 'commercial', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Other Non Commercial / Corporate Places (Non-Profit, Gov\'T, Firehall)', 'private', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Open Areas (Lakes, Parks, Rivers)', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Universities / Colleges', 'public_school', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Hospital / Institutions / Medical Facilities (Clinic, Dentist, Morgue)', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Schools During Un-Supervised Activity', 'public_school', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Schools During Supervised Activity', 'public_school', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Ttc Subway Station', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Commercial Dwelling Unit (Hotel, Motel, B & B, Short Term Rental)', 'commercial', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Religious Facilities (Synagogue, Church, Convent, Mosque)', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Police / Courts (Parole Board, Probation Office)', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Jails / Detention Centres', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Other Train Admin Or Support Facility', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Go Station', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Homeless Shelter / Mission', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Bank And Other Financial Institutions (Money Mart, Tsx)', 'commercial', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Other Train Tracks', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Retirement / Nursing Homes', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Go Train', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Dealership (Car, Motorcycle, Marine, Trailer, Etc.)', 'commercial', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Unknown', 'unknown', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Group Homes (Non-Profit, Halfway House, Social Agency)', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Ttc Bus Stop / Shelter / Loop', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Other Passenger Train', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Ttc Subway Train', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Ttc Admin Or Support Facility', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Ttc Bus', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Ttc Light Rail Transit Station', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Other Passenger Train Station', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Other Regional Transit System Vehicle', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Pharmacy', 'commercial', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Go Bus', 'public', dfc_location_rd['Location_Type'])
dfc_location_rd['Location_Type']=np.where(dfc_location_rd['Location_Type'] =='Retirement Home', 'public', dfc_location_rd['Location_Type'])

dfc_location_rd['Location_Type'].unique()
dfc_location_rd['Location_Type'].value_counts()

pd.crosstab(dfc_location_rd.Location_Type,dfc_location_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Location_Type')
plt.xlabel('Location_Type')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_location_rd_s.Location_Type,dfc_location_rd_s.Status).plot(kind='bar', colors=['orange'] )
plt.title('Event Frequency for Location_Type')
plt.xlabel('Location_Type')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_location_rd_r.Location_Type,dfc_location_rd_r.Status).plot(kind='bar')
plt.title('Event Frequency for Location_Type')
plt.xlabel('Location_Type')
plt.ylabel('Frequency of Event')


''' ------------------------------------- bike information ----------------------------------------------- '''


## bike information
dfc_bk_info_rd=dfc_bk_thefts_rd[['Bike_Make', 'Bike_Model', 'Bike_Type', 'Bike_Speed', 'Bike_Colour', 'Cost_of_Bike', 'Status']]

## Splitting recovered & stolen data
dfc_bk_info_rd_r=dfc_bk_info_rd[dfc_bk_info_rd.Status=='STOLEN']
dfc_bk_info_rd_s=dfc_bk_info_rd[dfc_bk_info_rd.Status=='RECOVERED']

## Checking percentage of values: stolen & recovered 
dfc_bk_info_rd_r['Bike_Type'].value_counts()/len(dfc_bk_info_rd_r)*100
dfc_bk_info_rd_s['Bike_Type'].value_counts()/len(dfc_bk_info_rd_s)*100


pd.crosstab(dfc_bk_info_rd.Bike_Type,dfc_bk_info_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Bike')
plt.xlabel('Bike_Type')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_bk_info_rd_r.Bike_Type,dfc_bk_info_rd_r.Status).plot(kind='bar', colors=['darkorange'])
plt.title('Event Frequency for Bike')
plt.xlabel('Bike_Type')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_bk_info_rd_s.Bike_Type,dfc_bk_info_rd_s.Status).plot(kind='bar', colors=['darkblue'])
plt.title('Event Frequency for Bike')
plt.xlabel('Bike_Type')
plt.ylabel('Frequency of Event')

## 7 features selected
#dfc_bk_info_rd=dfc_bk_thefts_rd[['Bike_Make', 'Bike_Model', 'Bike_Type', 'Bike_Speed', 'Bike_Colour', 'Cost_of_Bike', 'Status']]

## data transformation
## value classification
## import numpy as np

### ------------- for Bike Speed -------------
## Transformation to: 
##1. beginner (<10 mph)
##2. reasonable experienced (10-15 mph)
##3. more experienced (16-20 mph)
##4. professional rider (>21 mph)

##beginner (<10 mph)
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='0', 'beginner', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='1', 'beginner', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='2', 'beginner', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='3', 'beginner', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='4', 'beginner', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='5', 'beginner', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='6', 'beginner', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='7', 'beginner', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='8', 'beginner', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='9', 'beginner', dfc_bk_info_rd['Bike_Speed'])

##reasonable experienced (10-15 mph)
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='10', 'reasonable experienced', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='11', 'reasonable experienced', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='12', 'reasonable experienced', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='13', 'reasonable experienced', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='14', 'reasonable experienced', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='15', 'reasonable experienced', dfc_bk_info_rd['Bike_Speed'])

##more experienced (16-20 mph)
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='16', 'more experienced', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='17', 'more experienced', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='18', 'more experienced', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='19', 'more experienced', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='20', 'more experienced', dfc_bk_info_rd['Bike_Speed'])

##professional rider (>21 mph)
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='21', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='22', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='23', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='24', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='25', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='26', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='27', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='28', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='29', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='30', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='31', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='32', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='33', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='34', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='35', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='36', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='37', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='38', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='39', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='40', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='41', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='42', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='45', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='46', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='48', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='49', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='50', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='51', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='55', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='56', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='58', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='60', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='62', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='64', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='65', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='70', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='72', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='80', 'professional rider', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed']=np.where(dfc_bk_info_rd['Bike_Speed'] =='99', 'professional rider', dfc_bk_info_rd['Bike_Speed'])


###
dfc_bk_info_rd['Bike_Speed'].value_counts()/len(dfc_bk_info_rd)*100

## Splitting recovered & stolen data
dfc_bk_info_rd_r=dfc_bk_info_rd[dfc_bk_info_rd.Status=='STOLEN']
dfc_bk_info_rd_s=dfc_bk_info_rd[dfc_bk_info_rd.Status=='RECOVERED']

## Checking percentage of values: stolen & recovered 
dfc_bk_info_rd_r['Bike_Speed'].value_counts()/len(dfc_bk_info_rd_r)*100
dfc_bk_info_rd_s['Bike_Speed'].value_counts()/len(dfc_bk_info_rd_s)*100

pd.crosstab(dfc_bk_info_rd.Bike_Speed,dfc_bk_info_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Bike')
plt.xlabel('Bike_Speed')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_bk_info_rd_r.Bike_Speed,dfc_bk_info_rd_r.Status).plot(kind='bar', colors=['darkorange'])
plt.title('Event Frequency for Bike')
plt.xlabel('Bike_Speed')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_bk_info_rd_s.Bike_Speed,dfc_bk_info_rd_s.Status).plot(kind='bar', colors=['darkblue'])
plt.title('Event Frequency for Bike')
plt.xlabel('Bike_Speed')
plt.ylabel('Frequency of Event')


## Bike_Colour
###
## 7 features selected
dfc_bk_info_rd=dfc_bk_thefts_rd[['Bike_Make', 'Bike_Model', 'Bike_Type', 'Bike_Speed', 'Bike_Colour', 'Cost_of_Bike', 'Status']]

dfc_bk_info_rd['Bike_Colour']=np.where((dfc_bk_info_rd['Bike_Colour'] !='BLK   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='BLU   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='GRY   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='WHI   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='RED   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='SIL   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='GRN   ')
              ,'OT', dfc_bk_info_rd['Bike_Colour'])

dfc_bk_info_rd['Bike_Colour'].value_counts()/len(dfc_bk_info_rd)*100
pd.crosstab(dfc_bk_info_rd.Bike_Colour ,dfc_bk_info_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Bike_Colour')
plt.xlabel('Bike_Colour')
plt.ylabel('Frequency of Event')

## Splitting recovered & stolen data
dfc_bk_info_rd_r=dfc_bk_info_rd[dfc_bk_info_rd.Status=='STOLEN']
dfc_bk_info_rd_s=dfc_bk_info_rd[dfc_bk_info_rd.Status=='RECOVERED']

## Checking percentage of values: stolen & recovered 
dfc_bk_info_rd_r['Bike_Colour'].value_counts()/len(dfc_bk_info_rd_r)*100
dfc_bk_info_rd_s['Bike_Colour'].value_counts()/len(dfc_bk_info_rd_s)*100

pd.crosstab(dfc_bk_info_rd.Bike_Colour,dfc_bk_info_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Bike')
plt.xlabel('Bike_Colour')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_bk_info_rd_r.Bike_Colour,dfc_bk_info_rd_r.Status).plot(kind='bar', colors=['darkorange'])
plt.title('Event Frequency for Bike')
plt.xlabel('Bike_Colour')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_bk_info_rd_s.Bike_Colour,dfc_bk_info_rd_s.Status).plot(kind='bar', colors=['darkblue'])
plt.title('Event Frequency for Bike')
plt.xlabel('Bike_Colour')
plt.ylabel('Frequency of Event')


## Bike_Make (DROP)
dfc_bk_thefts_rd['Bike_Make'].value_counts()/len(dfc_bk_thefts_rd)*100
pd.crosstab(dfc_bk_thefts_rd.Bike_Make ,dfc_bk_thefts_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Bike_Make')
plt.xlabel('Bike_Make')
plt.ylabel('Frequency of Event')

###
from itertools import cycle, islice
bar_colors = list(islice(cycle(['orange']), None, len(dfc_bk_info_rd)))

pd.crosstab(dfc_bk_info_rd.Bike_Make,dfc_bk_info_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Bike')
plt.xlabel('Bike_Make')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_bk_info_rd.Bike_Make,dfc_bk_info_rd.Status).plot(kind='bar', colors=bar_colors)
plt.title('Event Frequency for Division')
plt.xlabel('Bike_Make')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_bk_info_rd.Bike_Make,dfc_bk_info_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Division')
plt.xlabel('Bike_Make')
plt.ylabel('Frequency of Event')


## Cost_of_Bike

dfc_bk_info_rd=dfc_bk_thefts_rd[['Bike_Make', 'Bike_Model', 'Bike_Type', 'Bike_Speed', 'Bike_Colour', 'Cost_of_Bike', 'Status']]

plt.boxplot(dfc_bk_info_rd['Cost_of_Bike'])

## Removing outliers
dfc_bk_info_rd3=dfc_bk_info_rd[(dfc_bk_info_rd['Cost_of_Bike']<1200)&(dfc_bk_info_rd['Cost_of_Bike']>0)]
plt.hist(dfc_bk_info_rd3['Cost_of_Bike'])
plt.title('Histogram of Cost_of_Bike')
plt.xlabel('Cost_of_Bike')
plt.ylabel('Frequency')

plt.boxplot(dfc_bk_info_rd3['Cost_of_Bike'])

##
dfc_bk_thefts_rd['Cost_of_Bike'].value_counts()/len(dfc_bk_thefts_rd)*100
pd.crosstab(dfc_bk_thefts_rd.Cost_of_Bike ,dfc_bk_thefts_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Cost_of_Bike')
plt.xlabel('Cost_of_Bike')
plt.ylabel('Frequency of Event')

## Splitting recovered & stolen data
dfc_bk_info_rd_r=dfc_bk_info_rd[dfc_bk_info_rd.Status=='STOLEN']
dfc_bk_info_rd_s=dfc_bk_info_rd[dfc_bk_info_rd.Status=='RECOVERED']

## Checking percentage of values: stolen & recovered 
dfc_bk_info_rd_r['Cost_of_Bike'].value_counts()/len(dfc_bk_info_rd_r)*100
dfc_bk_info_rd_s['Cost_of_Bike'].value_counts()/len(dfc_bk_info_rd_s)*100

pd.crosstab(dfc_bk_info_rd.Cost_of_Bike,dfc_bk_info_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Bike')
plt.xlabel('Cost_of_Bike')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_bk_info_rd_r.Cost_of_Bike,dfc_bk_info_rd_r.Status).plot(kind='bar', colors=['darkorange'])
plt.title('Event Frequency for Bike')
plt.xlabel('Cost_of_Bike')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_bk_info_rd_s.Cost_of_Bike,dfc_bk_info_rd_s.Status).plot(kind='bar', colors=['darkblue'])
plt.title('Event Frequency for Bike')
plt.xlabel('Cost_of_Bike')
plt.ylabel('Frequency of Event')


dfc_bk_thefts_rd['Cost_of_Bike'].describe()
dfc_bk_thefts_rd['Cost_of_Bike'].median()
df_bk_info_rd=dfc_bk_thefts_rd[['Cost_of_Bike','Bike_Colour','Bike_Type']]
df_bk_info_rd.groupby('Bike_Type').mean()
df_bk_info_rd.groupby('Bike_Type').median()
df_bk_info_rd.groupby('Bike_Make').mean()
df_bk_info_rd.groupby('Bike_Make').median()
df_bk_info_rd['Bike_Make'].unique()
df_bk_info_rd['Bike_Type'].unique()
df_bk_info_rd['Bike_Make'].value_counts()
df_bk_info_rd.dtypes

df_bk_info_rd.fillna("UK",inplace=True)

#import matplotlib.pyplot as plt
plt.boxplot(df_bk_info_rd['Cost_of_Bike'])
plt.show()

plt.hist(df_bk_info_rd['Cost_of_Bike'])
plt.title('Histogram of Cost_of_Bike')
plt.xlabel('Cost_of_Bike')
plt.ylabel('Frequency')

## remove outlier
df_bk_info_rd.fillna(df_bk_info_rd.median(),inplace=True)
df_bk_info_rd.isnull().sum()/len(df_bk_info_rd)*100
df_bk_info_rd['Cost_of_Bike'].median()


plt.boxplot(dfc_bk_info_rd['Cost_of_Bike'])

## Removing outliers
dfc_bk_info_rd3=dfc_bk_info_rd[(dfc_bk_info_rd['Cost_of_Bike']<1200)&(dfc_bk_info_rd['Cost_of_Bike']>0)]
plt.hist(dfc_bk_info_rd3['Cost_of_Bike'])
plt.title('Histogram of Cost_of_Bike')
plt.xlabel('Cost_of_Bike')
plt.ylabel('Frequency')

plt.boxplot(dfc_bk_info_rd3['Cost_of_Bike'])


''' ------------------------------------- time information ----------------------------------------------- '''


## time information
#import datetime
#d=pd.DataFrame(data=dfc_bk_thefts_rd['Occurrence_Date'],columns='Occur_Day_of_Week')
d=dfc_bk_thefts_rd['Occurrence_Date']
d.head()
date=d.str[0:4] + d.str[5:7] + d.str[8:10]
date=date.astype('datetime64[ns]')
date.head()
weekday=date.dt.weekday_name
weekday.head()
dfc_time_rd=pd.concat([dfc_bk_thefts_rd[['Occurrence_Date','Occurrence_Year','Occurrence_Month','Occurrence_Day','Occurrence_Time','Status']],weekday],axis='columns')
dfc_time_rd.columns=['Occurrence_Date','Occurrence_Year','Occurrence_Month','Occurrence_Day','Occurrence_Time','Status','Occurrence_Weekday']
dfc_time_rd.head(10)
dfc_time_rd_s=dfc_time_rd[dfc_time_rd.Status=='STOLEN']
dfc_time_rd_r=dfc_time_rd[dfc_time_rd.Status=='RECOVERED']


## Occurance features

# Occurance_Year

dfc_time_rd['Occurrence_Year'].value_counts()/len(dfc_time_rd)*100
#pd.crosstab(dfc_time_rd_s.Occurrence_Year,dfc_time_rd.Status).plot(kind='bar',colors=['darkorange'])
pd.crosstab(dfc_time_rd.Occurrence_Year,dfc_time_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Occurrence_Year')
plt.xlabel('Occurrence_Year')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_time_rd_s.Occurrence_Year,dfc_time_rd.Status).plot(kind='bar', colors=['darkorange'])
plt.title('Event Frequency for Occurrence_Year')
plt.xlabel('Occurrence_Year')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_time_rd_r.Occurrence_Year,dfc_time_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Occurrence_Year')
plt.xlabel('Occurrence_Year')
plt.ylabel('Frequency of Event')

# Occurance_Month

dfc_time_rd['Occurrence_Month'].value_counts()/len(dfc_time_rd)*100
pd.crosstab(dfc_time_rd.Occurrence_Month,dfc_time_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Occurrence_Month')
plt.xlabel('Occurrence_Month')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_time_rd_s.Occurrence_Month,dfc_time_rd.Status).plot(kind='bar', colors=['darkorange'])
plt.title('Event Frequency for Occurrence_Month')
plt.xlabel('Occurrence_Month')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_time_rd_r.Occurrence_Month,dfc_time_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Occurrence_Month')
plt.xlabel('Occurrence_Month')
plt.ylabel('Frequency of Event')

# Occurance_Month - Season

dfc_time_rd['Occurrence_Season']=np.where((dfc_time_rd['Occurrence_Month']>=3) & (dfc_time_rd['Occurrence_Month']<=5), 'Spring', dfc_time_rd['Occurrence_Month'])
dfc_time_rd['Occurrence_Season']=np.where((dfc_time_rd['Occurrence_Month']>=6) & (dfc_time_rd['Occurrence_Month']<=8), 'Summer', dfc_time_rd['Occurrence_Season'])
dfc_time_rd['Occurrence_Season']=np.where((dfc_time_rd['Occurrence_Month']>=9) & (dfc_time_rd['Occurrence_Month']<=11), 'Fall', dfc_time_rd['Occurrence_Season'])
dfc_time_rd['Occurrence_Season']=np.where((dfc_time_rd['Occurrence_Month']<=2) | (dfc_time_rd['Occurrence_Month']>=12), 'Winter', dfc_time_rd['Occurrence_Season'])

dfc_time_rd_s=dfc_time_rd[dfc_time_rd.Status=='STOLEN']
dfc_time_rd_r=dfc_time_rd[dfc_time_rd.Status=='RECOVERED']

dfc_time_rd['Occurrence_Season'].value_counts()/len(dfc_time_rd)*100
pd.crosstab(dfc_time_rd.Occurrence_Season,dfc_time_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Occurrence_Season')
plt.xlabel('Occurrence_Season')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_time_rd_s.Occurrence_Season,dfc_time_rd.Status).plot(kind='bar',colors=['darkorange'])
plt.title('Event Frequency for Occurrence_Season')
plt.xlabel('Occurrence_Season')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_time_rd_r.Occurrence_Season,dfc_time_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Occurrence_Season')
plt.xlabel('Occurrence_Season')
plt.ylabel('Frequency of Event')

# Occurance_Day
dfc_time_rd['Occurrence_Day'].value_counts()/len(dfc_time_rd)*100
pd.crosstab(dfc_time_rd.Occurrence_Day,dfc_time_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Occurrence_Day')
plt.xlabel('Occurrence_Day')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_time_rd_s.Occurrence_Day,dfc_time_rd.Status).plot(kind='bar',colors=['darkorange'])
plt.title('Event Frequency for Occurrence_Day')
plt.xlabel('Occurrence_Day')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_time_rd_r.Occurrence_Day,dfc_time_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Occurrence_Day')
plt.xlabel('Occurrence_Day')
plt.ylabel('Frequency of Event')

# Occurance_Weekday

dfc_time_rd['Occurrence_Weekday'].value_counts()/len(dfc_time_rd)*100
pd.crosstab(dfc_time_rd.Occurrence_Weekday,dfc_time_rd.Status).plot(kind='bar', stacked=True)
plt.title('Event Frequency for Occurrence_Weekday')
plt.xlabel('Occurrence_Weekday')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_time_rd_s.Occurrence_Weekday,dfc_time_rd.Status).plot(kind='bar',colors=['darkorange'])
plt.title('Event Frequency for Occurrence_Weekday')
plt.xlabel('Occurrence_Weekday')
plt.ylabel('Frequency of Event')

pd.crosstab(dfc_time_rd_r.Occurrence_Weekday,dfc_time_rd.Status).plot(kind='bar')
plt.title('Event Frequency for Occurrence_Weekday')
plt.xlabel('Occurrence_Weekday')
plt.ylabel('Frequency of Event')

# Occurance_Time
dfc_time_rd['Occurrence_Time'].value_counts()/len(dfc_time_rd)*100
dfc_time_rd.dtypes
dfc_time_rd_s['Occurrence_Time']=dfc_time_rd['Occurrence_Time'].str.replace(":",".",1).astype(float)
dfc_time_rd_r['Occurrence_Time']=dfc_time_rd['Occurrence_Time'].str.replace(":",".",1).astype(float)

plt.hist(dfc_time_rd_s['Occurrence_Time'],bins=10,color=['darkorange'])
plt.xlabel('Occurrence_Time')
plt.ylabel('Frequency')
plt.title('Occurrence_Time of STOLEN')

plt.hist(dfc_time_rd_r['Occurrence_Time'],bins=10)
plt.xlabel('Occurrence_Time')
plt.ylabel('Frequency')
plt.title('Occurrence_Time of RECOVERD')

dfc_time_rd['Occurrence_Time_N']=dfc_time_rd['Occurrence_Time'].str.replace(":",".",1).astype(float)
dfc_time_rd['Occurrence_Time']=np.where((dfc_time_rd['Occurrence_Time_N']>=6)
                                        &(dfc_time_rd['Occurrence_Time_N']<14)
                                        , 'morning', dfc_time_rd['Occurrence_Time'])
dfc_time_rd['Occurrence_Time']=np.where((dfc_time_rd['Occurrence_Time_N']>=14)
                                        &(dfc_time_rd['Occurrence_Time_N']<22)
                                        , 'afternoon', dfc_time_rd['Occurrence_Time'])
dfc_time_rd['Occurrence_Time']=np.where(((dfc_time_rd['Occurrence_Time_N']>=22)
                                        &(dfc_time_rd['Occurrence_Time_N']<24))
                                        |(dfc_time_rd['Occurrence_Time_N']<6)
                                        , 'night', dfc_time_rd['Occurrence_Time'])








