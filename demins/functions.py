import os
import sys

import pandas as pd
import numpy as np
from datetime import date, timedelta

import demres
from demres.common.constants import entry_type
from demres.common import codelists
from demres.dempred.constants import Study_Design
from demres.common.helper_functions import *
from pprint import pprint


def get_insomnia_event_count(pt_features,entries,windows):
    """
    Calculates count of insomnia-months for each patient, and adds it to pt_features dataframe
    """
    # Create list of all insomnia entries, then group it to calculate each patient's insomnia count, broken down by month
    insomnia_medcodes = get_medcodes_from_readcodes(codelists.insomnia_readcodes)
    insom_events = entries[entries['medcode'].isin(insomnia_medcodes)]
    insom_events = insom_events[pd.notnull(insom_events['eventdate'])] #drops a small number of rows (only about 64) with NaN eventdates
    insom_events = insom_events[['patid','eventdate']].set_index('eventdate').groupby('patid').resample('M').count()
    #convert group_by object back to dataframe
    insom_events = insom_events.add_suffix('_count').reset_index()
    insom_events.columns=['patid','eventdate','insom_count']
    #delete zero counts
    insom_events = insom_events[insom_events['insom_count']>0]
    insom_events = pd.merge(insom_events,pt_features,how='inner')[['patid','eventdate','insom_count','index_date']]

    for window_count,window in enumerate(get_windows()):
        window_insom_events = insom_events
        window_count = str(window_count)
        # Restrict insomnia event counts to those that occur during exposure window
        relevant_event_mask = (window_insom_events['eventdate']>=(window_insom_events['index_date']-window['start'])) & (window_insom_events['eventdate']<=(window_insom_events['index_date']-window['end']))
        window_insom_events = window_insom_events.loc[relevant_event_mask]
        window_insom_events = window_insom_events.groupby('patid')['insom_count'].count().reset_index()
        window_insom_events.columns=['patid','insom_count_window'+window_count]
    #     merge pt_features with new insomnia_event dataframe
        pt_features = pd.merge(pt_features,window_insom_events,how='left')
        pt_features['insom_count_window'+window_count].fillna(0,inplace=True)
        pt_features['insom_count_window'+window_count] = pt_features['insom_count_window'+window_count].astype(int)

    return pt_features

def create_pdds_new(pt_features,druglists,windows):
    prescriptions = pd.read_hdf('hdf/prescriptions.hdf')
    for druglist in druglists:
        pt_features = create_ppd_new(pt_features,prescriptions,druglist,windows) #note that create_ppd returns a tuple
    return pt_features

def create_ppd_new(pt_features,prescriptions,druglist,windows):
    '''
    Adds a prescribed daily dose (PDD) column for each drug in a druglist to the pt_features dataframe
    '''
    prescs = pd.merge(prescriptions,pt_features[['patid','index_date']],how='left',on='patid')
    prescs = prescs[pd.notnull(prescs['qty'])] #remove the relatively small number of prescriptions where the quantity is NaN

    prodcodes = get_prodcodes_from_drug_name(druglist['drugs'])
    prescs = prescs.loc[prescs['prodcode'].isin([prodcodes])]

    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv')
    prescs = pd.merge(prescs,pegprod[['prodcode','substance strength','route','drug substance name']],how='left')
    # if druglist['depot']:
    for route in druglist['routes']:
        prescs = prescs.loc[prescs['route'].str.contains(route,na=False,case=False)]

    amount_and_unit = prescs['substance strength'].str.extract('([\d\.]+)([\d\.\+ \w\/]*)',expand=True)
    amount_and_unit.columns=['amount','unit']
    amount_and_unit.amount = amount_and_unit.amount.astype('float')
    prescs = pd.concat([prescs,amount_and_unit],axis=1).drop(['numpacks','numdays','packtype','issueseq','type'],axis=1)

    prescs['total_amount'] = prescs['qty']*prescs['amount']

    for window_count,window in enumerate(windows):
        window_count = str(window_count)
        window_mask = (prescs['eventdate']>=(prescs['index_date']-window['start'])) & (prescs['eventdate']<=(prescs['index_date']-window['end']))
        window_prescs = prescs[window_mask]

        pdds = {}
        for drug in druglist['drugs']:
            drug = drug.upper()
            temp_prescs = window_prescs[window_prescs['drug substance name'].str.upper()==drug]
            if(len(temp_prescs))>0:
                drug_amounts = list(temp_prescs['amount'])
                drug_weights = list(temp_prescs['qty'])
                pdd = np.average(drug_amounts,weights=drug_weights)
                pdds[drug]=pdd
                assert pd.notnull(pdd)
        presc_count = window_prescs.groupby(by=['patid','drug substance name']).total_amount.sum().reset_index()
        presc_count['pdds']=presc_count['total_amount']/presc_count['drug substance name'].map(lambda x: pdds[x.upper()])
        pt_pdds = presc_count.groupby(by='patid').pdds.sum().reset_index() #sum the total pdds for each patients (e.g. lorazpeam AND zopiclone AND promethazine etc.)
        pt_pdds=pt_pdds.round(decimals=2)
        pt_pdds.columns=['patid',druglist['name']+'_pdds_window'+window_count]
        pt_features = pd.merge(pt_features,pt_pdds,how='left')
        pt_features.fillna(value=0,inplace=True)

        with open('output/pdds/'+druglist['name']+'_PDD_start_'+str(window['start'].days)+'_end_'+str(window['end'].days), 'w') as f:
            for key, value in pdds.items():
                f.write('{0}: {1}\n'.format(key, np.round(value)))
    return pt_features

def get_consultation_count(pt_features,all_entries,windows):
    '''
    Counts the number of consultations NOT associated with insomnia (a potential counfouder) and add it to pt_features
    '''
    relev_entries = pd.merge(all_entries,pt_features[['patid','index_date']],how='inner')
    # relev_entries['index_date'] = pd.to_datetime(relev_entries['index_date'],errors='coerce',format='%Y-%m-%d')
    # Find all consultations which occur on the same day as an insomnia readcode
    insomnia_medcodes = get_medcodes_from_readcodes(codelists.insomnia_readcodes)
    insom_dates = relev_entries.loc[relev_entries['medcode'].isin(insomnia_medcodes),['eventdate','patid']]
    insom_dates['insomnia']=True
    marked_consultations = pd.merge(relev_entries,insom_dates,how='left',left_on=['eventdate','patid'],right_on=['eventdate','patid'])
    marked_consultations = marked_consultations.loc[marked_consultations['type']==entry_type['consultation']]
    marked_consultations['insomnia'] = marked_consultations['insomnia'].fillna(False)
    non_insom_cons = marked_consultations.loc[marked_consultations['insomnia']==False]
    non_insom_cons = non_insom_cons.drop('insomnia',axis=1)
    for window_count,window in enumerate(windows):
        window_count = str(window_count)
        temp_cons = non_insom_cons
        window_mask = (temp_cons['eventdate']>=(temp_cons['index_date']-window['start'])) & (temp_cons['eventdate']<=(temp_cons['index_date']-window['end']))
        temp_cons = temp_cons[window_mask]
        temp_cons = temp_cons.groupby('patid')['eventdate'].count().reset_index()
        temp_cons.columns=['patid','consultation_count_window'+window_count]
        pt_features = pd.merge(pt_features,temp_cons,how='left')
        pt_features['consultation_count_window'+window_count].fillna(0,inplace=True)
        pt_features['consultation_count_window'+window_count] = pt_features['consultation_count_window'+window_count].astype(int)
    return pt_features
