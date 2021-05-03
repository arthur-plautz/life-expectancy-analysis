import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

def scatter_plot(cols,df):
    col1 = df["life_expectancy"]
    plots = []
    for col in cols:
        plt.scatter(col1,df[col])
        plt.show()

def multiple_linear_regression(cols, df):
   
    x = df[cols]
    y = df["life_expectancy"]
    logit_model = sm.OLS(y, sm.add_constant(x)).fit()
    print(logit_model.summary(),"\n")
    return logit_model.params

def model_adjustment(values, features):
    counter = 0
    Y = "Y = "
    index = 0
    for values in values:
        if index == 5:
            values = '{:.8f}'.format(values)
        else:
            values = '{:.4f}'.format(values)
        if counter == 0:
            counter += 1
            Y += str(values)
        else:
            Y += " + "+str(values)+features[index]
            index +=1

    print("Model Adjusted: \n", Y)
