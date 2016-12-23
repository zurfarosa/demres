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
    raw_pegmed.columns=['medcode','readcode','clinical events','immunisation events','referral events','test events','read term','database build']
    raw_pegmed.to_csv('data/dicts/proc_pegasus_medical.csv',index=False)

def create_pegprod():
    """
    Creates a cleaned up version of Pegasus Products dictionary in csv form
    """
    raw_pegprod = pd.read_csv('data/dicts/raw_pegasus_product.txt',delimiter='\t',encoding='latin-1',header=None)
    raw_pegprod.columns=['product code','XXX code','therapy events','product name','drug substance name','substance strength','formulation','route','BNF code','BNF header','database build','unknown column']
    raw_pegprod.to_csv('data/dicts/proc_pegasus_prod.csv',index=False)


def create_insomnia_medcodes():
    """
    creates csv files containing all the insomnia medcodes, based on insomnia_readcodes.csv
    """
    pegmed = pd.read_csv('data/dicts/proc_pegasus_medical.csv')
    readcodes = pd.read_csv('data/codelists/insomnia_readcodes.csv',delimiter=',')
    medcodes=[str(lookup_one_to_one(pegmed,'readcode','medcode',readcode)) for readcode in readcodes]
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

    #delete rows where there is no control for the case
    # matching = matching[matching.]


    #Create the cases
    feature1 = matching.copy(deep=True)
    del(feature1['match'])
    del(feature1['control_birthyear'])
    del(feature1['control_pracid'])
    del(feature1['control_gender'])
    feature1['isCase']=True
    feature1.columns=['patID','pracID','gender','birthyear','case_index','matchID','data_start','data_end','isCase']

    #Create the controls
    feature2 = matching.copy(deep=True)
    del(feature2['match'])
    del(feature2['case_pracid'])
    del(feature2['case_birthyear'])
    del(feature2['case_gender'])
    feature2['isCase']=False
    cols = ['matchID',
     'case_index',
     'patID',
     'pracID',
     'gender',
     'birthyear',
     'data_start',
     'data_end',
     'isCase']
    feature2.columns=cols

    #Merge cases and controls
    features = pd.concat([feature1,feature2])
    features=features[['patID','pracID','gender','birthyear','case_index','matchID','data_start','data_end','isCase']]

    features.to_csv('data/pt_data/pt_features.csv',index=False)



# def get_insomnia_clinentries():
#     df = pd.read_csv('data/pt_data/proc_insomnia_clinicalentries.csv',delimiter='\t')
#     print(df.head(10))
