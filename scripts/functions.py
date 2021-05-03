from data.definitions import FEATURES, TARGET
from decimal import Decimal
from scripts.models import Splitted
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def split_data(df):
    x = df[FEATURES]
    y = df[TARGET]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    return (
        Splitted('test', x_test, y_test),
        Splitted('train', x_train, y_train)
    )        

def feature_metrics(df):
    def format(value):
        return Decimal(value).quantize(Decimal('0.01'))
    corr = df.corr()
    skew = df.skew()
    kurtosis = df.kurtosis()
    for feature in FEATURES:
        desc = df[feature].describe()
        print(feature+'\n')
        for measure in ['mean', 'std', 'min', 'max']:
            value = format(desc[measure])
            print(f'{measure}: {value}')
        print(f'skew: {format(skew[feature])}')
        print(f'kurtosis: {format(kurtosis[feature])}')
        print('------------\n')

