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
import statsmodels.api as sm
from pprint import pprint


def get_univariate_and_multivariate_results(pt_features,training_cols):
    #first convert booleans to 1 or 0; and do not include columns where the mean value (if continuous) is 0
    temp = []
    for col in training_cols:
        pt_features[col] = pt_features[col].astype(int)
        if pt_features[col].mean()>0.01: #arbitary number which seems to prevent 'Maximum Likelihood optimization failed to converge' warnings
            temp.append(col)
    training_cols = temp

    # get univariate results
    univariate_results = pd.DataFrame(columns=['odds_ratio','p_value'])
    for col in training_cols:
        logit = sm.Logit(pt_features['isCase'], pt_features[col])
        result = logit.fit(disp=0,maxiter=500)
        OR = round(np.exp(result.params).astype(float),4)
        p_value = round(result.pvalues.astype(float),3)
        univariate_results.loc[col] = [OR.values[0],p_value.values[0]]

    # get multivariate results
    logit = sm.Logit(pt_features['isCase'], pt_features[training_cols])
    result = logit.fit()
    multivariate_results = pd.concat([round(np.exp(result.params),4),round(result.pvalues,3)],axis=1)
    multivariate_results.columns=['odds_ratio','p_value']
    multivariate_summary = result.summary()

    return univariate_results, multivariate_results, multivariate_summary

def get_multiple_condition_statuses(pt_features,entries,windows,conditions):
    for condition in conditions:
        print(condition['name'])
        pt_features = get_condition_status(pt_features,entries,windows,condition)
    return pt_features

def get_condition_status(pt_features,entries,windows,condition):
    '''
    Searches a patient's history (i.e. the list of medcoded entries) for any one of a list of related Read codes
    (e.g. 'clinically significant alcohol use', or 'insomnia') during a given exposure window  (e.g. 5-10 years prior to index date).
    According to the 'count_or_boolean' parameter, will return either a count of the Read codes (i.e. insomnia) or a simple boolean (all other conditions).
    '''
    medcodes = get_medcodes_from_readcodes(condition['codes'])
    medcode_events = entries[entries['medcode'].isin(medcodes)]
    medcode_events = medcode_events[pd.notnull(medcode_events['eventdate'])] #drops a small number of rows  with NaN eventdates
    print('\tTotal medcode_events: {0}'.format(len(medcode_events)))
    medcode_events = pd.merge(medcode_events[['patid','eventdate']],pt_features[['patid','index_date']],how='inner',on='patid')

    if condition['use_all_pt_history']:
        windows = [{'end': timedelta(0), 'start': timedelta(36500)}]

    for window_count,window in enumerate(windows):
        if len(windows) >1:
            new_colname = condition['name']+'_window'+str(window_count)
        else:
            new_colname = condition['name']
        # Restrict event counts to those that occur during pt's exposure window
        relevant_event_mask = (medcode_events['eventdate']>=(medcode_events['index_date']-window['start'])) & (medcode_events['eventdate']<=(medcode_events['index_date']-window['end']))
        window_medcode_events = medcode_events.loc[relevant_event_mask]
        window_medcode_events = window_medcode_events.groupby('patid')['eventdate'].count().reset_index()
        window_medcode_events.columns=['patid',new_colname]
        print('\t{0} events: {1}'.format(new_colname,len(window_medcode_events)))

        #delete zero counts
        window_medcode_events = window_medcode_events[window_medcode_events[new_colname]>0]

        pt_features = pd.merge(pt_features,window_medcode_events,how='left')
        if condition['int_or_boolean']=='boolean':
            pt_features.loc[pd.notnull(pt_features[new_colname]),new_colname] = 1
            pt_features.loc[pd.isnull(pt_features[new_colname]),new_colname] = 0
        else: # e.g. insomnia_count
            pt_features[new_colname].fillna(0,inplace=True)
        pt_features[new_colname] = pt_features[new_colname].astype(int)
    return pt_features


def create_pdds(pt_features,prescriptions,list_of_druglists,windows):

    prescs = pd.merge(prescriptions,pt_features[['patid','index_date']],how='left',on='patid')
    prescs = prescs[pd.notnull(prescs['qty'])] #remove the relatively small number of prescriptions where the quantity is NaN
    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv')
    prescs = pd.merge(prescs,pegprod[['prodcode','substance strength','route','drug substance name']],how='left')

    for druglist in list_of_druglists:
        pt_features = create_pdd(pt_features,prescs,druglist,windows) #note that create_ppd returns a tuple
    return pt_features

def create_pdd(pt_features,prescriptions,druglist,windows):
    '''
    Adds a prescribed daily dose (PDD) column for each drug in a druglist to the pt_features dataframe
    '''
    prodcodes = get_prodcodes_from_drug_name(druglist['drugs'])
    prescs = prescriptions.loc[prescriptions['prodcode'].isin([prodcodes])]

    # Remove prescriptions if they are not of the route (e.g. oral) specified on the druglist
    prescs = prescs.loc[prescs['route'].str.contains(druglist['route'],na=False,case=False)]

    amount_and_unit = prescs['substance strength'].str.extract('([\d\.]+)([\d\.\+ \w\/]*)',expand=True)
    amount_and_unit.columns=['amount','unit']
    amount_and_unit.amount = amount_and_unit.amount.astype('float')


    prescs = pd.concat([prescs,amount_and_unit],axis=1).drop(['numpacks','numdays','packtype','issueseq'],axis=1)

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
    insomnia_medcodes = get_medcodes_from_readcodes(codelists.insomnia['codes'])
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
