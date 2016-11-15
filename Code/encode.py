import json
import os
import pandas as pd


def encode_json(data, filename):
    jsondata = data.reset_index().to_json(orient='records')
    os.getcwd()
    with open(os.path.realpath('Display/' + str(filename)), 'w') as outfile:
        outfile.write(jsondata)
        outfile.close() 
