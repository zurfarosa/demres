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
    pt_features['male'] = pt_features['gender']-1
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


def add_data_start_and_end_dates(all_entries,pt_features):
    '''
    Needs the dateframe created by create_medcoded_entries() to be passed to it.
    This function looks at all clinical entries (e.g. prescriptions, referrals, consultations), and looks for the first and last 'sysdated' entry.
    '''
    logging.debug('add_sys_start_and_end_dates_to_pt_features all_entries.csv')

    logging.debug('finding earliest sysdates')
    earliest_sysdates = all_entries.groupby('patid')['sysdate'].min().reset_index()
    earliest_sysdates = earliest_sysdates.rename(columns={'sysdate':'data_start'},copy=False)
    logging.debug('earliest_sysdates:\n{0}'.format(earliest_sysdates.head(5)))

    logging.debug('finding latest sysdates')
    latest_sysdates = all_entries.groupby('patid')['sysdate'].max().reset_index()
    latest_sysdates = latest_sysdates.rename(columns={'sysdate':'data_end'},copy=False)
    logging.debug('latest_sysdates:\n{0}'.format(latest_sysdates.head(5)))

    logging.debug('merging pt_features with earliest sysdates')
    pt_features = pd.merge(pt_features,earliest_sysdates,how='left')
    logging.debug('merging pt_features with latest sysdates')
    pt_features = pd.merge(pt_features,latest_sysdates,how='left')

    # Remove pts without any sysdates
    logging.debug('removing patients without any events')
    # pd.options.mode.chained_assignment = None  # default='warn'
    pts_without_any_events = pt_features.loc[pd.isnull(pt_features['data_start'])]
    logging.debug('There are {0} patients without any events'.format(len(pts_without_any_events)))
    if len(pts_without_any_events)>0:
        pts_without_any_events.loc[:,'reason_for_removal']='Pt did not have any events'
        pts_without_any_events.to_csv('data/pt_data/removed_patients/pts_without_any_events.csv',index=False)

    logging.debug('writing all the patients with events to pt_features.csv')
    pt_features = pt_features.loc[pd.notnull(pt_features['data_start'])]
    return pt_features


def match_cases_and_controls(pt_features,req_yrs_post_index,start_year):
    '''
    Matches cases and controls. Will not match cases to controls who do not have enough years of data
    '''
    pt_features['matchid']=np.nan
    # pt_features['data_end'] = pd.to_datetime(pt_features['data_end'],errors='coerce', format='%Y-%m-%d')
    # pt_features['data_start'] = pd.to_datetime(pt_features['data_start'],errors='coerce', format='%Y-%m-%d')
    # pt_features['index_date'] = pd.to_datetime(pt_features['index_date'],errors='coerce', format='%Y-%m-%d')
    pt_features.loc[:,'total_available_data']= pt_features.loc[:,'data_end'] - pt_features.loc[:,'data_start']
    pt_features.sort_values(inplace=True,by='total_available_data',ascending=True) # To make matching more efficient, first try to match to controls the cases with with the LEAST amount of available data

    cases_mask = (pt_features['isCase']==True) & \
                (pt_features['data_start'] <= (pt_features['index_date'] - timedelta(days=(365*start_year))))
    suitable_cases = pt_features.loc[cases_mask]
    controls = pt_features.loc[pt_features['isCase']==False]
    for index,row in suitable_cases.iterrows():
        if pd.isnull(row['matchid']):
            patid = row['patid']
            yob = row['yob']
            male = row['male']
            pracid = row['pracid']
            index_date = row['index_date']
            # Define matching criteria
            matches_yob = controls['yob']==yob
            matches_male = controls['male']==male
            # matches_practice = controls['pracid']==pracid
            # is_not_already_matched = pd.isnull(controls['matchid'])
            enough_data_after_index_date = controls['data_end'] >= (index_date + timedelta(days=(365*req_yrs_post_index)))
            enough_data_before_index_date = controls['data_start'] <= (index_date - timedelta(days=(365*start_year)))
            match_mask =  matches_yob & matches_male & enough_data_after_index_date & enough_data_before_index_date #& matches_practice
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
    pt_features = pt_features.drop('total_available_data',axis=1)

    #Now that we ha ve an index date for both cases and controls, finally calculate age at index date
    pt_features['age_at_index_date'] = pd.DatetimeIndex(pt_features['index_date']).year.astype(int) - ('19' + pt_features['yob'].astype(str)).astype(int)

    return pt_features

def delete_unmatched_cases_and_controls(pt_features):
    '''
    Removes all unmatched cases and controls
    '''
    removed_pts = pt_features.loc[pd.isnull(pt_features['matchid'])]
    removed_pts.loc[:,'reason_for_removal']='Unmatchable'
    removed_pts.to_csv('data/pt_data/removed_patients/removed_unmatched_patients.csv',index=False)
    pt_features = pt_features.loc[pd.notnull(pt_features['matchid'])]
    pt_features['matchid']=pt_features['matchid'].astype(int)
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

    if condition['use_all_pt_history']:
        start_year = timedelta(days=(365*100))
    else:
        start_year = timedelta(days=(365*abs(window['start_year'])))


    new_colname = condition['name']

    # Restrict event counts to those that occur during pt's exposure window
    relevant_event_mask = (medcode_events['eventdate']>=(medcode_events['index_date']-start_year)) & (medcode_events['eventdate']<=(medcode_events['index_date']-timedelta(days=(365*sd.window_length_in_years))))
    window_medcode_events = medcode_events.loc[relevant_event_mask]
    window_medcode_events = window_medcode_events.groupby('patid')['eventdate'].count().reset_index()
    window_medcode_events.columns=['patid',new_colname]
    print('\t{0} events in this window for our patients: {1}'.format(new_colname,len(window_medcode_events)))

    #delete zero counts
    window_medcode_events = window_medcode_events.loc[window_medcode_events[new_colname]>0]

    pt_features = pd.merge(pt_features,window_medcode_events,how='left')

    if condition['int_or_boolean']=='both': # e.g. insomnia - we want both a boolean variable and a count (the former seems to be more useful in our model)
        #Rename and keep the 'count' column
        pt_features[new_colname+'_consultations']= pt_features[new_colname]
        pt_features[new_colname+'_consultations'].fillna(0,inplace=True)
        pt_features[new_colname+'_consultations'] = pt_features[new_colname+'_consultations'].astype(int)

    #Convert the original count column to a boolean column
    pt_features.loc[pd.notnull(pt_features[new_colname]),new_colname] = 1
    pt_features.loc[pd.isnull(pt_features[new_colname]),new_colname] = 0
    pt_features[new_colname] = pt_features[new_colname].astype(int)

    return pt_features


def create_pdds(pt_features,prescriptions,window,list_of_druglists):

    prescs = pd.merge(prescriptions,pt_features[['patid','index_date']],how='left',on='patid')
    prescs = prescs[pd.notnull(prescs['qty'])] #remove the relatively small number of prescriptions where the quantity is NaN
    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv')
    prescs = pd.merge(prescs,pegprod[['prodcode','substance strength','route','drug substance name']],how='left')

    for druglist in list_of_druglists:
        pt_features = create_pdd(pt_features,prescs,window,druglist) #note that create_ppd returns a tuple
    return pt_features

def create_pdd(pt_features,prescriptions,window,druglist):
    '''
    Adds a 100 prescribed daily doses (PDD) column for each drug in a druglist to the pt_features dataframe
    '''
    prodcodes = get_prodcodes_from_drug_name(druglist['drugs'])
    prescs = prescriptions.loc[prescriptions['prodcode'].isin([prodcodes])]

    # Remove prescriptions if they are not of the route (e.g. oral) specified on the druglist
    prescs = prescs.loc[prescs['route'].str.contains(druglist['route'],na=False,case=False)]

    # Create new columns ('amount' and 'unit', extracted from the 'substrance strength' string)
    amount_and_unit = prescs['substance strength'].str.extract('([\d\.]+)([\d\.\+ \w\/]*)',expand=True)
    amount_and_unit.columns=['amount','unit']
    amount_and_unit.amount = amount_and_unit.amount.astype('float')
    prescs = pd.concat([prescs,amount_and_unit],axis=1).drop(['numpacks','numdays','packtype','issueseq'],axis=1)

    # Create a 'total_amount' column - used to calculate each pt's PDDs for a given drug.
    prescs['total_amount'] = prescs['qty']*prescs['amount']

    #Change all 'numeric daily doses' (NDD) from 0 (this appears to be the default in the CPRD data) to 1.
    #Note that an NDD of 2 means 'twice daily'
    prescs.loc[prescs['ndd'] == 0,'ndd']=1

    #Only use prescriptions belonging to the exposure window
    start_year = timedelta(days=(365*abs(window['start_year'])))
    relevant_presc_mask = (prescs['eventdate']>=(prescs['index_date']-start_year)) & (prescs['eventdate']<=(prescs['index_date']-timedelta(days=(365*sd.window_length_in_years))))
    window_prescs = prescs[relevant_presc_mask]

    #Calculate the prescribed daily dose (PDD) for each drug (e.g. 'citalopram') in the druglist (e.g. 'antidepressants')
    pdds = {}
    for drug in druglist['drugs']:
        drug = drug.upper()
        temp_prescs = window_prescs[window_prescs['drug substance name'].str.upper()==drug]
        if(len(temp_prescs))>0:
            drug_amounts = np.array(temp_prescs['amount'])*np.array(temp_prescs['ndd'])
            drug_weights = np.array(temp_prescs['qty'])/np.array(temp_prescs['ndd'])
            pdd = np.average(drug_amounts,weights=drug_weights)
            pdds[drug]=pdd
            assert pd.notnull(pdd)
    #Write PDDs to file for reference
    with open('output/pdds/'+druglist['name']+'_PDD_'+str(abs(window['start_year'])), 'w') as f:
        for key, value in pdds.items():
            f.write('{0}: {1}\n'.format(key, np.round(value)))

    #Calculate number of PDDs (if any) each pt has been prescribed for the drugs in the druglist.  Note that we use 100_PDDs (roughly 3.3 months worth of a drug), rather than PDDs, as it makes the eventual odds ratio easier to interpret clinically
    window_prescs = window_prescs.groupby(by=['patid','drug substance name']).total_amount.sum().reset_index()
    new_colname = druglist['name']+'_100_pdds'
    window_prescs[new_colname]=(window_prescs['total_amount']/window_prescs['drug substance name'].map(lambda x: pdds[x.upper()])) / 100
    pt_pdds = window_prescs.groupby(by='patid')[new_colname].sum().reset_index() #sum the total pdds for each patients (e.g. lorazpeam AND zopiclone AND promethazine etc.) divide by 100, because 100_PDDs gives a more clinically useful odds ratio at the regression stage

    pt_features = pd.merge(pt_features,pt_pdds,how='left')
    pt_features[new_colname].fillna(value=0,inplace=True)
    pt_features[new_colname] = pt_features[new_colname]

    #Create quantile columns
    if druglist['name'] == 'benzo_and_z_drugs':
        pt_features['benzo_and_z_drugs<1096']=0
        pt_features['benzo_and_z_drugs>1096']=0
        pt_features['benzo_and_z_drugs_never_used']=0

        pt_features.loc[pt_features[new_colname] == 0,'benzo_and_z_drugs_never_used']=1
        pt_features.loc[((pt_features[new_colname]*100) < 1096) & (pt_features[new_colname] >0),'benzo_and_z_drugs<1096']=1
        pt_features.loc[(pt_features[new_colname]*100) > 1096,'benzo_and_z_drugs>1096']=1

    return pt_features


def divide_benzo_pdd_into_quantiles(pt_features,column_to_change):
    mask = (pt_features[column_to_change]>0) & (pt_features[column_to_change]<=1)
    pt_features.loc[mask,'benzo_and_z_drugs_1_to_100pdds']=1
    pt_features['benzo_and_z_drugs_1_to_100pdds'].fillna(value=0,inplace=True)

    mask = (pt_features[column_to_change]>1) & (pt_features[column_to_change]<=10)
    pt_features.loc[mask,'benzo_and_z_drugs_101_to_1000pdds']=1
    pt_features['benzo_and_z_drugs_101_to_1000pdds'].fillna(value=0,inplace=True)

    mask = pt_features[column_to_change]>10
    pt_features.loc[mask,'benzo_and_z_drugs_more_than_1000pdds']=1
    pt_features['benzo_and_z_drugs_more_than_1000pdds'].fillna(value=0,inplace=True)

    # pt_features.drop([column_to_change],axis=1,inplace=True)

    return pt_features



def get_consultation_count(pt_features,all_entries,window):
    '''
    Counts the number of non-insomnia-related consultations with the GP during the exposure window
    '''
    relev_entries = pd.merge(all_entries,pt_features[['patid','index_date']],how='inner')
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

    pt_features = pd.merge(pt_features,non_insom_cons,how='left')
    pt_features[new_colname].fillna(0,inplace=True)
    pt_features[new_colname] = pt_features[new_colname].astype(int)
    return pt_features
