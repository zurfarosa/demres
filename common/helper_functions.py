from datetime import datetime,timedelta
from shutil import copy
from pprint import pprint
import os
import pandas as pd
from IPython.display import Markdown, display


from demres.demins.constants import Study_Design as sd
from demres.common.constants import entry_type


def printbold(string):
    display(Markdown('**' + string + '**'))

def get_prodcodes_from_drug_name(codelist):
    pegprod = pd.read_csv('dicts/proc_pegasus_prod.csv')
    prodcodes = [pegprod.loc[pegprod['drugsubstance'].str.lower()==med.lower()].loc[:,'prodcode'].tolist() for med in codelist]
    # now flatten the list (which contains lists within lists):
    prodcodes = [prodcode for list in prodcodes for prodcode in list]
    return prodcodes

def get_medcodes_from_readcodes(readcodes):
    pegmed = pd.read_csv('dicts/proc_pegasus_medical.csv')
    medcodelists = []
    for readcode in readcodes:
        medcodelists.append(pegmed.loc[pegmed['readcode'].str.contains('^'+readcode,case=True,regex=True),'medcode'].values.tolist())  #regex required because Read codes contain dot characters as wild cards.
    medcodes = [item for medcodelist in medcodelists for item in medcodelist]
    medcodes_explained = pegmed.loc[pegmed['medcode'].isin(medcodes),['readcode','medcode']].values.tolist() #Don't delete - useful for debugging, as Read code to medcode conversion can lead to surprises!
    return medcodes

def backup_file(path,file,additional_suffix=None):
    file_to_backup = os.path.join(path,file)
    backup_name = os.path.join('backup',file+'.backup_'+datetime.now().strftime('%Y%m%d'))
    if additional_suffix:
        backup_name = backup_name + additional_suffix
    copy(file_to_backup,backup_name)

def get_patient_history(all_entries,patid):
    '''
    Returns a dataframe containing all patient entries (prescriptions, consultations, immunisations etc) for a specific patient,
    annotated with read terms, drugsubstances etc.
    '''
    pegprod = pd.read_csv('dicts/proc_pegasus_prod.csv',delimiter=',')
    pegmed = pd.read_csv('dicts/proc_pegasus_medical.csv',delimiter=',')

    pt_history = all_entries[all_entries['patid']==patid]
    pt_history_elaborated = pd.merge(pt_history,pegmed[['medcode','desc']],how='left')
    pt_history_elaborated = pd.merge(pt_history_elaborated,pegprod[['prodcode','drugsubstance']],how='left')
    pt_history_elaborated['description']=pt_history_elaborated['drugsubstance'].fillna(pt_history_elaborated['desc'])
    inv_entry_type = {v: k for k, v in entry_type.items()}
    pt_history_elaborated['type']=pt_history_elaborated['type'].map(inv_entry_type)
    pt_history_elaborated = pt_history_elaborated[['patid','medcode','prodcode','eventdate','sysdate','type','description']]
    return pt_history_elaborated

def get_windows():
    '''
    Returns the list of exposure windows, as defined in Study_Design constants, going from earliest to last
    '''
    windows = []
    for window_num in range(sd.number_of_windows,0,-1): #reverse step ensures that the earliest window is first
        window = {}
        window['start']= (sd.years_between_last_window_and_index_date + (window_num * sd.window_length_in_years)) * timedelta(days=365)
        window['end'] = window['start'] - (sd.window_length_in_years * timedelta(days=365))
        windows.append(window)
    return windows

def explore_similar_drug_names(drugs,pt_features,timely_prescs):
    '''
    Looks for drugs with similar names to those in the list of drugs passed to it. So if you pass it CINNARIZINE WITH DIMENHYDRINATE,
    it may bring drugs like cinnarizine or cinnarizine with X. If they sound sensible, these drugs can then be added manually to the relevant druglist.
    '''
    # Only use prescriptions belonging to the main exposure window (not the ones used in sensitivity analysis)
    prescriptions = pd.read_hdf('data/pt_data/processed_data/hdf/prescriptions.hdf')
    prescriptions = pd.merge(prescriptions,pt_features[['patid','index_date']],how='left',on='patid')
    start_year = timedelta(days=(365*abs(sd.exposure_windows[1]['start_year'])))
    end_year = timedelta(days=(365*abs(sd.exposure_windows[1]['start_year']+sd.window_length_in_years)))
    timely_presc_mask = (prescriptions['eventdate']>=(prescriptions['index_date']-start_year)) & (prescriptions['eventdate']<=(prescriptions['index_date']-end_year))
    timely_prescs = prescriptions[timely_presc_mask]
    pegprod = pd.read_csv('dicts/proc_pegasus_prod.csv')
    timely_prescs = pd.merge(timely_prescs,pegprod[['prodcode','strength','drugsubstance']],how='left')

    drug_lists = [drug.split(' ') for drug in drugs]
    print(drug_lists)
    drug_string = '|'.join([word for list in drug_lists for word in list if word.upper() not in ['WITH','ACID','HYDRATE','TARTRATE','SODIUM','CITRATE','CARBONATE','DISODIUM','HYDROCHLORIDE','MALEATE','ACETATE']])
    print(drug_string)
    prescs = timely_prescs.loc[timely_prescs['drugsubstance'].str.contains(drug_string,na=False,case=False)]
    prescs_group = prescs['prodcode'].groupby(prescs['drugsubstance']).count().reset_index()
    prescs_group.columns=['drugsubstance','count']
    print(prescs_group)
