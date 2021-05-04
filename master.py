import pandas as pd
from scripts.functions import *
from scripts.graphs import *

df = pd.read_csv("./data/clean/life_expectancy_analysis.csv")

eda_graphs(
    train.df(),
    box=False
)

outliers = get_outliers(
    df,
    {
        'violence': {'op': '>', 'value': 2},
        'inequality': {'op': '<', 'value': 0.5}
    }
)
df = remove_outliers(df, outliers)
test, train = split_data(df)

generate_scatter(train.features['violence'], train.target, 'violence')
generate_scatter(train.features['inequality'], train.target, 'inequality')
generate_hists(df[['violence','inequality']])

feature_metrics(df)
model = mlr_model(train.df())
print(model.summary())