# -*- coding: utf-8 -*-
"""
Created on Thr Dec 12

@author: sec001_group3
"""

#Exercise #5: Develop using “flask framework” a web service API encapsulating the model i.e. de-serialize
#We will develop a small flask app to:
#•	Load the model & columns
#•	Accept JASON new data generated  using POSTMAN simulator using the request module
#•	Convert the JASON format to the model format using the jsonify module
#•	Call the prediction service
#•	Return the predicted values as a list
#Note you can run the service at a port you specify as an argument when you call the api or it will default to the specified port in the script i.e. 12345. 
#Below is the code
from flask import Flask, request, jsonify
import traceback
import pandas as pd
import joblib
import sys
# Your API definition
app = Flask(__name__)

@app.route("/predict", methods=['GET','POST']) #use decorator pattern for the route
def predict():
    if lr:
        try:
            json_ = request.json
            print(json_)
            query = pd.get_dummies(pd.DataFrame(json_))
            query = query.reindex(columns=model_columns, fill_value=0)

            prediction = list(lr.predict(query))
            print({'prediction': str(prediction)})
            return jsonify({'prediction': str(prediction)})
            return "Welcome to titanic model APIs!"

        except:

            return jsonify({'trace': traceback.format_exc()})
    else:
        print ('Train the model first')
        return ('No model here to use')

if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 12346 # If you don't provide any port the port will be set to 12345

    lr = joblib.load('C:/Users/Daniel/Downloads/COMP309/Project2/pr2_sec001_gr3_bk_api.pkl') # Load "model.pkl"
    print ('Model loaded')
    model_columns = joblib.load('C:/Users/Daniel/Downloads/COMP309/Project2/pr2_sec001_gr3_bk_col.pkl') # Load "model_columns.pkl"
    print ('Model columns loaded')
    
    app.run(port=port, debug=True)
