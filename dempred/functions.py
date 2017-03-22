import os
import sys

import pandas as pd
import numpy as np
from datetime import date, timedelta

import demres
from demres.common.constants import entry_type
from demres.common import codelists
from demres.common.process_raw_data import *
from demres.dempred.constants import Study_Design
from dempred.functions import *

def create_relevant_prescriptions_hdf():
    '''
    Creates an HDF file of all prescriptions entered during each patient's exposure period
    '''
    pt_features = pd.read_csv('data/pt_data/processed_data/pt_features_dempred.csv',delimiter=',')
    pt_features['index_date'] = pd.to_datetime(pt_features['index_date'],format='%Y-%m-%d')
    pt_features['exposure_start_date']=pt_features['index_date']-timedelta(days=(365*Study_Design.total_years_required_pre_index_date))
    pt_features['exposure_end_date']=pt_features['index_date']

    prescriptions = pd.read_hdf('hdf/prescriptions.hdf')
    merged_prescriptions = pd.merge(prescriptions,pt_features[['patid','index_date','exposure_start_date','exposure_end_date']],how='left',on='patid')
    merged_prescriptions['eventdate']=pd.to_datetime(merged_prescriptions['eventdate'],format='%Y-%m-%d')
    relev_prescriptions = merged_prescriptions[(merged_prescriptions['eventdate']>merged_prescriptions['exposure_start_date'])&(merged_prescriptions['eventdate']<merged_prescriptions['exposure_end_date'])]

    relev_prescriptions.to_hdf('hdf/relev_prescriptions.hdf','relev_prescriptions',mode='w')

def create_ppds(pt_features,drugclass,drugclass_name):
    '''
    Adds a prescribed daily dose (PDD) column for a particular drug/drug class to the pt_features dataframe
    '''
    relev_prescriptions = pd.read_hdf('hdf/relev_prescriptions.hdf')
    relev_prescriptions = relev_prescriptions[pd.notnull(relev_prescriptions['qty'])] #remove the relatively small number of prescriptions where the quantity is NaN
    prodcodes = get_prodcodes_from_drug_name(drugclass)
    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv')
    specific_prescriptions = relev_prescriptions.loc[relev_prescriptions['prodcode'].isin([prodcodes])]
    specific_prescriptions = pd.merge(specific_prescriptions,pegprod[['prodcode','substance strength','drug substance name']],how='left')
    amount_and_unit = specific_prescriptions['substance strength'].str.extract('([0-9\.]+)(\w+)',expand=True)
    amount_and_unit.columns=['amount','unit']
    amount_and_unit.amount = amount_and_unit.amount.astype('float')
    prescs = pd.concat([specific_prescriptions,amount_and_unit],axis=1).drop(['numpacks','numdays','packtype','issueseq','type'],axis=1)
    for unit,multiplier in zip(['nanogram','microgram','micrograms','gram'],[0.000001,0.001,0.001,1000]):
        unit_mask = prescs['unit']==unit
        prescs.loc[unit_mask,'amount']*=multiplier
        prescs.loc[unit_mask,'unit']='mg'
        assert set(prescs['unit'])!=1, 'There is a unit present which is not a nanogram, mg, microgram or gram'
        prescs['total_in_mg'] = prescs['qty']*prescs['amount']
    pdds = calculate_pdds(drugclass,prescs)
    presc_count = prescs.groupby(by=['patid','drug substance name']).total_in_mg.sum().reset_index()
    presc_count['pdds']=presc_count['total_in_mg']/presc_count['drug substance name'].map(lambda x: pdds[x.lower()])
    pt_pdds = presc_count.groupby(by='patid').pdds.sum().reset_index() #sum the total pdds for each patients (e.g. lorazpeam AND zopiclone AND promethazine etc.)
    pt_pdds=pt_pdds.round(decimals=2)
    pt_pdds.columns=['patid',drugclass_name+'_pdds']
    pt_features = pd.read_csv('data/pt_data/processed_data/pt_features_dempred.csv',delimiter=',')
    pt_features = pd.merge(pt_features,pt_pdds,how='left')
    return pt_features

def calculate_pdds(drugclass, prescs):
    '''
    Calculate the prescribed daily dose
    '''
    pdds = {}
    for drug in drugclass:
        relev_prescs = prescs[prescs['drug substance name'].str.contains(drug,case=False)]
        if(len(relev_prescs))>0:
            drug_amounts = list(relev_prescs['amount'])
            drug_weights = list(relev_prescs['qty'])
            pdd = np.average(drug_amounts,weights=drug_weights)
            pdds[drug.lower()]=pdd
            assert pd.notnull(pdd), 'PDD for ' + drug + 'is null'
    return pdds
