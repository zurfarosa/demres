import pandas as pd
import numpy as np
from datetime import date, timedelta,datetime
from demres.common import codelists,druglists
from demres.common.process_entries import *
from common.helper_functions import *
from demres.demins.constants import Study_Design
from demres.common.logger import logging

def create_pt_features():
    '''
    Creates csv file containing all patients (cases and controls on separate rows)
    with a column for all variables to be analysed
    '''
    pt_features = pd.read_csv('data/pt_data/raw_data/Extract_Patient_001.txt', usecols=['patid','yob','gender','reggap'], delimiter='\t')
    # Remove patients with registration gaps of more than one day
    pts_with_registration_gaps = pt_features.loc[pt_features['reggap']>Study_Design.acceptable_number_of_registration_gap_days]
    pts_with_registration_gaps.to_csv('data/pt_data/removed_patients/pts_with_registration_gaps.csv',index=False)
    pt_features = pt_features.loc[pt_features['reggap']==Study_Design.acceptable_number_of_registration_gap_days]
    pt_features.drop('reggap',axis=1,inplace=True)

    pt_features['pracid']=pt_features['patid'].apply(str).str[-3:] #bizarre, but this is how the pracid works!
    pt_features['yob'] = pt_features['yob']+1800 # ditto!

    # pt_features.to_csv('data/pt_data/processed_data/pt_features.csv',index=False)
    return pt_features

def get_index_date_and_caseness_and_add_final_dementia_subtype(all_entries,pt_features):
    '''
    Calculates  index date and establishes caseness by looking for first dementia diagnoses.
    Also looks for final dementia diagnosis (e.g. 'vascular dementia'), as this is likely to be our best guess as to the dementia subtype
    '''

    pegmed = pd.read_csv('data/dicts/proc_pegasus_medical.csv',delimiter=',')
    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv',delimiter=',')
    medcodes = get_medcodes_from_readcodes(codelists.dementia_readcodes)
    prodcodes = get_prodcodes_from_drug_name(druglists.antidementia_drugs)

    # from the all_entries df, get just those which contain a dementia dx of an antidementia drug prescription
    all_dementia_entries = all_entries[(all_entries['prodcode'].isin(prodcodes))|(all_entries['medcode'].isin(medcodes))]
    # for clarity, look up the Read terms
    all_dem_labelled = pd.merge(all_dementia_entries,pegmed,how='left')[['patid','prodcode','medcode','sysdate','eventdate','type']]
    # for clarity, look up the drug names
    all_dem_labelled = pd.merge(all_dem_labelled,pegprod,how='left')[['patid','medcode','prodcode','sysdate','eventdate','type','drug substance name']]
    all_dem_labelled.loc[:,'eventdate']=pd.to_datetime(all_dem_labelled.loc[:,'eventdate'])
    #Get the date of earliest dementia diagnosis / antidementia drug prescription - this will be the revised index date, and will also determine revised caseness
    earliest_dementia_dates = all_dem_labelled.groupby('patid')['eventdate'].min().reset_index()
    earliest_dementia_dates.rename(columns={'eventdate':'index_date'},inplace=True)

    pt_features = pd.merge(pt_features,earliest_dementia_dates,how='left')
    pt_features['isCase']=np.where(pd.notnull(pt_features['index_date']),True,False)
    # Get the final dementia diagnosis
    just_dementia_diagnoses = all_dem_labelled[pd.isnull(all_dem_labelled['prodcode'])]
    final_dementia_dx = just_dementia_diagnoses.loc[just_dementia_diagnoses.groupby('patid')['eventdate'].idxmax()][['patid','medcode']]
    final_dementia_dx.rename(columns={'medcode':'final dementia medcode'},inplace=True)
    pt_features = pd.merge(pt_features,final_dementia_dx,how='left')
    return pt_features

def add_data_start_and_end_dates(all_entries,pt_features):
    '''
    Needs the dateframe created by create_medcoded_entries() to be passed to it.
    This function looks at all clinical entries (e.g. prescriptions, referrals, consultations), and looks for the first and last 'sysdated' entry.
    '''
    logging.debug('add_sys_start_and_end_dates_to_pt_features all_entries.csv')

    logging.debug('finding earliest sysdates')
    earliest_sysdates = all_entries.groupby('patid')['sysdate'].min().reset_index()
    earliest_sysdates.rename(columns={'sysdate':'data_start'},inplace=True)
    logging.debug('earliest_sysdates:\n{0}'.format(earliest_sysdates.head(5)))

    logging.debug('finding latest sysdates')
    latest_sysdates = all_entries.groupby('patid')['sysdate'].max().reset_index()
    latest_sysdates.rename(columns={'sysdate':'data_end'},inplace=True)
    logging.debug('latest_sysdates:\n{0}'.format(latest_sysdates.head(5)))

    logging.debug('merging pt_features with earliest sysdates')
    pt_features = pd.merge(pt_features,earliest_sysdates,how='left')
    logging.debug('merging pt_features with latest sysdates')
    pt_features = pd.merge(pt_features,latest_sysdates,how='left')

    # Remove pts without any sysdates
    logging.debug('removing patients without any events')
    # pd.options.mode.chained_assignment = None  # default='warn'
    pts_without_any_events = pt_features.loc[pd.isnull(pt_features['data_start'])]
    logging.debug('There are {0} patients without any events. They will now be removed.'.format(len(pts_without_any_events)))
    if len(pts_without_any_events)>0:
        pts_without_any_events.loc[:,'reason_for_removal']='Pt did not have any events'
        pts_without_any_events.to_csv('data/pt_data/removed_patients/pts_without_any_events.csv',index=False)

    logging.debug('writing all the patients with events to pt_features.csv')
    pt_features = pt_features.loc[pd.notnull(pt_features['data_start'])]
    return pt_features

# def calculate_amount_of_data_available(pt_features,isCase):
#     '''
#     Calculates the length of data available before and after the index date.
#     Requires isCase (i.e. whether pts are cases or controls) as an argument, because until they've been rematched,
#     controls don't yet have an index date.
#     '''
#     # case_mask = pt_features['isCase']==isCase
#     pt_features.loc[:,'days pre_indexdate'] = ((pt_features['index_date']-pt_features['data_start'])/np.timedelta64(1, 'D'))
#     pt_features.loc[case_mask,'days post_indexdate'] = ((pt_features['data_end']-pt_features['index_date'])/np.timedelta64(1, 'D'))
#     # pt_features.to_csv('data/pt_data/processed_data/pt_features.csv',index=False)
#     return pt_features



# def get_specific_prescription_count_then_add_to_pt_features(drugtype,column_name):
    # all_prescriptions = pd.read_csv('data/pt_data/processed_data/prescriptions.csv',delimiter=',')
    # prodcodes = get_prodcodes_from_drug_name(drugtype)
    # prescriptions = all_prescriptions[all_prescriptions['prodcode'].isin(prodcodes)][['patid','eventdate','prodcode']]
    # prescriptions['eventdate'] = pd.to_datetime(prescriptions['eventdate'],format='%Y-%m-%d',errors='coerce')
    # pt_features = pd.read_csv('data/pt_data/processed_data/pt_features.csv',delimiter=',')
    # prescriptions = pd.merge(prescriptions,pt_features, how='left')[['patid','eventdate','prodcode','index_date']]
    # prescriptions['index_date']=pd.to_datetime(prescriptions['index_date'],errors='coerce',format='%Y-%m-%d')
    # too_close_to_dx_period = timedelta(days=365)*Study_Design.years_between_end_of_exposure_period_and_index_date
    # too_distant_from_dx_period = too_close_to_dx_period + timedelta(days=365)*Study_Design.duration_of_exposure_measurement
    # not_too_close_to_dx = prescriptions['eventdate']<(prescriptions['index_date']-too_close_to_dx_period)
    # not_before_exposure_period = prescriptions['eventdate']>(prescriptions['index_date']-too_distant_from_dx_period)
    # relev_prescriptions = prescriptions[not_too_close_to_dx & not_before_exposure_period]
    # relev_prescriptions = relev_prescriptions['prodcode'].groupby(relev_prescriptions['patid']).count().reset_index()
    # relev_prescriptions.columns=['patid',column_name]
    # pt_features=pd.merge(pt_features,relev_prescriptions,how='left')
    # pt_features.to_csv('data/pt_data/processed_data/pt_features.csv',index=False)



def match_cases_and_controls(pt_features,req_yrs_post_index,req_yrs_pre_index):
    '''
    Matches cases and controls. Will not match cases to controls who do not have enough years of data
    '''
    pt_features['matchid']=np.nan
    pt_features['data_end'] = pd.to_datetime(pt_features['data_end'],errors='coerce', format='%Y-%m-%d')
    pt_features['data_start'] = pd.to_datetime(pt_features['data_start'],errors='coerce', format='%Y-%m-%d')
    pt_features['index_date'] = pd.to_datetime(pt_features['index_date'],errors='coerce', format='%Y-%m-%d')
    pt_features.loc[:,'total_available_data']= pt_features.loc[:,'data_end'] - pt_features.loc[:,'data_start']
    pt_features.sort_values(inplace=True,by='total_available_data',ascending=True) # To make matching more efficient, first try to match to controls the cases with with the LEAST amount of available data

    # print(pt_features['data_start'])
    # print(pt_features['data_end'])

    cases_mask = (pt_features['isCase']==True) & \
                (pt_features['data_start'] <= (pt_features['index_date'] - timedelta(days=(365*req_yrs_pre_index))))
    suitable_cases = pt_features[cases_mask]
    controls = pt_features.loc[pt_features['isCase']==False]
    for index,row in suitable_cases.iterrows():
        if pd.isnull(row['matchid']):
            patid = row['patid']
            yob = row['yob']
            gender = row['gender']
            pracid = row['pracid']
            index_date = row['index_date']
            # Define matching criteria
            matches_yob = controls['yob']==yob
            matches_gender = controls['gender']==gender
            matches_practice = controls['pracid']==pracid
            # is_not_already_matched = pd.isnull(controls['matchid'])
            enough_data_after_index_date = controls['data_end'] >= (index_date + timedelta(days=(365*req_yrs_post_index)))
            enough_data_before_index_date = controls['data_start'] <= (index_date - timedelta(days=(365*req_yrs_pre_index)))
            match_mask =  matches_yob & matches_gender & matches_practice & enough_data_after_index_date & enough_data_before_index_date
            if len(controls[match_mask])>0:
                best_match_index = controls.loc[match_mask,'total_available_data'].idxmin(axis=1) # To make matching more efficient, first try to match cases with those controls with the LEAST amount of available data
                best_match_id = controls.ix[best_match_index]['patid']
                logging.debug('Out of a list of {0} matching patients, patid {1} is the best match for {2}'.format(len(controls[match_mask]),best_match_id,patid))
                #give both the case and control a unique match ID (for convenience, I've used the iterrows index)
                pt_features.loc[index,'matchid']=index
                pt_features.loc[best_match_index,'matchid']=index
                pt_features.loc[best_match_index,'index_date']=index_date
                controls.drop(best_match_index,inplace=True) #drop this row from controls dataframe so it cannot be matched again
            else:
                logging.debug('No match found for {0}'.format(patid))
    pt_features.drop('total_available_data',axis=1,inplace=True)
    return pt_features

def delete_unmatched_cases_and_controls(pt_features):
    '''
    Removes all unmatched cases and controls
    '''
    removed_pts = pt_features.loc[pd.isnull(pt_features['matchid'])]
    removed_pts.loc[:,'reason_for_removal']='Unmatchable'
    removed_pts.to_csv('data/pt_data/removed_patients/removed_unmatched_patients.csv',index=False)
    pt_features = pt_features.loc[pd.notnull(pt_features['matchid'])]
    return pt_features

def delete_patients_if_not_enough_data(isCase,pt_features):
    '''
    Despite requiring user to specify whether patients are cases or controls, this only needs to be called for cases,
    as controls without enough data are removed by the match_cases_and_controls() function.
    '''
    delete_mask = (pt_features['days pre_indexdate']<(Study_Design.total_years_required_pre_index_date*365)) \
            | (pt_features['days post_indexdate']<(Study_Design.years_of_data_after_index_date_required_by_controls*365))
    delete_mask = delete_mask & (pt_features['isCase']==isCase)
    #delete cases and controls if not enough data prior to index dates
    removed_pts = pt_features.loc[delete_mask]
    removed_pts['reason_for_removal']='Not enough available data prior or post index date'
    removed_pts.to_csv('data/pt_data/removed_patients/removed_pts_with_not_enough_data.csv',mode='a',index=False)
    pt_features=pt_features.loc[delete_mask == False]
    # pt_features.to_csv('data/pt_data/processed_data/pt_features.csv',index=False)
    return pt_features
