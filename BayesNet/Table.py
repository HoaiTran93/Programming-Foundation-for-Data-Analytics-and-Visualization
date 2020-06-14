import numpy as np
import sys
import pandas as pd
import os

class Table():
    def __init__(self):
        self.tableProb = None
        return None

    def get(self):
        return self.tableProb

    def toString(self):
        return self.tableProb.to_string()

    def read_data(self, file_name):
        path = "./Data/" + str(file_name)
        data = pd.read_csv(path)
        self.tableProb = pd.DataFrame(data)
        return self.tableProb

