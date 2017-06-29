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
from pprint import pprint




# 
# def create_relevant_prescriptions_hdf():
#     '''
#     Creates an HDF file of all prescriptions entered during each patient's exposure period
#     '''
#     pt_features = pd.read_csv('data/pt_data/processed_data/pt_features_dempred.csv',delimiter=',')
#     pt_features['index_date'] = pd.to_datetime(pt_features['index_date'],format='%Y-%m-%d')
#     pt_features['exposure_start_date']=pt_features['index_date']-timedelta(days=(365*Study_Design.total_years_required_pre_index_date))
#     pt_features['exposure_end_date']=pt_features['index_date']
#
#     prescriptions = pd.read_hdf('hdf/prescriptions.hdf')
#     merged_prescriptions = pd.merge(prescriptions,pt_features[['patid','index_date','exposure_start_date','exposure_end_date']],how='left',on='patid')
#     merged_prescriptions['eventdate']=pd.to_datetime(merged_prescriptions['eventdate'],format='%Y-%m-%d')
#     relev_prescriptions = merged_prescriptions[(merged_prescriptions['eventdate']>merged_prescriptions['exposure_start_date'])&(merged_prescriptions['eventdate']<merged_prescriptions['exposure_end_date'])]
#
#     relev_prescriptions.to_hdf('hdf/relev_prescriptions.hdf','relev_prescriptions',mode='w')
#
# # def add_pdds(pt_features,)

def create_pdds(pt_features,druglists):
    for druglist in druglists:
        pt_features,_,_=create_ppd(pt_features,druglist) #note that create_ppd returns a tuple
    return pt_features



def get_total_prescriptions(pt_features):
    relev_prescriptions = pd.read_hdf('hdf/relev_prescriptions.hdf')
    all_psych_drugnames = [drug for druglist in druglists.psychotropic_list_of_lists for drug in druglist['drugs']]
    prodcodes = get_prodcodes_from_drug_name(all_psych_drugnames)
    psych_mask = relev_prescriptions['prodcode'].isin(prodcodes)

    psych_prescriptions = relev_prescriptions[psych_mask]
    psych_prescriptions = psych_prescriptions.groupby(by='patid').eventdate.count().reset_index()
    psych_prescriptions.columns=['patid','psych_prescription_count']

    nonpsych_prescriptions = relev_prescriptions[~psych_mask]
    nonpsych_prescriptions = nonpsych_prescriptions.groupby(by='patid').eventdate.count().reset_index()
    nonpsych_prescriptions.columns=['patid','nonpsych_prescription_count']

    pt_features = pd.merge(pt_features,psych_prescriptions,how='left')
    pt_features = pd.merge(pt_features,nonpsych_prescriptions,how='left')

    pt_features.fillna(value=0,inplace=True)
    return pt_features
