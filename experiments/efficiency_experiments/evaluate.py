'''
@auther: Samaneh
'''
import pandas as pd
import numpy as np
import csv
import re
import math
import glob

#################################################################################

def handler():
    base_df = pd.read_csv("/mnt/e/data-EABlock/exp/baseline_sorted.csv", encoding='utf8', low_memory=False)
    bio_df = pd.read_csv("/mnt/e/data-EABlock/exp/EABlock_sorted.csv", encoding='utf8', low_memory=False)
    errorList = []
    matchList = []
    baseList = base_df["name"]
    for j in range (0,len(bio_df)):
        if str(bio_df["name"][j]) not in baseList:
            errorList.append(bio_df["name"][j])
        else:
            matchList.append(bio_df["name"][j])
    print ("match: "+str(len(matchList))+" unmatch: "+str(len(errorList)))
    f = open("/mnt/e/data-EABlock/exp/diff.txt","w")
    for i in errorList:
        f.write(i+"\n")  
    f.close()

    

if __name__ == "__main__":
        handler()
