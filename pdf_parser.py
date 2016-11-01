from subprocess import call
from sys import argv
import pandas as pd
import codecs

def transform(filename):
    call(["pdftotext","-layout",filename])
    return filename.split(".")[0] + ".txt"

def segment_one(contents):
    relevant = []
    start = False
    for line in contents:
        if "Volunteers" in line:
            start = True
        if "(New PIA or modification:" in line:
            start = False
        if start:
            relevant.append(line)
    return relevant

def parse(df,file_name):
    tmp = {}
    with codecs.open(file_name,"r",encoding='utf-8', errors='ignore') as fdata:
        text = fdata.read()
    text = text.split("\r")
    relevant_segment_one = segment_one(text)
    for ind,line in enumerate(relevant_segment_one):
        
        if "(Is PIA required?)" in line:
            if "Checked" in line:
                if "No" in relevant_segment_one[ind+1]:
                    tmp["Complete only Section 1 and Section 6"] = "No"
                elif "Yes" in relevant_segment_one[ind+1]:
                    tmp["Complete only Section 1 and Section 6"] = "Yes"
        
    df = df.append(tmp,ignore_index=True)
    return df

if __name__ == '__main__':
    df = pd.DataFrame()
    #txt_file = transform(argv[1])
    
    df = parse(df,argv[1])
    df.to_csv("results.csv")
