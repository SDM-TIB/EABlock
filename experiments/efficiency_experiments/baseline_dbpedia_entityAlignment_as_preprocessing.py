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

def falcon_call_db(text,mode):
    if mode=='short':
        url = 'http://node3.research.tib.eu:5005/api?mode=short'
        entities=[]
        payload = '{"text":"'+text+'"}'
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            for result in response['entities']:
                entities.append(result[0])
        else:
            r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
            if r.status_code == 200:
                response=r.json()
                for result in response['entities']:
                    entities.append(result[0])
        if len(entities) >= 1:
            output = entities[0]
        else:
            output = ""          
        return output
    elif mode=='long':
        url = 'http://node3.research.tib.eu:5005/api?mode=long'
        entities=[]
        payload = '{"text":"'+text+'"}'
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            for result in response['entities']:
                entities.append(result)
        else:
            r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
            if r.status_code == 200:
                response=r.json()
                for result in response['entities']:
                    entities.append(result)
        return entities

def handler():
    dbpediaList = []
    drug_df = pd.read_csv("/mnt/e/Experiments/BioFunMap/EABlock-data/efficiency_exp_data/dataset_2k_noORM_experiments.csv", low_memory=False)
    for j in range (0,len(drug_df)):
        dbpediaList.append(falcon_call_db(drug_df["DrugName"][j],'short'))
    dbpediaSeries = pd.Series(dbpediaList, name="dbpedia")
    classList = ["https://dbpedia.org/ontology/Disease"]*len(drug_df)
    classSeries = pd.Series(classList, name="dbpediaClass")
    result_df = pd.concat([drug_df,dbpediaSeries,classSeries],axis=1)
    result_df.to_csv("/mnt/e/Experiments/BioFunMap/EABlock-data/efficiency_exp_data/dataset_2k_noORM_experiments_processed.csv")

if __name__ == "__main__":
        handler()