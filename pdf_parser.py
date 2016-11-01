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

def segment_two(contents):
    relevant = []
    start = False
    for line in contents:
        if "Section 1. Contact Information" in line:
            start = True
        if "Section 2. General System Information" in line:
            start = False
        if start:
            relevant.append(line)
    return relevant

def segment_three(contents):
    relevant = []
    start = False
    for line in contents:
        if "2.1 Is this a new PIA or a modification of an existing PIA?" in line:
            start = True
        if "2.2 What is this system for?" in line:
            start = False
        if start:
            relevant.append(line)
    return relevant


def parse(df,file_name):
    tmp = {}
    with codecs.open(file_name,"r",encoding='utf-8', errors='ignore') as fdata:
        text = fdata.read()
    text = text.split("\r")

    #parsing txt section
    relevant_segment_one = segment_one(text)
    relevant_segment_two = segment_two(text)
    relevant_segment_three = segment_three(text)
    
    #adding to tmp object to store results section
    for ind,line in enumerate(relevant_segment_one):
        
        if "(Is PIA required?)" in line:
            if "Checked" in line:
                if "No" in relevant_segment_one[ind+1]:
                    tmp["Complete only Section 1 and Section 6"] = "No"
                elif "Yes" in relevant_segment_one[ind+1]:
                    tmp["Complete only Section 1 and Section 6"] = "Yes"
    
    for ind,line in enumerate(relevant_segment_two):
        if "(Date)" in line:
            tmp["Date"] = line.split("(Date)")[1].strip()
        if "(System name)" in line:
            tmp["System Name"] = line.split("(System name)")[1].strip()
        if "(Organization)" in line:
            tmp["Organization"] = line.split("(Organization)")[1].strip()
        if "(First Name)" in line:
            tmp["First Name"] = line.split("(First Name)")[1].strip()
        if "(Last Name)" in line:
            tmp["Last Name"] = line.split("(Last Name)")[1].strip()
        if "(Contact Title)" in line:
            tmp["Contact Title"] = line.split("(Contact Title)")[1].strip()
        if "(contact email)" in line:
            tmp["Contact email"] = line.split("(contact email)")[1].strip()
        if "(contact phone)" in line:
            tmp["Contact phone"] = line.split("(contact phone)")[1].strip()
        if "(contact address)" in line:
            tmp["Contact Address"] = line.split("(contact address)")[1].strip()
        if "(contact city)" in line:
            tmp["Contact City"] = line.split("(contact city)")[1].strip()
        if "(State/Territory)" in line:
            tmp["State/Territory"] = line.split("(State/Territory)")[1].strip()
        if "(contact zip)" in line:
            tmp["contact zip"] = line.split("(contact zip)")[1].strip()

    new_pia_modification_flag = False
    for ind,line in enumerate(relevant_segment_three):
        if "(New PIA or modification: New)" in line:
            if "Checked" in line:
                tmp["New PIA or modification"] = "New"
    
        if "(New PIA or modification: Modification)" in line:
            if "Checked" in line:
                tmp["New PIA or modification"] = "Modification"
                new_pia_modification_flag = True
        if not "New PIA or modification" in tmp.keys():
            tmp["New PIA or modification"] = "N/A"
        if new_pia_modification_flag:
            if "(Name of existing PIA)" in line:
                tmp["Name of existing PIA"] = line.split("(Name of existing PIA)")[1].strip()
        if "(What is the system for)" in line:
            tmp["What is the system for"] = line.split("(What is the system for)")[1].strip()
        
    df = df.append(tmp,ignore_index=True)
    return df

if __name__ == '__main__':
    df = pd.DataFrame()
    #txt_file = transform(argv[1])
    
    df = parse(df,argv[1])
    df.to_csv("results.csv")
