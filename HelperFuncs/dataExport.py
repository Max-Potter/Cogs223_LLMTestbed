import pandas as pd
import numpy as np
import os


def data_to_CSV(pdDataframe, filename):
    pdDataframe.to_csv(filename, encoding='utf-8', index=False)
    return

def updateDataframe(pdDataframe, newData):
    
