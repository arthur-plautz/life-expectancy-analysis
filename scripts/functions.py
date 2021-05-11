from data.definitions import FEATURES, TARGET, ALPHA
from decimal import Decimal
from scripts.models import Splitted
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
import pandas as pd
import numpy as np

def mlr_model(df, features=FEATURES):
    y = df[TARGET]
    x = df[features]
    model = sm.OLS(y, sm.add_constant(x)).fit()
    return model

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

def get_outliers(df, features):
    results = {}
    for feature, factor in features.items():
        mean = df[feature].mean()
        out_value = factor['value'] * mean
        outliers = df.query(f"{feature} {factor['op']} {out_value}") 
        results[feature] = outliers.index
    return results

def remove_outliers(df, features):
    for outliers in features.values():
        df = df.drop(outliers)
    return df

def transform_log(feature):
    return np.log(feature)

def p_value_test(stats_df, a=ALPHA):
    features = stats_df.query(f'p_t < {a}')
    return features[1:]

def inference_stats(model):
    summary = model.summary()
    data = summary.tables[1].data
    stats = data[0]
    features = data[1:]
    df = pd.DataFrame(features, columns=stats)
    df['p_t'] = [float(i) for i in df['P>|t|'].values]
    df['t'] = [float(i) for i in df['t'].values]
    df = df.drop('P>|t|', axis=1)
    return p_value_test(df)

def select_features(model):
    df = inference_stats(model)
    features = df[df.columns[0]]
    return features

def transform_df(df):
    outliers = get_outliers(
        df,
        {
            'inequality': {'op': '<', 'value': 0.5},
            'air_polution': {'op': '>', 'value': 2},
        }
    )
    df = remove_outliers(df, outliers)
    df['violence'] = np.log(df['violence'])
    return df