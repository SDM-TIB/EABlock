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

def getCui(text, mode):
    if mode=='short':
        url = 'http://node1.research.tib.eu:9002/umlsmatching?type=cui'
        payload = '{"data":"'+text+'"}'
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            return response['cui']
        else:
            return ""
    elif mode=='long':
        url = 'http://node3.research.tib.eu:5005/api_umls?mode=long&type=cui'
        payload = '{"data":"'+text+'"}'
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            output = response['entities']
        else:
            output = ""
        return output

def handler():
    umlsList = []
    drug_df = pd.read_csv("_PATH_TO_THE_DATASET_e.g._dataset_1k_1ORM_2ORM_experiments.csv", low_memory=False)
    for z in range (0,len(drug_df)):
        umlsList.append(getCui(drug_df["DrugName"][z],'short'))
    umlsSeries = pd.Series(umlsList, name="umls")
    result_df = pd.concat([drug_df,umlsSeries],axis=1)
    result_df.to_csv("_PATH_TO_THE_DATASET_e.g.dataset_1k_1ORM_2ORM_experiments_processed.csv")

if __name__ == "__main__":
        handler()