'''
@auther: Samaneh
'''
import pandas as pd
import numpy as np
import math
import csv
import re
import math
import glob
import requests

#################################################################################

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

def getCui(value):
    output = ""
    url = 'http://node1.research.tib.eu:9002/umlsmatching?type=cui'
    text = str(value).replace("_"," ")
    payload = '{"data":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        return response['cui']
    else:
        return ""

def handler():
    umlsList = []
    df = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/umls_modified_4combination.csv", low_memory=False)      
    for z in range (0,len(df)):
        umlsList.append(getCui(df["modified_label"][z]))
    umlsSeries = pd.Series(umlsList, name="eablock_result")
    result_df = pd.concat([df,umlsSeries],axis=1)
    result_df.to_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/umls_modified_4combination_eablock.csv")


if __name__ == "__main__":
        handler()