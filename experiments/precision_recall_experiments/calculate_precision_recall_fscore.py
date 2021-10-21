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

def handler():
    df = pd.read_csv("_PATH_TO_THE_DATASET/precision_experiment//dbpedia_test_elimination_eablock.csv", low_memory=False)
    #original = df["dbpedia"]
    original = df["dbpedia"]
    eablock = df["eablock_result"]
    match = 0
    noMatch = 0
    empty = 0
    for i in range (0,len(original)):
        if str(original[i]) == str(eablock[i]):
            match = match + 1
        elif str(eablock[i]) == "nan" or str(eablock[i]) == "" :
            empty = empty + 1
        else:
            noMatch = noMatch + 1
    f = open("_PATH_TO_THE_DATASET/precision_experiment//match_comparison_elimination.txt","w")
    precision = int(match)/(int(match)+int(noMatch))
    recall = int(match)/(len(original))
    Fscore = 2*( ( precision * recall ) / (precision + recall ) )
    f.write("match: "+str(match)+" no match: "+str(noMatch) +\
            " empty: " + str(empty) + " precision: " + str(precision) +\
            " recall: " + str(recall) + " Fscore: " + str(Fscore) )
    f.close()

if __name__ == "__main__":
        handler()