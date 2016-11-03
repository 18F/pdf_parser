from subprocess import call
from sys import argv
import pandas as pd
import codecs
from collections import OrderedDict

def transform(filename):
    call(["pdftotext","-layout",filename])
    return filename.split(".")[0] + ".txt"

def parse(df,file_name):
    tmp = OrderedDict()
    with codecs.open(file_name,"r",encoding='utf-8', errors='ignore') as fdata:
        text = fdata.read()
    text = text.split("\r")

    for ind,line in enumerate(text):
        if "check all that apply" in line.lower(): continue
        if "button" in line.lower(): continue
        if line.startswith("(") and "checked" not in line.lower() and len(line.split("(")[1].split(")")[0]) != 1:
            column_header = line.split("(")[1].split(")")[0]
            value = line.split(")")[1].strip()
            tmp[column_header.capitalize()] = value
        if line.startswith("(") and "checked" in line.lower() and ":" in line:
            column_header = line.split("(")[1].split(")")[0].split(":")[0]
            tmp[column_header.capitalize()] = "N/A"
            if "Checked" in line:
                value = line.split("(")[1].split(")")[0].split(":")[1]
                tmp[column_header.capitalize()] = value
        if line.startswith("(") and "checked" in line.lower() and ":" not in line:
            column_header = line.split("(")[1].split(")")[0]
            tmp[column_header.capitalize()] = "N/A"
            if "Checked" in line:
                value = text[ind+1].split(" ")[0]
                tmp[column_header.capitalize()] = value
                
    df = df.append(tmp,ignore_index=True)
    df = df[list(tmp.keys())] #reorders the columns
    return df

if __name__ == '__main__':
    df = pd.DataFrame()
    #txt_file = transform(argv[1])
    df = parse(df,argv[1])
    df.to_csv("results.csv")
