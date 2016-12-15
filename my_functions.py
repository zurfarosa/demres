import pandas as pd
import csv

def process_pegmed():
    pegmed = pd.read_csv('data/pegasus_medical.txt',delimiter='\t',skiprows=[0,1,2],header=None)
    pegmed.columns=['MedCode','ReadCode',2,3,4,5,'Description','Date']
    pegmed.to_csv('processed_pegmed.csv')
    return pegmed

pegmed=process_pegmed()

def lookup_one_to_one(df,lookup_col,new_col, lookupval):
    return df.loc[df[lookup_col]==lookupval][new_col].iloc[0]

def create_insomnia_medcodes():
    readcodes = pd.read_csv('insomnia_readcodes.csv',delimiter=',')
    medcodes=[str(lookup_one_to_one(pegmed,'ReadCode','MedCode',readcode)) for readcode in readcodes]
    with open('insomnia_medcodes.csv','w', newline='') as f:
        writer = csv.writer(f,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(medcodes)

def get_insomnia_medcodes():
    medcodes = pd.read_csv('insomnia_medcodes.csv',delimiter=',')
    return [int(medcode) for medcode in list(medcodes)]

def create_insomnia_clinentries():
    df = pd.read_csv('data/Extract_Clinical_001.txt',delimiter='\t')
    df['file']='001'
    df2 = pd.read_csv('data/Extract_Clinical_002.txt',delimiter='\t')
    df2['file']='002'
    df_joined = pd.concat([df,df2])
    medcodes = get_insomnia_medcodes()
    relev_clinical = df_joined[df_joined['medcode'].isin(medcodes)]
    relev_clinical.to_csv('insomnia_clinicalentries.csv',index=False)
