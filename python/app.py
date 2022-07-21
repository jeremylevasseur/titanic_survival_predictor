'''
    Author: Jeremy Levasseur
    Last Updated: 2021-06-16
    Comments:

'''

# ========== Importing Third Party Libraries ==========
from decimal import *
import os
from flask import Flask, request, render_template, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
from numpy.core.numeric import NaN
from pprint import pprint
from datetime import date
import warnings
import joblib

warnings.filterwarnings("ignore")
getcontext().prec = 2


# ========== Importing Custom Libraries ==========


# ========== Importing Constants ==========


# ========== Defining Constants ==========
# filePath = "./data/housing.csv"
numericalColumns = [
    "Pclass",
    "Age",
    "SibSp",
    "Parch",
    "Fare"
]
categoricalColumns = [
    "Sex",
    "Embarked"
]
columnOrderToFollow = numericalColumns + categoricalColumns

# ========== Initializing App ==========
model = joblib.load('./models/model_1.pkl')
modelPipeline = joblib.load('./pipelines/model_1_pipeline.pkl')


app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['DEBUG'] = True

# Loading in dataframe from excel spreadsheet
# dataFrame = pd.read_csv(filePath)


# ========== Predictor Function ==========
def getPrediction(queryData):
    global model, modelPipeline, categoricalColumns, numericalColumns, columnOrderToFollow
    xColumnTitles = categoricalColumns + numericalColumns
    xDataFrameDict = {}
    for columnTitle in columnOrderToFollow:
        if columnTitle in xColumnTitles:
            xDataFrameDict[columnTitle] = [queryData[columnTitle]]

    xDataFrame = pd.DataFrame(xDataFrameDict)
    xPreparedDataFrame = modelPipeline.transform(xDataFrame)
    xPredictionRow = np.array([xPreparedDataFrame[-1]])
    prediction = model.predict(xPredictionRow)
    return int(prediction[0])


# ========== Creating Endpoints ==========
@app.route('/api/v1/get_prediction', methods=['POST'])
@cross_origin(supports_credentials=True)
def getPredictionEndpoint():
    '''
        Example POST Body:
            {
                "ticketClass": 1,
                "age": 37,
                "sex": "male",
                "sibsp": 1,
                "parch": 2,
                "fare": 7.526,
                "embarked": "S"
            }
    '''
    postData = request.json
    queryData = {
        "Pclass": postData['ticketClass'],
        "Age": postData['age'],
        "Sex": postData['sex'],
        "SibSp": postData['sibsp'],
        "Parch": postData['parch'],
        "Fare": postData['fare'],
        "Embarked": postData['embarked']
    }
    try:
        prediction = getPrediction(queryData)
        return jsonify(isError=False,
                       message="Success",
                       statusCode=200,
                       prediction=prediction), 200
    except Exception as e:
        return jsonify(isError=True,
                       message=e,
                       statusCode=500), 500


@app.route('/api/v1')
def baseRoot():
    return 'Hello from base root of api.'


@app.route('/')
def serveHTML():
    return render_template('index.html')


def create_app():
    return app
