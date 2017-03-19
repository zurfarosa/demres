import pandas as pd
import numpy as np
from datetime import date, timedelta,datetime
from demres.definitions import ROOT_DIR
from demres.common.constants import entry_type
from demres.common import codelists
from demres.common.process_raw_data import *
from demres.demins.constants import Study_Design
from demres.common.logger import logging

def get_patient_history(all_entries,patid):
    '''
    Returns a dataframe containing all patient entries (prescriptions, consultations, immunisations etc) for a specific patient,
    annotated with read terms, drug substance names etc.
    '''
    pegprod = pd.read_csv(ROOT_DIR + '/data/dicts/proc_pegasus_prod.csv',delimiter=',')
    pegmed = pd.read_csv(ROOT_DIR + '/data/dicts/proc_pegasus_medical.csv',delimiter=',')
    pt_history = all_entries[all_entries['patid']==patid]
    pt_history_elaborated = pd.merge(pt_history,pegmed[['medcode','read term']],how='left')
    pt_history_elaborated = pd.merge(pt_history_elaborated,pegprod[['prodcode','drug substance name']],how='left')
    pt_history_elaborated['description']=pt_history_elaborated['drug substance name'].fillna(pt_history_elaborated['read term'])
    inv_entry_type = {v: k for k, v in entry_type.items()}
    pt_history_elaborated['type']=pt_history_elaborated['type'].map(inv_entry_type)
    pt_history_elaborated = pt_history_elaborated[['patid','eventdate','sysdate','type','description']]
    return pt_history_elaborated

def create_pt_features():
    '''
    Creates csv file containing all patients (cases and controls on separate rows)
    with a column for all variables to be analysed
    '''
    pt_features = pd.read_csv(ROOT_DIR + '/data/pt_data/raw_data/Extract_Patient_001.txt', usecols=['patid','yob','gender','reggap'], delimiter='\t')
    # Remove patients with registration gaps of more than one day
    pts_with_registration_gaps = pt_features.loc[pt_features['reggap']>Study_Design.acceptable_number_of_registration_gap_days]
    pts_with_registration_gaps.to_csv(ROOT_DIR + '/data/pt_data/removed_patients/pts_with_registration_gaps.csv',index=False)
    pt_features = pt_features.loc[pt_features['reggap']==Study_Design.acceptable_number_of_registration_gap_days]
    pt_features.drop('reggap',axis=1,inplace=True)

    pt_features['pracid']=pt_features['patid'].apply(str).str[-3:] #bizarre, but this is how the pracid works!
    pt_features['yob'] = pt_features['yob']+1800 # ditto!

    # pt_features.to_csv(ROOT_DIR + '/data/pt_data/processed_data/pt_features.csv',index=False)
    return pt_features

def get_index_date_and_caseness_and_add_final_dementia_subtype(all_entries,pt_features):
    '''
    Calculates  index date and establishes caseness by looking for first dementia diagnoses.
    Also looks for final dementia diagnosis (e.g. 'vascular dementia'), as this is likely to be our best guess as to the dementia subtype
    '''

    pegmed = pd.read_csv(ROOT_DIR + '/data/dicts/proc_pegasus_medical.csv',delimiter=',')
    pegprod = pd.read_csv(ROOT_DIR + '/data/dicts/proc_pegasus_prod.csv',delimiter=',')
    medcodes = get_medcodes_from_readcodes(codelists.dementia_readcodes)
    prodcodes = get_prodcodes_from_drug_name(codelists.antidementia_drugs)

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
    # pt_features.to_csv(ROOT_DIR + '/data/pt_data/processed_data/pt_features.csv',index=False)
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
    pd.options.mode.chained_assignment = None  # default='warn'
    pts_without_any_events = pt_features.loc[pd.isnull(pt_features['data_start'])]
    pts_without_any_events.loc[:,'reason_for_removal']='Pt did not have any events'
    pts_without_any_events.to_csv(ROOT_DIR + '/data/pt_data/removed_patients/pts_without_any_events.csv',index=False)

    logging.debug('writing all the patients with events to pt_features.csv')
    pt_features = pt_features.loc[pd.notnull(pt_features['data_start'])]
    pt_features.to_csv(ROOT_DIR + '/data/pt_data/processed_data/pt_features.csv',index=False)
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
#     # pt_features.to_csv(ROOT_DIR + '/data/pt_data/processed_data/pt_features.csv',index=False)
#     return pt_features

def get_prodcodes_from_drug_name(codelist):
    pegprod = pd.read_csv(ROOT_DIR + '/data/dicts/proc_pegasus_prod.csv')
    prodcodes = [pegprod.loc[pegprod['drug substance name'].str.contains(med,na=False,case=False)].loc[:,'prodcode'].tolist() for med in codelist]
    # now flatten the list (which contains lists within lists):
    prodcodes = [prodcode for list in prodcodes for prodcode in list]
    return prodcodes

def get_specific_prescription_count_then_add_to_pt_features(drugtype,column_name):
    all_prescriptions = pd.read_csv(ROOT_DIR + '/data/pt_data/processed_data/prescriptions.csv',delimiter=',')
    prodcodes = get_prodcodes_from_drug_name(drugtype)
    prescriptions = all_prescriptions[all_prescriptions['prodcode'].isin(prodcodes)][['patid','eventdate','prodcode']]
    prescriptions['eventdate'] = pd.to_datetime(prescriptions['eventdate'],format='%Y-%m-%d',errors='coerce')
    pt_features = pd.read_csv(ROOT_DIR + '/data/pt_data/processed_data/pt_features.csv',delimiter=',')
    prescriptions = pd.merge(prescriptions,pt_features, how='left')[['patid','eventdate','prodcode','index_date']]
    prescriptions['index_date']=pd.to_datetime(prescriptions['index_date'],errors='coerce',format='%Y-%m-%d')
    too_close_to_dx_period = timedelta(days=365)*Study_Design.years_between_end_of_exposure_period_and_index_date
    too_distant_from_dx_period = too_close_to_dx_period + timedelta(days=365)*Study_Design.duration_of_exposure_measurement
    not_too_close_to_dx = prescriptions['eventdate']<(prescriptions['index_date']-too_close_to_dx_period)
    not_before_exposure_period = prescriptions['eventdate']>(prescriptions['index_date']-too_distant_from_dx_period)
    relev_prescriptions = prescriptions[not_too_close_to_dx & not_before_exposure_period]
    relev_prescriptions = relev_prescriptions['prodcode'].groupby(relev_prescriptions['patid']).count().reset_index()
    relev_prescriptions.columns=['patid',column_name]
    pt_features=pd.merge(pt_features,relev_prescriptions,how='left')
    pt_features.to_csv(ROOT_DIR + '/data/pt_data/processed_data/pt_features.csv',index=False)

def get_medcodes_from_readcodes(readcodes):
    pegmed = pd.read_csv(ROOT_DIR + '/data/dicts/proc_pegasus_medical.csv')
    medcodes=[pegmed.loc[pegmed['readcode']==readcode,'medcode'].iloc[0] for readcode in readcodes]
    return medcodes

def match_cases_and_controls(pt_features,years_post_index,years_pre_index):
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
                (pt_features['data_start'] <= (pt_features['index_date'] - timedelta(days=(365*years_pre_index))))
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
            is_not_already_matched = pd.isnull(controls['matchid'])
            enough_data_after_index_date = controls['data_end'] >= (index_date + timedelta(days=(365*years_post_index)))
            enough_data_before_index_date = controls['data_start'] <= (index_date - timedelta(days=(365*years_pre_index)))
            match_mask =  matches_yob & matches_gender & matches_practice & is_not_already_matched & enough_data_after_index_date & enough_data_before_index_date
            if len(controls[match_mask])>0:
                best_match_index = controls.loc[match_mask,'total_available_data'].idxmin(axis=1) # To make matching more efficient, first try to match cases with those controls with the LEAST amount of available data
                best_match_id = controls.ix[best_match_index]['patid']
                logging.debug('Out of a list of {0} matching patients, patid {1} is the best match for {2}'.format(len(controls[match_mask]),best_match_id,patid))
                #give both the case and control a unique match ID (for convenience, I've used the iterrows index)
                pt_features.loc[index,'matchid']=index
                pt_features.loc[best_match_index,'matchid']=index
                pt_features.loc[best_match_index,'index_date']=index_date
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
    removed_pts.to_csv(ROOT_DIR + '/data/pt_data/removed_patients/removed_unmatched_patients.csv',index=False)
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
    removed_pts.to_csv(ROOT_DIR + '/data/pt_data/removed_patients/removed_pts_with_not_enough_data.csv',mode='a',index=False)
    pt_features=pt_features.loc[delete_mask == False]
    # pt_features.to_csv(ROOT_DIR + '/data/pt_data/processed_data/pt_features.csv',index=False)
    return pt_features

def create_pegmed():
    """
    Creates a cleaned up version of Pegasus Medical dictionary in csv form
    """
    pegmed = pd.read_csv(ROOT_DIR + '/data/dicts/raw_pegasus_medical.txt',delimiter='\t',skiprows=[0,1,2],header=None)
    pegmed.columns=['medcode','readcode','clinical events','immunisation events','referral events','test events','read term','database build']
    pegmed.to_csv(ROOT_DIR + '/data/dicts/proc_pegasus_medical.csv',index=False)

def create_pegprod():
    """
    Creates a cleaned up version of Pegasus Products dictionary in csv form
    """
    pegprod = pd.read_csv(ROOT_DIR + '/data/dicts/raw_pegasus_product.txt',delimiter='\t',encoding='latin-1', skiprows=[0,1],header=None)
    pegprod.columns=['prodcode','XXX code','therapy events','product name','drug substance name','substance strength','formulation','route','BNF code','BNF header','database build','unknown column']
    pegprod.to_csv(ROOT_DIR + '/data/dicts/proc_pegasus_prod.csv',index=False)

def create_specific_prescriptions(all_prescriptions,medlist,csv_name):
    #First get the drug product info from Pegasus
    pegprod = pd.read_csv(ROOT_DIR + '/data/dicts/proc_pegasus_prod.csv', delimiter=',')
    pegprod['drug substance name'].fillna('',inplace=True)
    specific_pegprod = pegprod[pegprod['drug substance name'].str.contains('|'.join(medlist), case=False)]
    specific_pegprod=specific_pegprod[['prodcode', 'product name','drug substance name','substance strength', 'formulation','route']]

    #Select only relevant drugs from the list of all our sample's prescriptions
    relevant_prescriptions=all_prescriptions[all_prescriptions['prodcode'].isin(specific_pegprod['prodcode'])]

    #Now merge the relevant prescriptions with the Pegasus drug product info
    all_info = pd.merge(relevant_prescriptions,specific_pegprod,how='inner')
    all_info.to_csv(ROOT_DIR + '/data/medlists/'+csv_name,index=False)

def create_prescriptions():
    logging.debug(entry_type['prescription'])
    logging.debug('reading presc1')
    presc1 = pd.read_csv(ROOT_DIR + '/data/pt_data/raw_data/Extract_Therapy_001.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','prodcode','qty','ndd','numdays','numpacks','packtype','issueseq'])
    logging.debug('reading presc2')
    presc2 = pd.read_csv(ROOT_DIR + '/data/pt_data/raw_data/Extract_Therapy_002.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','prodcode','qty','ndd','numdays','numpacks','packtype','issueseq'])
    logging.debug('concatenating')
    prescriptions = pd.concat([presc1,presc2])
    logging.debug('converting eventdate to datetime')
    prescriptions['eventdate'] = pd.to_datetime(prescriptions['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    logging.debug('converting sysdate to datetime')
    prescriptions['sysdate'] = pd.to_datetime(prescriptions['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    prescriptions['type']=entry_type['prescription']
    logging.debug('writing to csv')
    prescriptions.to_csv(ROOT_DIR + '/data/pt_data/processed_data/prescriptions.csv',index=False)

def create_medcoded_entries():
    #logging.debug('calling create_medcoded_entries')
    """
    Creates create_medcoded_entries.csv
    This is a file containing a dataframe containing simplified data
    (just patient ID, eventdate, sysdate, and medcode) from the
    Extract_Clinical_001 and 002 files, Extract_Test_001 and 002 file and Extract_Referral_001 file
    (but not the Extract_Therapy_001 or 002 files or Extract_Consultations_001 or 002)
    """
    #logging.debug('processing clinical - reading clin1')
    clin1 = pd.read_csv(ROOT_DIR + '/data/pt_data/raw_data/Extract_Clinical_001.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    #logging.debug('processing clinical - reading clin2')
    clin2 = pd.read_csv(ROOT_DIR + '/data/pt_data/raw_data/Extract_Clinical_002.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    #logging.debug('processing clinical - concatenating')
    clinical = pd.concat([clin1,clin2])
    clinical['type']=entry_type['clinical']
    #logging.debug('processing clinical - converting to datetime - eventdate')
    clinical['eventdate'] = pd.to_datetime(clinical['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('processing clinical - converting to datetime - sysdate')
    clinical['sysdate'] = pd.to_datetime(clinical['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)

    #logging.debug('processing tests')
    test1 = pd.read_csv(ROOT_DIR + '/data/pt_data/raw_data/Extract_Test_001.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    test2 = pd.read_csv(ROOT_DIR + '/data/pt_data/raw_data/Extract_Test_002.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    #logging.debug('processing test - concatenating')
    test = pd.concat([test1,test2])
    test['type']=entry_type['test']
    #logging.debug('processing test - converting to datetime - eventdate')
    test['eventdate'] = pd.to_datetime(test['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('processing test - converting to datetime - sysdate')
    test['sysdate'] = pd.to_datetime(test['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)

    #logging.debug('processing referrals')
    referral = pd.read_csv(ROOT_DIR + '/data/pt_data/raw_data/Extract_Referral_001.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    referral['type']=entry_type['referral']
    #logging.debug('processing referrals - converting to datetime - eventdate')
    referral['eventdate'] = pd.to_datetime(referral['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('processing referrals - converting to datetime - sysdate')
    referral['sysdate'] = pd.to_datetime(referral['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)

    #logging.debug('processing immunisations')
    immunisations = pd.read_csv(ROOT_DIR + '/data/pt_data/raw_data/Extract_Immunisation_001.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    immunisations['type']=entry_type['immunisation']
    #logging.debug('processing immunisations - converting to datetime - eventdate')
    immunisations['eventdate'] = pd.to_datetime(immunisations['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('processing  immunisations - converting to datetime - sysdate')
    immunisations['sysdate'] = pd.to_datetime(immunisations['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)

    #logging.debug('concatenating the different entry types')
    medcoded_entries = pd.concat([clinical,test,referral,immunisations])

    #logging.debug('writing to csv')
    medcoded_entries.to_csv(ROOT_DIR + '/data/pt_data/processed_data/medcoded_entries.csv',index=False)

def create_consultations():
    """
    Creates a csv file containing all the data from Extract_Consultation_001.txt and Extract_Consultation_002.txt
    """
    #logging.debug('reading Extract_Consultation_001.txt')
    cons1 = pd.read_csv(ROOT_DIR + '/data/pt_data/raw_data/Extract_Consultation_001.txt',delimiter='\t')
    #logging.debug('reading Extract_Consultation_002.txt')
    cons2 = pd.read_csv(ROOT_DIR + '/data/pt_data/raw_data/Extract_Consultation_002.txt',delimiter='\t')
    #logging.debug('concatenating')
    consultations = pd.concat([cons1,cons2])[['patid','sysdate','eventdate']]
    #logging.debug('converting to datetime - eventdate')
    consultations['eventdate'] = pd.to_datetime(consultations['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('converting to datetime - sysdate')
    consultations['sysdate'] = pd.to_datetime(consultations['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('adding type column')
    consultations['type']= entry_type['consultation']
    #logging.debug('writing to csv')
    consultations.to_csv(ROOT_DIR + '/data/pt_data/processed_data/consultations.csv',index=False)

def create_all_entries():
    """
    Creates a csv file (all_entries.csv) containing all entries (consultations, prescriptions, clinicals, tests, referrals)
    """
    #logging.debug('reading consultations')
    consultations = pd.read_csv(ROOT_DIR + '/data/pt_data/processed_data/consultations.csv',delimiter=',',parse_dates=['eventdate','sysdate'],infer_datetime_format=True)
    #logging.debug('reading medcoded entries')
    medcoded_entries = pd.read_csv(ROOT_DIR + '/data/pt_data/processed_data/medcoded_entries.csv',delimiter=',',parse_dates=['eventdate','sysdate'],infer_datetime_format=True)
    #logging.debug('reading prescriptions')
    prescriptions = pd.read_csv(ROOT_DIR + '/data/pt_data/processed_data/prescriptions.csv',delimiter=',',usecols=['patid','eventdate','sysdate','prodcode','type'],parse_dates=['eventdate','sysdate'],infer_datetime_format=True)
    #logging.debug('concatenating...')
    all_entries = pd.concat([consultations,medcoded_entries,prescriptions],ignore_index=True)
    #logging.debug('writing to file...')
    all_entries.to_csv(ROOT_DIR + '/data/pt_data/processed_data/all_entries.csv',index=False)
    return all_entries
