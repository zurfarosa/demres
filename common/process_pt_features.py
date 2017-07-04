import pandas as pd
import numpy as np
from datetime import date, timedelta,datetime
from demres.common import codelists,druglists
from demres.common.process_entries import *
from common.helper_functions import *
from demres.demins.constants import Study_Design as sd
from demres.common.logger import logging

def create_pt_features():
    '''
    Creates csv file containing all patients (cases and controls on separate rows)
    with a column for all variables to be analysed
    '''
    pt_features = pd.read_csv('data/pt_data/raw_data/Extract_Patient_001.txt', usecols=['patid','yob','gender','reggap'], delimiter='\t')
    # Remove patients with registration gaps of more than one day
    pts_with_registration_gaps = pt_features.loc[pt_features['reggap']>sd.acceptable_number_of_registration_gap_days]
    pts_with_registration_gaps.to_csv('data/pt_data/removed_patients/pts_with_registration_gaps.csv',index=False)
    pt_features = pt_features.loc[pt_features['reggap']==sd.acceptable_number_of_registration_gap_days]
    pt_features.drop('reggap',axis=1,inplace=True)

    pt_features['pracid']=pt_features['patid'].apply(str).str[-3:] #bizarre, but this is how the pracid works!
    pt_features['female'] = pt_features['gender']-1
    pt_features.drop(['gender'],axis=1,inplace=True)
    # pt_features['yob'] = pt_features['yob']+1800 # ditto!
    pt_features['yob'] = pt_features['yob'].astype(str).str[1:]

    # pt_features.to_csv('data/pt_data/processed_data/pt_features.csv',index=False)
    return pt_features

def get_index_date_and_caseness_and_add_final_dementia_subtype(all_entries,pt_features):
    '''
    Calculates  index date and establishes caseness by looking for first dementia diagnoses.
    Also looks for final dementia diagnosis (e.g. 'vascular dementia'), as this is likely to be our best guess as to the dementia subtype
    '''

    pegmed = pd.read_csv('data/dicts/proc_pegasus_medical.csv',delimiter=',')
    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv',delimiter=',')
    medcodes = get_medcodes_from_readcodes(codelists.all_dementia)
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

def only_include_specific_dementia_subtype(pt_features,subtype='all_dementia'):
    if subtype == 'all_dementia':
        return pt_features
    elif subtype=='alzheimers':
        subtype_codelist = codelists.alzheimers
    elif subtype=='vascular':
        subtype_codelist = codelists.vascular
    pt_features = pt_features[(pt_features['isCase']==False) |(pt_features['final dementia medcode'].isin(get_medcodes_from_readcodes(subtype_codelist)))]
    return pt_features


def add_data_start_and_end_dates(all_encounters,pt_features):
    '''
    This function looks at all clinical encounters (e.g. referrals, consultations, but not prescriptions)
    to find the data start and end dates.
    '''
    logging.debug('add_sys_start_and_end_dates_to_pt_features all_entries.csv')

    #Calculate the data_end date - we can use the last sysdate
    print('calculating lastest_sysdate')
    latest_sysdates = all_encounters.groupby('patid')['sysdate'].max().reset_index()
    latest_sysdates.rename(columns={'sysdate':'data_end'},inplace=True)
    pt_features = pd.merge(pt_features,latest_sysdates,how='left')

    #We now find the earliest sysdate - however, this will not necessarily be the data_start date, as often patients have detailed notes prior to this, entered retrospectively
    print('calculating earliest_sysdate')
    earliest_sysdates = all_encounters.groupby('patid')['sysdate'].min().reset_index()
    earliest_sysdates.rename(columns={'sysdate':'earliest_sysdate'},inplace=True)
    pt_features = pd.merge(pt_features,earliest_sysdates,how='left')

    #As an alternative to the earliest sysdate, find the earliest year in which you have at least 15
    # retrospectively-dated entries - this, in my opinion, is likely to be when the electronic record
    # started to be filled in prospectively (the reason for the discrepancy between the eventdate and the sysdate
    # is probably because the entries were given a new sysdate for some reason, e.g. software update)
    print('resampling all_encounters - may take some time...')
    resampled_entries = all_encounters.set_index('eventdate').groupby('patid').resample('AS').size()
    resampled_entries2 = resampled_entries.reset_index()
    resampled_entries2.columns = ['patid','year','consultation_count']
    resampled_entries3 = resampled_entries2.loc[resampled_entries2['consultation_count']>=15]
    resampled_entries4 = resampled_entries3.groupby('patid').year.min().reset_index()
    resampled_entries4['year']=resampled_entries4['year']+pd.Timedelta(days=365)
    resampled_entries4.columns=['patid','start_of_year_after_earliest_year_with_>15_consultations']
    pt_features = pd.merge(pt_features,resampled_entries4,how='left')

    # Watch out for 'converted codes' (medcode 14) - these are uninformative medcodes where the specific Read codes have
    # been lost, probably due to some software update in the 1990s.
    print('locating converted codes')
    converted_code_entries = all_encounters[all_encounters['medcode']==14]
    latest_converted_code_entries = converted_code_entries.groupby('patid')['sysdate'].max().reset_index()
    latest_converted_code_entries.columns = ['patid','sysdate_of_final_converted_code']
    pt_features = pd.merge(pt_features,latest_converted_code_entries,how='left')

    # Now choose which measure we are going to use for data_start. Note that if a converted code exists for a patid,
    # it's probably safest just to use the earliest sysdate
    print('choosing most appropriate measure of data_start')
    dont_use_earliest_sysdate_mask = ((pt_features['start_of_year_after_earliest_year_with_>15_consultations']<pt_features['earliest_sysdate']) &
        ((pt_features['start_of_year_after_earliest_year_with_>15_consultations'] > pt_features['sysdate_of_final_converted_code']) | (pd.isnull(pt_features['sysdate_of_final_converted_code'])))
            )
    pt_features['data_start']=np.nan
    pt_features.loc[dont_use_earliest_sysdate_mask,'data_start']=pt_features['start_of_year_after_earliest_year_with_>15_consultations'].copy()
    pt_features.loc[~dont_use_earliest_sysdate_mask,'data_start']=pt_features['earliest_sysdate'].copy()

    # Remove patients without any events
    print('removing patients without any events')
    no_event_mask = pd.isnull(pt_features['earliest_sysdate'])
    print('There are {0} patients without any events'.format(len(pt_features[no_event_mask])))
    if len(pt_features[no_event_mask])>0:
        pts_without_any_events.loc[:,'reason_for_removal']='Pt did not have any events'
        pts_without_any_events.to_csv('data/pt_data/removed_patients/pts_without_any_events.csv',index=False)
    pt_features = pt_features.loc[~no_event_mask].copy()

    pt_features.drop(['earliest_sysdate',
       'sysdate_of_final_converted_code',
       'start_of_year_after_earliest_year_with_>15_consultations'],inplace=True,axis=1)


    return pt_features


def match_cases_and_controls(pt_features,window):
    '''
    Matches cases and controls. Will not match cases to controls who do not have enough years of data
    '''
    req_yrs_post_index=sd.req_yrs_post_index
    start_year=abs(window['start_year'])
    pt_features['matchid']=np.nan
    # pt_features['data_end'] = pd.to_datetime(pt_features['data_end'],errors='coerce', format='%Y-%m-%d')
    # pt_features['data_start'] = pd.to_datetime(pt_features['data_start'],errors='coerce', format='%Y-%m-%d')
    # pt_features['index_date'] = pd.to_datetime(pt_features['index_date'],errors='coerce', format='%Y-%m-%d')
    pt_features.loc[:,'total_available_data']= pt_features.loc[:,'data_end'] - pt_features.loc[:,'data_start']
    pt_features.sort_values(inplace=True,by='total_available_data',ascending=True) # To make matching more efficient, first try to match to controls the cases with with the LEAST amount of available data

    cases_mask = (pt_features['isCase']==True) & \
                (pt_features['data_start'] <= (pt_features['index_date'] - timedelta(days=(365*start_year))))
    suitable_cases = pt_features.loc[cases_mask].copy()
    print('length of suitable cases',len(suitable_cases))
    controls = pt_features.loc[pt_features['isCase']==False].copy()
    print('length of controls',len(controls))
    for index,row in suitable_cases.iterrows():
        if pd.isnull(row['matchid']):
            patid = row['patid']
            yob = row['yob']
            female = row['female']
            index_date = row['index_date']
            # Define matching criteria
            matches_yob = controls['yob']==yob
            matches_gender = controls['female']==female
            # matches_practice = controls['pracid']==pracid
            enough_data_after_index_date = controls['data_end'] >= (index_date + timedelta(days=(365*req_yrs_post_index)))
            enough_data_before_index_date = controls['data_start'] <= (index_date - timedelta(days=(365*start_year)))
            match_mask =  matches_yob & matches_gender & enough_data_after_index_date & enough_data_before_index_date #& matches_practice
            if len(controls[match_mask])>0:
                best_match_index = controls.loc[match_mask,'total_available_data'].idxmin(axis=1) # To make matching more efficient, first try to match cases with those controls with the LEAST amount of available data
                best_match_id = controls.ix[best_match_index]['patid']
                logging.debug('Out of a list of {0} matching patients, patid {1} is the best match for {2}'.format(len(controls[match_mask]),best_match_id,patid))
                #give both the case and control a unique match ID (for convenience, I've used the iterrows index)
                pt_features.loc[index,'matchid']=index
                pt_features.loc[best_match_index,'matchid']=index
                pt_features.loc[best_match_index,'index_date']=index_date
                controls = controls.drop(best_match_index) #drop this row from controls dataframe so it cannot be matched again
            else:
                logging.debug('No match found for {0}'.format(patid))
    pt_features.drop('total_available_data',axis=1,inplace=True)

    #Now that we have an index date for both cases and controls, finally calculate age at index date
    pt_features['age_at_index_date'] = pd.DatetimeIndex(pt_features['index_date']).year.astype(int) - (1900 + pt_features['yob'].astype(int))

    return pt_features

def delete_unmatched_cases_and_controls(pt_features):
    '''
    Removes all unmatched cases and controls
    '''
    removed_pts = pt_features.loc[pd.isnull(pt_features['matchid'])]
    removed_pts.loc[:,'reason_for_removal']='Unmatchable'
    print(len(removed_pts),' patients being removed as unmatchable')
    removed_pts.to_csv('data/pt_data/removed_patients/removed_unmatched_patients.csv',index=False)
    pt_features = pt_features.loc[pd.notnull(pt_features['matchid'])]
    pt_features.loc[:,'matchid']=pt_features['matchid'].astype(int)
    return pt_features

def delete_patients_if_not_enough_data(isCase,pt_features,start_year):
    '''
    Despite requiring user to specify whether patients are cases or controls, this only needs to be called for cases,
    as controls without enough data are removed by the match_cases_and_controls() function.
    '''
    delete_mask = (pt_features['days pre_indexdate']<(start_year*365)) \
            | (pt_features['days post_indexdate']<(sd.req_yrs_post_index*365))
    delete_mask = delete_mask & (pt_features['isCase']==isCase)
    #delete cases and controls if not enough data prior to index dates
    removed_pts = pt_features.loc[delete_mask]
    removed_pts['reason_for_removal']='Not enough available data prior or post index date'
    removed_pts.to_csv('data/pt_data/removed_patients/removed_pts_with_not_enough_data.csv',mode='a',index=False)
    pt_features=pt_features.loc[delete_mask == False]
    # pt_features.to_csv('data/pt_data/processed_data/pt_features.csv',index=False)
    return pt_features


def get_multiple_condition_statuses(pt_features,entries,window,conditions):
    for condition in conditions:
        print(condition['name'])
        pt_features = get_condition_status(pt_features,entries,window,condition)
    return pt_features

def get_condition_status(pt_features,entries,window,condition):
    '''
    Searches a patient's history (i.e. the list of medcoded entries) for any one of a list of related Read codes
    (e.g. 'clinically significant alcohol use', or 'insomnia') during a given exposure window  (e.g. 5-10 years prior to index date).
    According to the 'count_or_boolean' parameter, will return either a count of the Read codes (i.e. insomnia) or a simple boolean (all other conditions).
    '''

    medcodes = get_medcodes_from_readcodes(condition['codes'])
    medcode_events = entries[entries['medcode'].isin(medcodes)]
    medcode_events = medcode_events[pd.notnull(medcode_events['eventdate'])] #drops a small number of rows  with NaN eventdates
    print('\tTotal {0} events in all medcoded_events dataframe: {1}'.format(condition['name'],len(medcode_events)))
    medcode_events = pd.merge(medcode_events[['patid','eventdate']],pt_features[['patid','index_date']],how='inner',on='patid')
    # If we're using all the patient's history from the exposure window back to birth
    #(e.g. for intellectual disability), overwrite the predefined exposure windows with a single window

    if condition['record_exposure_in_window_period_only']==True:
        start_year = timedelta(days=(365*abs(window['start_year'])))
        print('\t{0} is being measured only during the window period'.format(condition['name']))
    else: #for all other conditions, record exposure from end of window period back to start of their records
        start_year = timedelta(days=(365*100))

    new_colname = condition['name']

    if new_colname in pt_features.columns: #delete column if it already exists (otherwise this causes problems with the 'fillna' command below)
        pt_features.drop(new_colname,axis=1,inplace=True)

    # Restrict event counts to those that occur during pt's exposure window
    relevant_event_mask = (medcode_events['eventdate']>=(medcode_events['index_date']-start_year)) & (medcode_events['eventdate']<=(medcode_events['index_date']-timedelta(days=(365*sd.window_length_in_years))))
    window_medcode_events = medcode_events.loc[relevant_event_mask]
    window_medcode_events = window_medcode_events.groupby('patid')['eventdate'].count().reset_index()
    window_medcode_events.columns=['patid',new_colname]
    print('\t{0} events in this window for our patients: {1}'.format(new_colname,len(window_medcode_events)))

    #delete zero counts
    window_medcode_events = window_medcode_events.loc[window_medcode_events[new_colname]>0]

    pt_features = pd.merge(pt_features,window_medcode_events,how='left')

    pt_features[new_colname].fillna(0,inplace=True)


    if condition['int_or_boolean']=='boolean': #convert condition from a count to a boolean
        pt_features.loc[pt_features[new_colname]>0,new_colname] = 1
        pt_features.loc[pt_features[new_colname]==0,new_colname] = 0

    pt_features[new_colname] = pt_features[new_colname].astype(int)

    print('\tUnique values  ',set(pt_features[new_colname]))

    return pt_features


def create_quantiles_and_booleans(pt_features):
    '''
    Converts various continuous variables (e.g. age, insomnia) into quantiles,
    and converts others (insomnia, benzodiazepine_pdd) into booleans
    '''

    benzo_mask = pt_features['benzo_and_z_drugs_100_pdds']>0
    pt_features['benzo_and_z_drugs_any']=np.nan
    pt_features.loc[benzo_mask,'benzo_and_z_drugs_any']=1
    pt_features.loc[~benzo_mask,'benzo_and_z_drugs_any']=0

    #for the insomnia variable, create an additional dichotomous yes/no variable ('insomnia_any')
    pt_features['insomnia_any']= np.nan
    pt_features.loc[pt_features['insomnia']>0,'insomnia_any'] = 1
    pt_features.loc[pt_features['insomnia']==0,'insomnia_any'] = 0

    #Also, create quantiles for insomnia
    insomnia_count_0_mask = pt_features['insomnia']==0
    insomnia_count_1_5_mask = (pt_features['insomnia']>0) & (pt_features['insomnia']<=5)
    insomnia_count_above_5_mask = pt_features['insomnia']>5
    pt_features.loc[insomnia_count_0_mask,'insomnia_count:0']=1
    pt_features.loc[~insomnia_count_0_mask,'insomnia_count:0']=0
    pt_features.loc[insomnia_count_1_5_mask,'insomnia_count:1_5']=1
    pt_features.loc[~insomnia_count_1_5_mask,'insomnia_count:1_5']=0
    pt_features.loc[insomnia_count_above_5_mask,'insomnia_count:above_5']=1
    pt_features.loc[~insomnia_count_above_5_mask,'insomnia_count:above_5']=0

    #Create quantiles for non_insomnia_GP_consultations
    # (these are only used in the baseline characteristics section of the paper, not in the actual logistic regression)
    non_insomnia_GP_consultations_0_mask = pt_features['non_insomnia_GP_consultations']==0
    non_insomnia_GP_consultations_1_10_mask = (pt_features['non_insomnia_GP_consultations']>0) & (pt_features['non_insomnia_GP_consultations']<=10)
    non_insomnia_GP_consultations_11_100_mask = (pt_features['non_insomnia_GP_consultations']>10) & (pt_features['non_insomnia_GP_consultations']<=100)
    non_insomnia_GP_consultations_101_1000_mask = (pt_features['non_insomnia_GP_consultations']>100) & (pt_features['non_insomnia_GP_consultations']<=1000)
    non_insomnia_GP_consultations_above_1000_mask = pt_features['non_insomnia_GP_consultations']>1000
    pt_features.loc[non_insomnia_GP_consultations_0_mask,'non_insomnia_GP_consultations:0']=1
    pt_features.loc[~non_insomnia_GP_consultations_0_mask,'non_insomnia_GP_consultations:0']=0
    pt_features.loc[non_insomnia_GP_consultations_1_10_mask,'non_insomnia_GP_consultations:1_10']=1
    pt_features.loc[~non_insomnia_GP_consultations_1_10_mask,'non_insomnia_GP_consultations:1_10']=0
    pt_features.loc[non_insomnia_GP_consultations_11_100_mask,'non_insomnia_GP_consultations:11_100']=1
    pt_features.loc[~non_insomnia_GP_consultations_11_100_mask,'non_insomnia_GP_consultations:11_100']=0
    pt_features.loc[non_insomnia_GP_consultations_101_1000_mask,'non_insomnia_GP_consultations:101_1000']=1
    pt_features.loc[~non_insomnia_GP_consultations_101_1000_mask,'non_insomnia_GP_consultations:101_1000']=0
    pt_features.loc[non_insomnia_GP_consultations_above_1000_mask,'non_insomnia_GP_consultations:above_1000']=1
    pt_features.loc[~non_insomnia_GP_consultations_above_1000_mask,'non_insomnia_GP_consultations:above_1000']=0

    # Create quantiles for age
    # (these are only used in the baseline characteristics section of the paper, not in the actual logistic regression)
    age_65_69_mask = pt_features['age_at_index_date']<70
    age_70_74_mask = (pt_features['age_at_index_date']<75) & (pt_features['age_at_index_date']>=70)
    age_75_79_mask = (pt_features['age_at_index_date']<80) & (pt_features['age_at_index_date']>=75)
    age_80_84_mask = (pt_features['age_at_index_date']<85) & (pt_features['age_at_index_date']>=80)
    age_85_89_mask = (pt_features['age_at_index_date']<90) & (pt_features['age_at_index_date']>=85)
    age_90_94_mask = (pt_features['age_at_index_date']<95) & (pt_features['age_at_index_date']>=90)
    age_95_99_mask = (pt_features['age_at_index_date']<100) & (pt_features['age_at_index_date']>=95)
    above_99_mask = pt_features['age_at_index_date']>=100
    pt_features.loc[age_65_69_mask,'age_at_index_date:65-69']=1
    pt_features.loc[~age_65_69_mask,'age_at_index_date:65-69']=0
    pt_features.loc[age_70_74_mask,'age_at_index_date:70-74']=1
    pt_features.loc[~age_70_74_mask,'age_at_index_date:70-74']=0
    pt_features.loc[age_75_79_mask,'age_at_index_date:75-79']=1
    pt_features.loc[~age_75_79_mask,'age_at_index_date:75-79']=0
    pt_features.loc[age_80_84_mask,'age_at_index_date:80-84']=1
    pt_features.loc[~age_80_84_mask,'age_at_index_date:80-84']=0
    pt_features.loc[age_85_89_mask,'age_at_index_date:85-89']=1
    pt_features.loc[~age_85_89_mask,'age_at_index_date:85-89']=0
    pt_features.loc[age_90_94_mask,'age_at_index_date:90-99']=1
    pt_features.loc[~age_90_94_mask,'age_at_index_date:90-99']=0
    pt_features.loc[above_99_mask,'age_at_index_date:above_99']=1
    pt_features.loc[~above_99_mask,'age_at_index_date:above_99']=0

    for drug in ['antidepressants_100_pdds','antipsychotics_100_pdds','depot_antipsychotics_100_pdds','other_sedatives_100_pdds','benzo_and_z_drugs_100_pdds','mood_stabilisers_100_pdds']:
        drug_pdds = pt_features[drug] * 100 #convert unit from '100 pdds' to 'pdds'
        drug_0_mask = drug_pdds==0
        drug_1_10_mask = (drug_pdds>0) & (drug_pdds<=10)
        drug_11_100_mask = (drug_pdds>10) & (drug_pdds<=100)
        drug_101_1000_mask = (drug_pdds>100) & (drug_pdds<=1000)
        drug_1001_10000_mask = (drug_pdds>1000) & (drug_pdds<=10000)
        drug_above_10000_mask = drug_pdds>10000
        drug_name_with_100_pdds_removed = drug.replace('s_100','')

        pt_features.loc[drug_0_mask,drug_name_with_100_pdds_removed+':00000']=1
        pt_features.loc[~drug_0_mask,drug_name_with_100_pdds_removed+':00000']=0

        pt_features.loc[drug_1_10_mask,drug_name_with_100_pdds_removed+':00001_10']=1
        pt_features.loc[~drug_1_10_mask,drug_name_with_100_pdds_removed+':00001_10']=0

        pt_features.loc[drug_11_100_mask,drug_name_with_100_pdds_removed+':00011_100']=1
        pt_features.loc[~drug_11_100_mask,drug_name_with_100_pdds_removed+':00011_100']=0

        pt_features.loc[drug_101_1000_mask,drug_name_with_100_pdds_removed+':00101_1000']=1
        pt_features.loc[~drug_101_1000_mask,drug_name_with_100_pdds_removed+':00101_1000']=0

        pt_features.loc[drug_1001_10000_mask,drug_name_with_100_pdds_removed+':01001_10000']=1
        pt_features.loc[~drug_1001_10000_mask,drug_name_with_100_pdds_removed+':01001_10000']=0

        pt_features.loc[drug_above_10000_mask,drug_name_with_100_pdds_removed+':10000_and_above']=1
        pt_features.loc[~drug_above_10000_mask,drug_name_with_100_pdds_removed+':10000_and_above    ']=0

    return pt_features

def get_relevant_and_reformatted_prescs(prescriptions,druglists,pt_features,window):
    '''
    Filter prescriptions to only include ones which are for relevant drugs and within the exposure window,
    and create 'amount' and 'unit' columns (necessary for calculating PDD)
    '''
    prescs = pd.merge(prescriptions,pt_features[['patid','index_date']],how='left',on='patid')
    prescs = prescs.loc[pd.notnull(prescs['qty'])].copy() #remove the relatively small number of prescriptions where the quantity is NaN

    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv')
    prescs = pd.merge(prescs,pegprod[['prodcode','substance strength','route','drug substance name']],how='left')

    #Only use prescriptions belonging to the main exposure window (not the ones used in sensitivity analysis)
    start_year = timedelta(days=(365*abs(sd.exposure_windows[1]['start_year'])))
    end_year = timedelta(days=(365*abs(sd.exposure_windows[1]['start_year']+sd.window_length_in_years)))
    timely_presc_mask = (prescs['eventdate']>=(prescs['index_date']-start_year)) & (prescs['eventdate']<=(prescs['index_date']-end_year))
    timely_prescs = prescs.loc[timely_presc_mask].copy()

    all_drugs = [drug for druglist in druglists for drug in druglist['drugs'] ]

    prodcodes = get_prodcodes_from_drug_name(all_drugs)
    relev_prescs = timely_prescs.loc[timely_prescs['prodcode'].isin(prodcodes)].copy()

    # Create new columns ('amount' and 'unit', extracted from the 'substrance strength' string)
    amount_and_unit = relev_prescs['substance strength'].str.extract('([\d\.]+)([\d\.\+ \w\/]*)',expand=True)
    amount_and_unit.columns=['amount','unit']
    amount_and_unit.amount = amount_and_unit.amount.astype('float')
    reformatted_prescs = pd.concat([relev_prescs,amount_and_unit],axis=1).drop(['numpacks','numdays','packtype','issueseq'],axis=1)

    # Convert micrograms to mg
    micro_mask = reformatted_prescs['unit'].str.contains('microgram',na=False,case=False)
    reformatted_prescs.loc[micro_mask,'amount'] /= 1000
    reformatted_prescs.loc[micro_mask,'unit'] = 'mg'

    #Convert mg/Xml to mg for simplicity
    micro_mask = reformatted_prescs['unit'].str.contains('mg/',na=False,case=False)
    reformatted_prescs.loc[micro_mask,'unit'] = 'mg'

    #Remove the small number of  prescriptions where there is no amount
    reformatted_prescs = reformatted_prescs[pd.notnull(reformatted_prescs['amount'])].copy()

    # Create a 'total_amount' column - used to calculate each pt's PDDs for a given drug.
    reformatted_prescs['total_amount'] = reformatted_prescs['qty']*reformatted_prescs['amount']

    #Change all 'numeric daily doses' (NDD) from 0 (this appears to be the default in the CPRD data) to 1.
    #Note that an NDD of 2 means 'twice daily'
    reformatted_prescs.loc[reformatted_prescs['ndd'] == 0,'ndd']=1

    return reformatted_prescs

def create_pdd_for_each_drug(prescriptions,druglists,pt_features,window):
    '''
    Create a prescribed daily dose for each drug, based on average doses in the patient sample during the main exposure window
    '''
    prescs = get_relevant_and_reformatted_prescs(prescriptions,druglists,pt_features,window)

    pdds = pd.DataFrame(columns=['drug_name','drug_type','pdd(mg)'])

    for druglist in druglists:
        prodcodes = get_prodcodes_from_drug_name(druglist['drugs'])
        druglist_prescs = prescs.loc[prescs['prodcode'].isin(prodcodes)].copy()

        # Remove prescriptions if they are not of the route (e.g. oral) specified on the druglist
        druglist_prescs = druglist_prescs.loc[prescs['route'].str.contains(druglist['route'],na=False,case=False)]

        #Calculate the prescribed daily dose (PDD) for each drug (e.g. 'citalopram') in the druglist (e.g. 'antidepressants')
        for drug in druglist['drugs']:
            drug = drug.upper()
            temp_prescs = druglist_prescs[druglist_prescs['drug substance name'].str.upper()==drug].copy()
            if(len(temp_prescs))>0:
                drug_amounts = np.array(temp_prescs['amount'])*np.array(temp_prescs['ndd'])
                drug_weights = np.array(temp_prescs['qty'])/np.array(temp_prescs['ndd'])
                pdd = np.average(drug_amounts,weights=drug_weights)
                print(drug,'\tpdd:',str(pdd))
                pdds.loc[len(pdds)]=[drug,druglist['name'], pdd]
                assert pd.notnull(pdd)
            else:
                print(drug,'\tNo prescriptions found')

    #Write PDDs to file for reference
    pdds.to_csv('output/drug_pdds.csv',index=False)


def create_PDD_columns_for_each_pt(pt_features,window,druglists,prescriptions):
    '''
    Adds a prescribed daily doses (PDD) column for each drug in a druglist to the pt_features dataframe
    '''
    pdds = pd.read_csv('output/drug_pdds.csv', delimiter=',')
    prescs = get_relevant_and_reformatted_prescs(prescriptions,druglists,pt_features,window)
    prescs_grouped = prescs.groupby(by=['patid','prodcode','drug substance name']).total_amount.sum().reset_index()
    for druglist in druglists:
        new_colname = druglist['name']+'_100_pdds'
        prodcodes = get_prodcodes_from_drug_name(druglist['drugs'])
        print(len(prodcodes))
        relev_prescs = prescs_grouped.loc[prescs_grouped['prodcode'].isin(prodcodes)]
        print(relev_prescs)

        # Sum the total pdds for each patients (e.g. lorazpeam AND zopiclone AND promethazine etc.).
        # Then divide by 100, because 100_PDDs gives a more clinically useful odds ratio at the regression stage
        relev_prescs.loc[:,new_colname]=(relev_prescs['total_amount']/relev_prescs['drug substance name'].map(lambda x: pdds.loc[pdds['drug_name']==x.upper(),'pdd(mg)'].values[0]))/100

        pt_pdds = relev_prescs.groupby(by='patid')[new_colname].sum().reset_index().copy()
        if new_colname in pt_features.columns: #delete column if it already exists (otherwise this causes problems with the 'fillna' command below)
            pt_features.drop(new_colname,axis=1,inplace=True)
        pt_features = pd.merge(pt_features,pt_pdds,how='left')
        pt_features[new_colname].fillna(value=0,inplace=True)
    return pt_features


def get_consultation_count(pt_features,all_encounters,window):
    '''
    Counts the number of non-insomnia-related consultations with the GP during the exposure window
    '''
    relev_entries = pd.merge(all_encounters,pt_features[['patid','index_date']],how='inner')
    new_colname = 'non_insomnia_GP_consultations'

    # Find all consultations which occur on the same day as an insomnia readcode
    insomnia_medcodes = get_medcodes_from_readcodes(codelists.insomnia['codes'])
    insom_dates = relev_entries.loc[relev_entries['medcode'].isin(insomnia_medcodes),['eventdate','patid']]
    insom_dates['insomnia']=True
    marked_entries = pd.merge(relev_entries,insom_dates,how='left',left_on=['eventdate','patid'],right_on=['eventdate','patid'])
    marked_consultations = marked_entries.loc[marked_entries['type']==entry_type['consultation']]
    non_insom_cons = marked_consultations.loc[pd.isnull(marked_consultations['insomnia'])]
    non_insom_cons = non_insom_cons.drop('insomnia',axis=1)
    start_year = timedelta(days=(365*abs(window['start_year'])))
    window_mask = (non_insom_cons['eventdate']>=(non_insom_cons['index_date']-start_year)) & (non_insom_cons['eventdate']<=(non_insom_cons['index_date']-timedelta(days=(365*sd.window_length_in_years))))
    non_insom_cons = non_insom_cons[window_mask]
    non_insom_cons = non_insom_cons.groupby('patid')['eventdate'].count().reset_index()
    non_insom_cons.columns=['patid',new_colname]


    if new_colname in pt_features.columns: #delete column if it already exists (otherwise this causes problems with the 'fillna' command below)
        pt_features.drop(new_colname,axis=1,inplace=True)

    pt_features = pd.merge(pt_features,non_insom_cons,how='left')
    pt_features[new_colname].fillna(0,inplace=True)
    pt_features[new_colname] = pt_features[new_colname].astype(int)
    return pt_features
