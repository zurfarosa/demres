from datetime import datetime,timedelta
from shutil import copy
import os
import pandas as pd

from demres.demins.constants import Study_Design
from demres.common.constants import entry_type


def get_prodcodes_from_drug_name(codelist):
    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv')
    prodcodes = [pegprod.loc[pegprod['drug substance name'].str.lower()==med.lower()].loc[:,'prodcode'].tolist() for med in codelist]
    # now flatten the list (which contains lists within lists):
    prodcodes = [prodcode for list in prodcodes for prodcode in list]
    return prodcodes

def get_medcodes_from_readcodes(readcodes):
    pegmed = pd.read_csv('data/dicts/proc_pegasus_medical.csv')
    medcodes=[pegmed.loc[pegmed['readcode']==readcode,'medcode'].iloc[0] for readcode in readcodes]
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
    annotated with read terms, drug substance names etc.
    '''
    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv',delimiter=',')
    pegmed = pd.read_csv('data/dicts/proc_pegasus_medical.csv',delimiter=',')
    pt_history = all_entries[all_entries['patid']==patid]
    pt_history_elaborated = pd.merge(pt_history,pegmed[['medcode','read term']],how='left')
    pt_history_elaborated = pd.merge(pt_history_elaborated,pegprod[['prodcode','drug substance name']],how='left')
    pt_history_elaborated['description']=pt_history_elaborated['drug substance name'].fillna(pt_history_elaborated['read term'])
    inv_entry_type = {v: k for k, v in entry_type.items()}
    pt_history_elaborated['type']=pt_history_elaborated['type'].map(inv_entry_type)
    pt_history_elaborated = pt_history_elaborated[['patid','eventdate','sysdate','type','description']]
    return pt_history_elaborated


def get_windows():
    '''
    Returns the list of exposure windows, as defined in Study_Design constants, going from earliest to last
    '''
    windows = []
    for window_num in range(Study_Design.number_of_windows-1,-1,-1): #reverse step ensures that the earliest window is first
        window = {}
        window['start']= (Study_Design.years_between_last_window_and_index_date + (window_num * Study_Design.window_length_in_years)) * timedelta(days=365)
        window['end'] = window['start'] + (Study_Design.window_length_in_years * timedelta(days=365))
        windows.append(window)
    return windows
