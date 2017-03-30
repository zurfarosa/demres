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
        relevant_event_mask = (window_insom_events['eventdate']<=(window_insom_events['index_date']-window['start'])) & (window_insom_events['eventdate']>=(window_insom_events['index_date']-window['end']))
        window_insom_events = window_insom_events.loc[relevant_event_mask]
        window_insom_events = window_insom_events.groupby('patid')['insom_count'].count().reset_index()
        window_insom_events.columns=['patid','insom_count_window'+window_count]
    #     merge pt_features with new insomnia_event dataframe
        pt_features = pd.merge(pt_features,window_insom_events,how='left')
        pt_features['insom_count_window'+window_count].fillna(0,inplace=True)
        pt_features['insom_count_window'+window_count] = pt_features['insom_count_window'+window_count].astype(int)

    return pt_features

def get_consultation_count(pt_features,all_entries,windows):
    '''
    Counts the number of consultations NOT associated with insomnia (a potential counfouder) and add it to pt_features
    '''
    relev_entries = pd.merge(all_entries,pt_features[['patid','index_date']],how='inner')
    #Use the index to create a unique ID for each consultation
    relev_entries.reset_index(level=0,inplace=True)
    # Find all consultations which occur on the same day as an insomnia readcode
    insomnia_medcodes = get_medcodes_from_readcodes(codelists.insomnia_readcodes)
    insom_dates = relev_entries.loc[relev_entries['medcode'].isin(insomnia_medcodes),['eventdate','patid']]
    insom_consultations = pd.merge(relev_entries,insom_dates,how='inner',left_on=['eventdate','patid'],right_on=['eventdate','patid'])
    insom_consultations = insom_consultations[insom_consultations['type']==entry_type['consultation']]
    # Now remove all these insomnia consultations
    non_insom_cons = relev_entries[~relev_entries.index.isin(insom_consultations['index'])]
    non_insom_cons[non_insom_cons['type']==entry_type['consultation']]
    # For each exposure window (e.g. 0-5 years pre-index date, 5-10 years etc), count the total non-insomnia-related consultations
    for window_count,window in enumerate(windows):
        window_count = str(window_count)
        temp_cons = non_insom_cons
        window_mask = (temp_cons['eventdate']<=(temp_cons['index_date']-window['start'])) & (temp_cons['eventdate']>=(temp_cons['index_date']-window['end']))
        temp_cons = temp_cons[window_mask]
        temp_cons = temp_cons.groupby('patid')['index'].count().reset_index()
        temp_cons.columns=['patid','consultation_count_window'+window_count]
        pt_features = pd.merge(pt_features,temp_cons,how='left')
        pt_features['consultation_count_window'+window_count].fillna(0,inplace=True)
        pt_features['consultation_count_window'+window_count] = pt_features['consultation_count_window'+window_count].astype(int)
    return pt_features
