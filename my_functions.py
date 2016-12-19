import pandas as pd
import csv


"""HELPER FUNCTIONS"""
def lookup_one_to_one(df,lookup_col,new_col, lookupval):
    return df.loc[df[lookup_col]==lookupval][new_col].iloc[0]


def create_pegmed():
    """
    Creates a cleaned up version of Pegasus Medical dictionary in csv form
    """
    raw_pegmed = pd.read_csv('data/dicts/raw_pegasus_medical.txt',delimiter='\t',skiprows=[0,1,2],header=None)
    raw_pegmed.columns=['MedCode','ReadCode','col2','col3','col4','col5','Description','Date']
    raw_pegmed.to_csv('data/dicts/proc_pegasus_medical.csv')

def create_insomnia_medcodes():
    """
    creates csv files containing all the insomnia medcodes, based on insomnia_readcodes.csv
    """
    pegmed = pd.read_csv('data/dicts/proc_pegasus_medical.csv')
    readcodes = pd.read_csv('data/codelists/insomnia_readcodes.csv',delimiter=',')
    medcodes=[str(lookup_one_to_one(pegmed,'ReadCode','MedCode',readcode)) for readcode in readcodes]
    with open('data/codelists/insomnia_medcodes.csv','w', newline='') as f:
        writer = csv.writer(f,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(medcodes)

def get_insomnia_medcodes():
    medcodes = pd.read_csv('data/codelists/insomnia_medcodes.csv',delimiter=',')
    return [int(medcode) for medcode in list(medcodes)]

def create_insomnia_clinentries():
    """
    Creates csv file containing all Clinical Entries relating to our insomnia medcodes
    """
    df = pd.read_csv('data/pt_data/Extract_Clinical_001.txt',delimiter='\t')
    df['file']='001'
    df2 = pd.read_csv('data/pt_data/Extract_Clinical_002.txt',delimiter='\t')
    df2['file']='002'
    df_joined = pd.concat([df,df2])
    medcodes = get_insomnia_medcodes()
    relev_clinical = df_joined[df_joined['medcode'].isin(medcodes)]
    relev_clinical.to_csv('data/pt_data/proc_insomnia_clinicalentries.csv',index=False)

def create_pt_features():
    '''
    Creates csv file containing all patients (cases and controls on separate
    rows) with a column for all variables for logistic regression
    '''
    matching = pd.read_csv('data/pt_data/Matching_File.txt',delimiter='\t')
    feature_index=['patID','pracID','gender','birthyear','isCase','matchid','case_index','data_start','data_end']
    features = pd.DataFrame(columns=feature_index)
    for index,row in matching.iterrows():
        # first append the case
        index = len(features)
        features.loc[index,feature_index[0]]=row[0] #patID
        features.loc[index,feature_index[1]]=row[1] #pracID
        features.loc[index,feature_index[2]]=row[2] #gender
        features.loc[index,feature_index[3]]=row[3] #birthyear
        features.loc[index,feature_index[4]]=True #isCase
        features.loc[index,feature_index[5]]=row[6] #matchid
        features.loc[index,feature_index[6]]=row[4] #case_index
        features.loc[index,feature_index[7]]=row[10] #data_start
        features.loc[index,feature_index[8]]=row[11] #data_end
        # now append the control
        index = len(features)
        features.loc[index,feature_index[0]]=row[6] #patID
        features.loc[index,feature_index[1]]=row[7] #pracID
        features.loc[index,feature_index[2]]=row[8] #gender
        features.loc[index,feature_index[3]]=row[9] #birthyear
        features.loc[index,feature_index[4]]=False #isCase
        features.loc[index,feature_index[5]]=row[0] #matchid
        features.loc[index,feature_index[6]]=row[4] #case_index
        features.loc[index,feature_index[7]]=row[10] #data_start
        features.loc[index,feature_index[8]]=row[11] #data_end
        features.to_csv(data/pt_data/pt_features.csv)

# def get_insomnia_clinentries():
#     df = pd.read_csv('data/pt_data/proc_insomnia_clinicalentries.csv',delimiter='\t')
#     print(df.head(10))
