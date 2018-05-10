import pandas as pd
import numpy as np
from datetime import date, timedelta,datetime
from demres.common.constants import entry_type
from demres.common import codelists,druglists
from demres.common.process_pt_features import *
from demres.demins.constants import Study_Design
from demres.common.logger import logging



def create_pegmed():
    """
    Creates a cleaned up version of Pegasus Medical dictionary in csv form
    """
    pegmed = pd.read_csv('dicts/medical.txt',delimiter='\t',skiprows=[1])
    pegmed.to_csv('dicts/proc_pegasus_medical.csv',index=False)

def create_pegprod():
    """
    Creates a cleaned up version of Pegasus Products dictionary in csv form
    """
    pegprod = pd.read_csv('dicts/product.txt',delimiter='\t',skiprows=[1,2],encoding='latin-1', header=0)

    pegprod.to_csv('dicts/proc_pegasus_prod.csv',index=False)

def create_specific_prescriptions(all_prescriptions,medlist,csv_name):
    #First get the drug product info from Pegasus
    pegprod = pd.read_csv('dicts/proc_pegasus_prod.csv', delimiter=',')
    pegprod['drugsubstance'].fillna('',inplace=True)
    specific_pegprod = pegprod[pegprod['drugsubstance'].str.contains('|'.join(medlist), case=False)]
    specific_pegprod=specific_pegprod[['prodcode', 'productname','drugsubstance','strength', 'formulation','route']]

    #Select only relevant drugs from the list of all our sample's prescriptions
    relevant_prescriptions=all_prescriptions[all_prescriptions['prodcode'].isin(specific_pegprod['prodcode'])]

    #Now merge the relevant prescriptions with the Pegasus drug product info
    all_info = pd.merge(relevant_prescriptions,specific_pegprod,how='inner')
    all_info.to_csv('data/medlists/'+csv_name,index=False)

def create_prescriptions():
    logging.debug(entry_type['prescription'])
    # logging.debug('reading presc1')
    presc1 = pd.read_csv('data/pt_data/raw_data/Extract_Therapy_001.txt',delimiter='\t')
    # logging.debug('reading presc2')
    presc2 = pd.read_csv('data/pt_data/raw_data/Extract_Therapy_002.txt',delimiter='\t')
    # logging.debug('concatenating')
    prescriptions = pd.concat([presc1,presc2])
    # logging.debug('converting eventdate to datetime')
    prescriptions['eventdate'] = pd.to_datetime(prescriptions['eventdate'],format='%d/%m/%Y',errors='coerce')
    # logging.debug('converting sysdate to datetime')
    prescriptions['sysdate'] = pd.to_datetime(prescriptions['sysdate'],format='%d/%m/%Y',errors='coerce')
    # logging.debug('writing to csv')
    prescriptions.to_hdf('data/pt_data/processed_data/hdf/prescriptions.hdf','prescriptions',mode='w')

def create_clinicals():
    #logging.debug('processing clinical - reading clin1')
    clin1 = pd.read_csv('data/pt_data/raw_data/Extract_Clinical_001.txt',delimiter='\t')
    #logging.debug('processing clinical - reading clin2')
    clin2 = pd.read_csv('data/pt_data/raw_data/Extract_Clinical_002.txt',delimiter='\t')
    #logging.debug('processing clinical - concatenating')
    clinicals = pd.concat([clin1,clin2])
    #logging.debug('processing clinical - converting to datetime - eventdate')
    clinicals['eventdate'] = pd.to_datetime(clinicals['eventdate'],format='%d/%m/%Y',errors='coerce')
    #logging.debug('processing clinical - converting to datetime - sysdate')
    clinicals['sysdate'] = pd.to_datetime(clinicals['sysdate'],format='%d/%m/%Y',errors='coerce')
    clinicals.to_hdf('data/pt_data/processed_data/hdf/clinicals.hdf','clinicals',mode='w')

def create_tests():
    #logging.debug('processing tests')
    test1 = pd.read_csv('data/pt_data/raw_data/Extract_Test_001.txt',delimiter='\t')
    test2 = pd.read_csv('data/pt_data/raw_data/Extract_Test_002.txt',delimiter='\t')
    #logging.debug('processing test - concatenating')
    tests = pd.concat([test1,test2])
    #logging.debug('processing test - converting to datetime - eventdate')
    tests['eventdate'] = pd.to_datetime(tests['eventdate'],format='%d/%m/%Y',errors='coerce')
    #logging.debug('processing test - converting to datetime - sysdate')
    tests['sysdate'] = pd.to_datetime(tests['sysdate'],format='%d/%m/%Y',errors='coerce')
    tests.to_hdf('data/pt_data/processed_data/hdf/tests.hdf','tests',mode='w')

def create_referrals():
    #logging.debug('processing referrals')
    referrals = pd.read_csv('data/pt_data/raw_data/Extract_Referral_001.txt',delimiter='\t')
    #logging.debug('processing referrals - converting to datetime - eventdate')
    referrals['eventdate'] = pd.to_datetime(referrals['eventdate'],format='%d/%m/%Y',errors='coerce')
    #logging.debug('processing referrals - converting to datetime - sysdate')
    referrals['sysdate'] = pd.to_datetime(referrals['sysdate'],format='%d/%m/%Y',errors='coerce')
    referrals.to_hdf('data/pt_data/processed_data/hdf/referrals.hdf','referrals',mode='w')

def create_consultations():
    """
    Creates a csv file containing all the data from Extract_Consultation_001.txt and Extract_Consultation_002.txt
    """
    #logging.debug('reading Extract_Consultation_001.txt')
    cons1 = pd.read_csv('data/pt_data/raw_data/Extract_Consultation_001.txt',delimiter='\t')
    #logging.debug('reading Extract_Consultation_002.txt')
    cons2 = pd.read_csv('data/pt_data/raw_data/Extract_Consultation_002.txt',delimiter='\t')
    #logging.debug('concatenating')
    consultations = pd.concat([cons1,cons2])
    #logging.debug('converting to datetime - eventdate')
    consultations['eventdate'] = pd.to_datetime(consultations['eventdate'],format='%d/%m/%Y',errors='coerce')
    #logging.debug('converting to datetime - sysdate')
    consultations['sysdate'] = pd.to_datetime(consultations['sysdate'],format='%d/%m/%Y',errors='coerce')
    #logging.debug('adding type column')
    #logging.debug('writing to csv')
    consultations.to_hdf('data/pt_data/processed_data/hdf/consultations.hdf','consultations',mode ='w')

def create_immunisations():
    #logging.debug('processing immunisations')
    immunisations = pd.read_csv('data/pt_data/raw_data/Extract_Immunisation_001.txt',delimiter='\t')
    #logging.debug('processing immunisations - converting to datetime - eventdate')
    immunisations['eventdate'] = pd.to_datetime(immunisations['eventdate'],format='%d/%m/%Y',errors='coerce')
    #logging.debug('processing  immunisations - converting to datetime - sysdate')
    immunisations['sysdate'] = pd.to_datetime(immunisations['sysdate'],format='%d/%m/%Y',errors='coerce')
    immunisations.to_hdf('data/pt_data/processed_data/hdf/immunisations.hdf','immunisations',mode='w')

def create_medcoded_entries():
    #logging.debug('calling create_medcoded_entries')
    """
    Creates simplified hdf file.
    This is a file containing a dataframe containing simplified data
    (just patient ID, eventdate, sysdate, and medcode) from the
    Extract_Clinical_001 and 002 files, Extract_Test_001 and 002 file and Extract_Referral_001 file
    (but not the Extract_Therapy_001 or 002 files or Extract_Consultations_001 or 002)
    """
    clinicals = pd.read_hdf('data/pt_data/processed_data/hdf/clinicals.hdf')[['patid','sysdate','eventdate','medcode']]
    clinicals['type']=entry_type['clinical']

    tests = pd.read_hdf('data/pt_data/processed_data/hdf/tests.hdf')[['patid','sysdate','eventdate','medcode']]
    tests['type']=entry_type['test']

    referrals = pd.read_hdf('data/pt_data/processed_data/hdf/referrals.hdf')[['patid','sysdate','eventdate','medcode']]
    referrals['type']=entry_type['referral']

    immunisations = pd.read_hdf('data/pt_data/processed_data/hdf/immunisations.hdf')[['patid','sysdate','eventdate','medcode']]
    immunisations['type']=entry_type['immunisation']

    medcoded_entries = pd.concat([clinicals,tests,referrals,immunisations],ignore_index=True)
    medcoded_entries.to_hdf('data/pt_data/processed_data/hdf/medcoded_entries.hdf','medcoded_entries',mode='w')

def get_all_encounters():
    medcoded_entries = pd.read_hdf('data/pt_data/processed_data/hdf/medcoded_entries.hdf')
    medcoded_entries['prodcode']=np.nan

    # prescriptions = pd.read_hdf('data/pt_data/processed_data/hdf/prescriptions.hdf')
    # prescriptions = prescriptions.loc[:,['patid','sysdate','eventdate','prodcode']]
    # prescriptions['medcode']=np.nan
    # prescriptions['type']=entry_type['prescription']

    consultations = pd.read_hdf('data/pt_data/processed_data/hdf/consultations.hdf')[['patid','sysdate','eventdate']]
    consultations['medcode']=np.nan
    consultations['prodcode']=np.nan
    consultations['type']=entry_type['consultation']

    # all_entries = pd.concat([consultations,prescriptions,medcoded_entries],ignore_index=True)
    all_encounters = pd.concat([consultations,medcoded_entries],ignore_index=True)
    return all_encounters

def get_all_entries(all_encounters):

    prescriptions = pd.read_hdf('data/pt_data/processed_data/hdf/prescriptions.hdf')
    prescriptions = prescriptions.loc[:,['patid','sysdate','eventdate','prodcode']]
    prescriptions['medcode']=np.nan
    prescriptions['type']=entry_type['prescription']

    all_entries = pd.concat([all_encounters,prescriptions],ignore_index=True)
    return all_entries
