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

def falcon_call_wikidata(text,mode):
    if mode=='short':
        url = 'http://node3.research.tib.eu:5005/falcon2/api?mode=short'
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
                for result in response['entities_wikidata']:
                    entities.append(result[0])
        if len(entities) >= 1:
            output = entities[0].replace('<','').replace('>','')
        else:
            output = ""           
        return output
    elif mode=='long':
        url = 'http://node3.research.tib.eu:5005/falcon2/api?mode=long'
        entities=[]
        payload = '{"text":"'+text+'"}'
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            for result in response['entities_wikidata']:
                entities.append([result[0].replace('<','').replace('>',''),result[1]])
        else:
            r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
            if r.status_code == 200:
                response=r.json()
                for result in response['entities_wikidata']:
                    entities.append([result[0].replace('<','').replace('>',''),result[1]])
        return entities

def handler():
    wikidataList = []
    drug_df = pd.read_csv("/mnt/e/Experiments/BioFunMap/EABlock-data/efficiency_exp_data/dataset_2k_noORM_experiments.csv", low_memory=False)
    for i in range (0,len(drug_df)):
        wikidataList.append(falcon_call_wikidata(drug_df["DrugName"][i],'short'))
    wikidataSeries = pd.Series(wikidataList, name="wikidata")
    classList = ["https://www.wikidata.org/wiki/Q11173"]*len(drug_df)
    classSeries = pd.Series(classList, name="wikidataClass")
    result_df = pd.concat([drug_df,wikidataSeries,classSeries],axis=1)
    result_df.to_csv("/mnt/e/Experiments/BioFunMap/EABlock-data/efficiency_exp_data/dataset_2k_noORM_experiments_processed.csv")

if __name__ == "__main__":
        handler()