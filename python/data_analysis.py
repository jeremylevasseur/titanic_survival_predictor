# ========== IMPORTING THIRD PARTY LIBRARIES ==========
from pprint import pprint
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import joblib

# ========== IMPORTING CUSTOM LIBRARIES ==========
from custom_transformers import PassengerTitleAttributeAdder

# ========== DEFINING CONSTANTS ==========
trainingDataFilePath = './data/train.csv'
testingDataFilePath = './data/test.csv'
yColumnTitle = "Survived"
numericalFeatureColumnTitles = [
    "Pclass",
    "Age",
    "SibSp",
    "Parch",
    "Fare"
]
catigoricalFeatureColumnTitles = [
    "Sex",
    "Embarked",
]
analysisColumnTitles = [
    "Pclass",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Sex",
    "Embarked",
    "Name"
]

# RandomForestClassifier training parameters
# trainingParameters = [
#     {'bootstrap': [True], 'n_estimators': [3, 10, 30, 50, 100, 150],
#         'max_depth': [3, 5, 8, 12, 15, 20]},
#     {'bootstrap': [False], 'n_estimators': [3, 10, 30,
#                                             50, 100], 'max_depth': [3, 5, 8, 12, 15, 20]},
# ]

# MLP Classifier training parameters
trainingParameters = [
    {
        'hidden_layer_sizes': [(500, 400, 300, 200, 100), (400, 400, 400, 400, 400), (300, 300, 300, 300, 300), (200, 200, 200, 200, 200)],
        'activation': ['identity', 'logistic', 'tanh', 'relu'],
        'solver': ['lbfgs', 'sgd', 'adam'],
        'alpha': [0.0001, 0.001, 0.005],
        'learning_rate': ['constant', 'invscaling', 'adaptive'],
        'max_iter': [400],
        'warm_start': [True, False],
        'early_stopping': [True, False],
    }
]

crossValidationNumber = 5
modelTrainingVerbose = 1

# Importing data
trainingDataFrame = pd.read_csv(trainingDataFilePath)
testingDataFrame = pd.read_csv(testingDataFilePath)

xTrain = trainingDataFrame[analysisColumnTitles].copy()
yTrain = trainingDataFrame[yColumnTitle].copy()

xTest = testingDataFrame[analysisColumnTitles].copy()

# Cleaning data
numericalPipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="median")),
    ('std_scaler', StandardScaler()),
])

fullPipeline = ColumnTransformer([
    ("titles", PassengerTitleAttributeAdder(), ["Name"]),
    ("numerical", numericalPipeline, numericalFeatureColumnTitles),
    ("categorical", OneHotEncoder(), catigoricalFeatureColumnTitles),
])

xTrainPrepared = fullPipeline.fit_transform(xTrain)

# =============== RandomForestClassifier ===============
# gridSearch = GridSearchCV(RandomForestClassifier(), trainingParameters, cv=crossValidationNumber,
#                           scoring='neg_mean_squared_error', verbose=modelTrainingVerbose)

# =============== MLPClassifier ===============
gridSearch = GridSearchCV(MLPClassifier(), trainingParameters, cv=crossValidationNumber,
                          scoring='neg_mean_squared_error', verbose=10)

gridSearch.fit(xTrainPrepared, yTrain)

finalModel = gridSearch.best_estimator_

yTrainPredictions = finalModel.predict(xTrainPrepared)


xTestPrepared = fullPipeline.transform(xTest)
finalPredictions = finalModel.predict(xTestPrepared)
score = finalModel.score(xTrainPrepared, yTrain)
print("SCORE: %.2f %%" % (score*100))
output = pd.DataFrame({'PassengerId': testingDataFrame.PassengerId,
                      'Survived': finalPredictions})
output.to_csv('./data/submission.csv', index=False)

joblib.dump(finalModel, './models/model_3.pkl')
joblib.dump(fullPipeline, './pipelines/model_3_pipeline.pkl')
