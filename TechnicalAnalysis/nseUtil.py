import os
import pandas as pd


def getNSEStocksList():
    currentdir = os.path.dirname(os.path.realpath(__file__))
    nifty100filename = "\\resources\\nifty100list.csv"
    return pd.read_csv(currentdir + nifty100filename)
