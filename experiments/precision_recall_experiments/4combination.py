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
import random, string

#################################################################################

def capitalize():
    #batch1 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/batch1.csv", low_memory=False) 
    #batch1 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/dbpedia/batch1.csv", low_memory=False)
    batch1 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/batch1.csv", low_memory=False)
    b1List = batch1["Label"]
    capLabelList = list(str(b1List[i]).upper() for i in range (0, len(b1List)))
    labelSeries = pd.Series(capLabelList, name="modified_label")
    result_batch1 = pd.concat([batch1,labelSeries],axis=1)
    #result_batch1.to_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/batch1_modified.csv")
    #result_batch1.to_csv("_PATH_TO_THE_DATASET/precision_experiment/dbpedia/batch1_modified.csv")
    result_batch1.to_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/batch1_modified.csv")

def randomElimination():
    #batch2 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/batch2.csv", low_memory=False)
    #batch2 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/dbpedia/batch2.csv", low_memory=False)
    batch2 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/batch2.csv", low_memory=False)
    b2List = batch2["Label"]
    eliminateList = list(str(b2List[i]).
        replace((random.choices(string.ascii_letters, k=1)[0].lower()),"",1) 
            for i in range (0, len(b2List)))
    eliminateSeries = pd.Series(eliminateList, name="modified_label")
    result_batch2 = pd.concat([batch2,eliminateSeries],axis=1)
    #result_batch2.to_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/batch2_modified.csv")
    #result_batch2.to_csv("_PATH_TO_THE_DATASET/precision_experiment/dbpedia/batch2_modified.csv")    
    result_batch2.to_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/batch2_modified.csv")

def randomReplacement():
    #batch3 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/batch3.csv", low_memory=False)
    #batch3 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/dbpedia/batch3.csv", low_memory=False)
    batch3 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/batch3.csv", low_memory=False)
    b3List = batch3["Label"]
    replaceList = list(str(b3List[i]).
        replace((random.choices(string.ascii_letters, k=1)[0].lower()),
            (random.choices(string.ascii_letters, k=1)[0].lower()),1) 
                for i in range (0, len(b3List)))
    replaceSeries = pd.Series(replaceList, name="modified_label")
    result_batch3 = pd.concat([batch3,replaceSeries],axis=1)
    #result_batch3.to_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/batch3_modified.csv")
    #result_batch3.to_csv("_PATH_TO_THE_DATASET/precision_experiment/dbpedia/batch3_modified.csv")
    result_batch3.to_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/batch3_modified.csv")

def randomInsertion():
    #batch4 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/batch4.csv", low_memory=False)
    #batch4 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/dbpedia/batch4.csv", low_memory=False)
    batch4 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/batch4.csv", low_memory=False)
    b4List = batch4["Label"]
    insertList = []
    for i in range(0, len(b4List)):
        j = int(random.choices(string.digits,k=1)[0])
        insertValue = b4List[i][:j] + random.choices(string.ascii_letters, k=1)[0].lower() + b4List[i][j:]
        insertList.append(insertValue)
    insertSeries = pd.Series(insertList, name="modified_label")
    result_batch4 = pd.concat([batch4,insertSeries],axis=1)
    #result_batch4.to_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/batch4_modified.csv")
    #result_batch4.to_csv("_PATH_TO_THE_DATASET/precision_experiment/dbpedia/batch4_modified.csv")
    result_batch4.to_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/batch4_modified.csv")

def noChnage():
    #batch5 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/batch5.csv", low_memory=False)
    #batch5 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/dbpedia/batch5.csv", low_memory=False)
    batch5 = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/batch5.csv", low_memory=False)
    b5List = batch5["Label"]
    insertSeries = pd.Series(b5List, name="modified_label")
    result_batch5 = pd.concat([batch5,insertSeries],axis=1)
    #result_batch5.to_csv("_PATH_TO_THE_DATASET/precision_experiment/umls/batch5_modified.csv")
    #result_batch5.to_csv("_PATH_TO_THE_DATASET/precision_experiment/dbpedia/batch5_modified.csv")
    result_batch5.to_csv("_PATH_TO_THE_DATASET/precision_experiment/wikidata/batch5_modified.csv")

def handler():
    capitalize()
    randomElimination()
    randomReplacement()
    randomInsertion()
    noChnage()
    ### the output of all three functions with be merge together as a dataset with the suffix of "_4combination"###

if __name__ == "__main__":
        handler()

