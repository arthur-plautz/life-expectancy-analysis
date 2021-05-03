import pandas as pd
from scripts.functions import *

df = pd.read_csv("./data/clean/life_expectancy_analysis.csv")
features = [
    'rmnch_by_wealth',
    'air_polution',
    'basic_sanitation',
    'inequality',
    'mortality',
    'violence',
    'water_quality'
]

scatter_plot(features, df)
model = multiple_linear_regression(features, df)
model_adjustment(model, features)
