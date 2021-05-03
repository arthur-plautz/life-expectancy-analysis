import pandas as pd
from scripts.functions import *
from scripts.graphs import *

df = pd.read_csv("./data/clean/life_expectancy_analysis.csv")
test, train = split_data(df)

eda_graphs(
    train.df()
)