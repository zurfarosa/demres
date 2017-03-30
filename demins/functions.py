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
from demres.common.helper_functions import *
from dempred.functions import *
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
        print(window_count)
        # Restrict insomnia event counts to those that occur during exposure window
        relevant_event_mask = (window_insom_events['eventdate']<=(window_insom_events['index_date']-window['start_latency'])) & (window_insom_events['eventdate']>=(window_insom_events['index_date']-window['end_latency']))
        window_insom_events = window_insom_events.loc[relevant_event_mask]
        window_insom_events = window_insom_events.groupby('patid')['insom_count'].count().reset_index()
        window_insom_events.columns=['patid','insom_count_window'+window_count]
    #     merge pt_features with new insomnia_event dataframe
        pt_features = pd.merge(pt_features,window_insom_events,how='left')
        pt_features['insom_count_window'+window_count].fillna(0,inplace=True)
        pt_features['insom_count_window'+window_count] = pt_features['insom_count_window'+window_count].astype(int)

    return pt_windows
