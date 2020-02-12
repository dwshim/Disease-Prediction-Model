# -*- coding: utf-8 -*-
"""
Created on Thr Dec 12

@author: sec001_group3
"""

import pandas as pd
import os
import numpy as np

path = "C:/Users/Daniel/Downloads/COMP309/Project2/"
filename = 'Bicycle_Thefts.csv'
fullpath = os.path.join(path,filename)
dfc_bk_thefts = pd.read_csv(fullpath)


##8.	Drop the rows 
dfc_bk_thefts_rd=dfc_bk_thefts[(dfc_bk_thefts['Status']!='UNKNOWN')]

dfc_class_rd=dfc_bk_thefts_rd[['Status']]
dfc_class_rd['Status']=np.where(dfc_class_rd['Status'] =='STOLEN', 0, dfc_class_rd['Status'])
dfc_class_rd['Status']=np.where(dfc_class_rd['Status'] =='RECOVERED', 1, dfc_class_rd['Status'])
dfc_class_rd=dfc_class_rd.astype({'Status':'int'})
dfc_class_rd.dtypes

dfc_crime_rd=dfc_bk_thefts_rd[['Primary_Offence','Status']]
dfc_crime_rd['Primary_Offence']=np.where((dfc_crime_rd['Primary_Offence'] !='THEFT UNDER')&
            (dfc_crime_rd['Primary_Offence'] !='THEFT UNDER - BICYCLE')&
            (dfc_crime_rd['Primary_Offence'] !='B&E')&
            (dfc_crime_rd['Primary_Offence'] !='THEFT OF EBIKE UNDER $5000')&
            (dfc_crime_rd['Primary_Offence'] !='POSSESSION PROPERTY OBC UNDER')&
            (dfc_crime_rd['Primary_Offence'] !='PROPERTY - FOUND')&
            (dfc_crime_rd['Primary_Offence'] !='FTC PROBATION ORDER')
            ,'OT', dfc_crime_rd['Primary_Offence'])


dfc_location_rd=dfc_bk_thefts_rd[['X', 'Y', 'Division', 'City', 'Location_Type', 'Premise_Type', 'Hood_ID', 'Neighbourhood', 'Lat', 'Long','Status']]
df_coordinates_rd=dfc_location_rd[['Long','Lat']]
from sklearn.cluster import KMeans
model=KMeans(n_clusters=7)
model.fit(df_coordinates_rd)
md=pd.Series(model.labels_)
dfc_location_rd['Clust']=md


dfc_time_rd=dfc_bk_thefts_rd[['Occurrence_Date','Occurrence_Year','Occurrence_Month','Occurrence_Day','Occurrence_Time','Status']]
# identify day of week from date
d=dfc_bk_thefts_rd['Occurrence_Date']
d.head()
date=d.str[0:4] + d.str[5:7] + d.str[8:10]
date=date.astype('datetime64[ns]')
date.head()
weekday=date.dt.weekday_name
weekday.head()
dfc_time_rd=pd.concat([dfc_bk_thefts_rd[['Occurrence_Date','Occurrence_Year','Occurrence_Month','Occurrence_Day','Occurrence_Time','Status']],weekday],axis=1)
dfc_time_rd.columns=['Occurrence_Date','Occurrence_Year','Occurrence_Month','Occurrence_Day','Occurrence_Time','Status','Occurrence_Weekday']
# classification about time zone
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


dfc_bk_info_rd=dfc_bk_thefts_rd[['Bike_Make', 'Bike_Model', 'Bike_Type', 'Bike_Speed', 'Bike_Colour', 'Cost_of_Bike', 'Status']]
dfc_bk_info_rd.fillna(dfc_bk_info_rd.median(),inplace=True)
dfc_bk_info_rd['Bike_Colour']=np.where((dfc_bk_info_rd['Bike_Colour'] !='BLK   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='BLU   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='GRY   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='WHI   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='RED   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='SIL   ')
              &(dfc_bk_info_rd['Bike_Colour'] !='GRN   ')
              ,'OT', dfc_bk_info_rd['Bike_Colour'])
dfc_bk_info_rd['Bike_Speed_C']=np.where((dfc_bk_info_rd['Bike_Speed']>=0)
                                        &(dfc_bk_info_rd['Bike_Speed']<10)
                                        , 'beginner', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed_C']=np.where((dfc_bk_info_rd['Bike_Speed']>=10)
                                        &(dfc_bk_info_rd['Bike_Speed']<16)
                                        , 'experienced', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed_C']=np.where((dfc_bk_info_rd['Bike_Speed']>=16)
                                        &(dfc_bk_info_rd['Bike_Speed']<21)
                                        , 'advanced', dfc_bk_info_rd['Bike_Speed'])
dfc_bk_info_rd['Bike_Speed_C']=np.where((dfc_bk_info_rd['Bike_Speed']>=21)
                                        , 'professional', dfc_bk_info_rd['Bike_Speed'])

#dfc_bk_features=pd.concat([dfc_location_rd[['Division','Premise_Type','Hood_ID']],df_coordinates_rd[['clust']],dfc_time_rd[['Occurrence_Month','Occurrence_Day','Occurrence_Weekday']],df_bk_info_rd[['Bike_Type','Cost_of_Bike']]],axis='columns')
dfc_bk_features=pd.concat([dfc_location_rd.drop(['Status'], axis=1),dfc_time_rd.drop(['Status'], axis=1),dfc_bk_info_rd.drop(['Status'], axis=1),dfc_crime_rd.drop(['Status'], axis=1),dfc_class_rd],axis=1)
print('features            count(%)')
dfc_bk_features.isnull().sum()/len(dfc_bk_features)*100

#identify features for final features
last_vars=['Status'
          ,'Premise_Type'
          ,'Division'
          ,'Hood_ID'
#          ,'Clust'
          ,'Occurrence_Month'
#          ,'Occurrence_Day'
#          ,'Occurrence_Weekday'
#          ,'Occurrence_Time'
          ,'Bike_Type'
#          ,'Bike_Colour'
#          ,'Bike_Speed_C'
#          ,'Cost_of_Bike'
#          ,'Primary_Offence'
          ]
dfc_bk_features= dfc_bk_features[last_vars]

#identify features for get_dummies
cat_vars=['Premise_Type'
          ,'Division'
          ,'Hood_ID'
#          ,'Clust'
          ,'Occurrence_Month'
#          ,'Occurrence_Day'
#          ,'Occurrence_Weekday'
#          ,'Occurrence_Time'
          ,'Bike_Type'
#          ,'Bike_Colour'
#          ,'Bike_Speed_C'
#          ,'Primary_Offence'
          ]
df_ohe = pd.get_dummies(dfc_bk_features, columns=cat_vars, dummy_na=False)
df_ohe['Status'].value_counts()/len(df_ohe)*100


from sklearn import preprocessing
# Get column names first
names = df_ohe.columns

## normalizing
normalizer = preprocessing.Normalizer().fit(df_ohe)  # fit does nothing
normalized_df = normalizer.transform(df_ohe)
normalized_df = pd.DataFrame(normalized_df, columns=names)

#scaled_df = normalized_df
#normalized_df =df_ohe

# standardization
scaler = preprocessing.StandardScaler()
scaled_df = scaler.fit_transform(normalized_df)
scaled_df = pd.DataFrame(scaled_df, columns=names)


dependent_variable = 'Status'
x = scaled_df[scaled_df.columns.difference([dependent_variable])]
#x.dtypes
#y = scaled_df[dependent_variable]
y = dfc_bk_features[dependent_variable]
#y.dtypes
#convert the class back into integer
y = y.astype(int)
y.value_counts()/len(scaled_df)*100

# Split the data into train test
from sklearn.model_selection import train_test_split
trainX,testX,trainY,testY = train_test_split(x,y, test_size = 0.2)

#LogisticRegression Model
from sklearn.linear_model import LogisticRegression
lrc = LogisticRegression(solver='lbfgs')
lrc.fit(trainX, trainY)

##DecisionTreeClassifier Model
#from sklearn.tree import DecisionTreeClassifier
#dtc = DecisionTreeClassifier(criterion='entropy',max_depth=200, min_samples_split=20, random_state=99)
#dtc.fit(trainX, trainY)
#
##RandomForestClassifier Model
#from sklearn.ensemble import RandomForestClassifier
#rfc = RandomForestClassifier(n_estimators=10)
#rfc.fit(trainX, trainY)


# Score the model using 10 fold cross validation
from sklearn.model_selection import KFold
crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
from sklearn.model_selection import cross_val_score
score = np.mean(cross_val_score(lrc, trainX, trainY, scoring='accuracy', cv=crossvalidation, n_jobs=1))
print ('The score of the 10 fold run is: ',score)

#13.	Test the model using the 20% testing data
#o	Use the predict method
#o	Import the metrics module
#o	Print the accuracy
#o	Print the confusion matrix
from sklearn import metrics 
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
testY_predict = lrc.predict(testX)
testY_predict.dtype

#labels = y.unique()
#print(labels)
print("Accuracy:",metrics.accuracy_score(testY, testY_predict))
#print("Confusion matrix \n" , confusion_matrix(testY, testY_predict, labels))
print("Confusion matrix--------- \nSTOLEN:0 , RECOVERD: 1")
print("------------------------- ")
print(pd.crosstab(testY,testY_predict,rownames=['Actual'],colnames=['Predictions']))
print("------------------------- \n")
print("f1_score:",f1_score(testY, testY_predict))
print("recall_score:",recall_score(testY, testY_predict))
#print(testX.columns.values)

## upsampling
y=df_ohe.Status
X=df_ohe.drop(['Status'], axis=1)

# setting up testing and training sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=27)
# concatenate our training data back together
X = pd.concat([X_train, y_train], axis=1)

# separate minority and majority Statuses
bk_stolen = X[X.Status==0]
bk_recovered = X[X.Status==1]

# upsample minority
from sklearn.utils import resample
bk_recovered_upsampled = resample(bk_recovered,
                          replace=True, # sample with replacement
                          n_samples=len(bk_stolen), # match number in majority Status
                          random_state=27) # reproducible results

# combine majority and upsampled minority
upsampled = pd.concat([bk_stolen, bk_recovered_upsampled])
# check new Status counts
upsampled.Status.value_counts()

# trying logistic regression again with the balanced dataset
y_train = upsampled.Status
X_train = upsampled.drop('Status', axis=1)

upsampled = LogisticRegression(solver='liblinear').fit(X_train, y_train)
upsampled_pred = upsampled.predict(X_test)
y_test.value_counts()

print("Accuracy:",metrics.accuracy_score(y_test, upsampled_pred))
#print("Confusion matrix \n" , confusion_matrix(y_test, upsampled_pred, labels))
print("Confusion matrix--------- \nSTOLEN:0 , RECOVERD: 1")
print("------------------------- ")
print(pd.crosstab(y_test,upsampled_pred,rownames=['Actual'],colnames=['Predictions']))
print("------------------------- \n")
print("f1_score:",f1_score(y_test, upsampled_pred))
print("recall_score:",recall_score(y_test, upsampled_pred))
#print(X_test.columns.values)

##14.	Serialize (save) the model as an object
##o	Import joblib
##o	Use the dump method to create the model pickle object
#import joblib 
#joblib.dump(lrc, 'C:/Users/Daniel/Downloads/COMP309/Project2/pr2_sec001_gr3_bk_api.pkl')
#print("Model dumped!")
#
##15.	Serialize save the model columns as an object
#model_columns = list(x.columns)
#print(model_columns)
#joblib.dump(model_columns, 'C:/Users/Daniel/Downloads/COMP309/Project2/pr2_sec001_gr3_bk_col.pkl')
#print("Models columns dumped!")


