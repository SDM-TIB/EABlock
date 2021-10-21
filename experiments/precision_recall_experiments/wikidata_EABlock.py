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

def falcon_wikipedia_function(value):
    output = ""
    url = 'http://node3.research.tib.eu:5005/falcon2/api?mode=short'
    entities=[]
    text = str(value).replace("_"," ")
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
        return entities[0].replace('<','').replace('>','')
    else:
        return "" 

def handler():
    wikidataList = []
    df = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/wikidata_modified_4combination.csv", low_memory=False)       
    for z in range (0,len(df)):
        wikidataList.append(falcon_wikipedia_function(df["modified_label"][z]))
    wikidataSeries = pd.Series(wikidataList, name="eablock_result")
    result_df = pd.concat([df,wikidataSeries],axis=1)
    result_df.to_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/wikidata_modified_4combination_eablock.csv")

if __name__ == "__main__":
        handler()