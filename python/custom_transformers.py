from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import pandas as pd
import numpy as np


def determineTitle(name):
    title = name.split(',')[1].split('.')[0].strip()
    return title


class PassengerTitleAttributeAdder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        columnTitles = X.columns.to_list()
        columnTitles.append('Title')
        columnTitles.remove('Name')
        newColumnTitles = {k: v for k, v in zip(
            range(len(columnTitles)), columnTitles)}
        titleColumnSeries = X.apply(
            lambda row: determineTitle(row['Name']), axis=1)
        ordinalEncoder = OrdinalEncoder()
        encodedTitleColumn = ordinalEncoder.fit_transform(
            pd.DataFrame({'Title': titleColumnSeries})).flatten()
        encodedTitleColumnSeries = pd.Series(encodedTitleColumn)
        combinedDataFrame = pd.DataFrame(
            np.c_[X.drop('Name', axis=1), encodedTitleColumnSeries]).rename(columns=newColumnTitles)
        return combinedDataFrame
