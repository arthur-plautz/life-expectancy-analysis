from scripts.functions import *
from scripts.graphs import *

df = pd.read_csv("./data/clean/life_expectancy_analysis.csv")
df = transform_df(df)

test, train = split_data(df)

eda_graphs(
    train.df(),
    False,
    False
)

model1 = mlr_model(df)
features2 = select_features(model1)
model2 = mlr_model(df, features=features2)
