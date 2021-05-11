from data.definitions import FEATURES, TARGET
from sklearn.linear_model import LinearRegression
from statsmodels.graphics.gofplots import qqplot
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
sns.set(style="whitegrid")

def generate_scatter(x, y, info=None):
    lr = LinearRegression()
    lr.fit(x,y)
    figure, graph = plt.subplots(figsize=(20,10), dpi=100)
    graph.scatter(
        x, y,
        color='gray'
    )
    graph.plot(
        x, lr.predict(x),
        color='blue'
    )
    if info:
        graph.set_title(info['x'],  fontsize=20)
        graph.set_xlabel(info['x'], fontsize=15)
        graph.set_ylabel(info['y'], fontsize=15)
    plt.show()
    return figure

def df_single_scatters(df, show=True):
    x_set = FEATURES
    y = TARGET
    graphs = []
    for x in x_set:
        info = {
            'x': x,
            'y': y,
            'title': f'{x} scatter visualization'
        }
        graph = generate_scatter(
            df.loc[:,[x]],
            df[y],
            info
        )
        graphs.append(graph)
    if show:
        plt.show()
    else:
        return graphs

def generate_boxplots(df, show=True):
    graphs = []
    for feature in FEATURES:
        fig, ax = plt.subplots(figsize=(20,10))
        ax.boxplot(df[feature])
        ax.set_title(feature)
        graphs.append(fig)
    if show:
        plt.show()
    else:
        return graphs

def generate_hists(df, show=True):
    graphs = []
    for feature in FEATURES:
        fig, ax = plt.subplots(figsize=(20,10))
        ax.hist(df[feature])
        ax.set_title(feature)
        graphs.append(fig)
    if show:
        plt.show()
    else:
        return graphs

def generate_hist(df, col):
    df_col = df[col]
    fig, ax = plt.subplots(figsize=(20,10))
    ax.hist(df_col)
    ax.set_title(col)
    plt.show()

def eda_graphs(df, hist=True, box=True, sct=True):
    if box:
        generate_boxplots(df)
    if hist:
        generate_hists(df)
    if sct:
        df_single_scatters(df)

def generate_qqplots(model):
    print(model)
