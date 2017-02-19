from import_file import *

def get_patient_history(all_entries,patid):
    '''
    Returns a dataframe containing all patient entries (prescriptions, consultations, immunisations etc) for a specific patient,
    annotated with read terms, drug substance names etc.
    '''
    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv',delimiter=',')
    pegmed = pd.read_csv('data/dicts/proc_pegasus_medical.csv',delimiter=',')
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

    matching = pd.read_csv('data/pt_data/matching_unmatched_removed.csv',delimiter=',')
    del(matching['match'])
    del(matching['control_end'])
    del(matching['control_start'])

    #Create the cases
    feature1 = matching.copy(deep=True)
    # reorder the columns
    feature1=feature1[['case_patid','case_pracid','case_gender','case_birthyear','case_index']]
    feature1['isCase']=True
    # rename the columns
    feature1.columns=['patid','pracid','gender','birthyear','index_date','isCase']

    #Create the controls
    feature2 = matching.copy(deep=True)
    # reorder the columns
    feature2=feature2[['control_patid','control_pracid','control_gender','control_birthyear','case_index']]
    feature2['isCase']=False
    # rename the columns
    feature2.columns=['patid','pracid','gender','birthyear','index_date','isCase']
    feature2['index_date']=np.nan

    #Merge cases and controls
    features = pd.concat([feature1,feature2])
    features=features[['patid','pracid','gender','birthyear','index_date','isCase']]

    # Add the previously removed patients from ummatched_cases.csv (these were unmatched in the original raw data files)
    # Note that I don't think these patients have any clinical events at all, and are thus automatically deleted at a later stage!
    ummatched_cases = pd.read_csv('data/pt_data/removed_patients/ummatched_cases.csv',delimiter=',')
    ummatched_cases['isCase']=True

    features = pd.concat([features,ummatched_cases])
    # features['index_date']= pd.to_datetime(features['index_date'],format='%d/%m/%Y',errors='coerce')

    features['index_date']=pd.to_datetime(features['index_date'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    features.to_csv('data/pt_data/pt_features.csv',index=False)

def correct_index_date_and_caseness_and_add_final_dementia_subtype(all_entries):
    '''
    Calculates correct index date and establishes caseness by looking for first dementia diagnoses.
    Also looks for final dementia diagnosis (e.g. 'vascular dementia'), as this is likely to be our best guess as to the dementia subtype
    Then deletes the (inaccurate) casesness and index date given to us by CPRD
    '''

    pegmed = pd.read_csv('data/dicts/proc_pegasus_medical.csv',delimiter=',')
    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv',delimiter=',')
    medcodes = get_medcodes_from_readcodes(codelists.dementia_readcodes)
    prodcodes = get_prodcodes_from_drug_name(codelists.antidementia_drugs)

    # from the all_entries df, get just those which contain a dementia dx of an antidementia drug prescription
    all_dementia_entries = all_entries[(all_entries['prodcode'].isin(prodcodes))|(all_entries['medcode'].isin(medcodes))]
    # for clarity, look up the Read terms
    all_dem_labelled = pd.merge(all_dementia_entries,pegmed,how='left')[['patid','prodcode','medcode','sysdate','eventdate','type','read term']]
    # for clarity, look up the drug names
    all_dem_labelled = pd.merge(all_dem_labelled,pegprod,how='left')[['patid','medcode','prodcode','sysdate','eventdate','type','drug substance name','read term']]
    all_dem_labelled.loc[:,'eventdate']=pd.to_datetime(all_dem_labelled.loc[:,'eventdate'])
    #Get the date of earliest dementia diagnosis / antidementia drug prescription - this will be the revised index date, and will also determine revised caseness
    earliest_dementia_dates = all_dem_labelled.groupby('patid')['eventdate'].min().reset_index()
    earliest_dementia_dates.rename(columns={'eventdate':'index_date'},inplace=True)
    pt_features = pd.read_csv('data/pt_data/pt_features.csv',delimiter=',')
    #Delete the old (CRPD-created) index_date and isCase, because we're about to create more accurate ones
    pt_features.drop(['isCase','index_date'],axis=1,inplace=True)
    pt_features = pd.merge(pt_features,earliest_dementia_dates,how='left')
    pt_features['isCase']=np.where(pd.notnull(pt_features['index_date']),True,False)
    # Get the final dementia diagnosis
    just_dementia_diagnoses = all_dem_labelled[pd.isnull(all_dem_labelled['prodcode'])]
    final_dementia_dx = just_dementia_diagnoses.loc[just_dementia_diagnoses.groupby('patid')['eventdate'].idxmax()][['patid','medcode','read term']]
    final_dementia_dx.rename(columns={'medcode':'final dementia medcode','read term':'final dementia read term'},inplace=True)
    pt_features = pd.merge(pt_features,final_dementia_dx,how='left')
    pt_features.to_csv('data/pt_data/pt_features.csv',index=False)

def add_data_start_and_end_dates_to_pt_entries(all_entries):
    '''
    Needs the dateframe created by create_medcoded_entries() to be passed to it.
    This will need to be rewritten when I know the PROPER way to get the start and end dates for each patient's period of data extraction.
    This function looks at all clinical entries (e.g. prescriptions, referrals, consultations), and looks for the first and last 'sysdated' entry.
    '''
    logging.debug('add_sys_start_and_end_dates_to_pt_features all_entries.csv')

    logging.debug('finding earliest systdates')
    earliest_sysdates = all_entries.sort_values(by='sysdate').groupby('patid').first().reset_index().loc[:,['patid','sysdate']]
    earliest_sysdates = earliest_sysdates.loc[:,['patid','sysdate']]
    earliest_sysdates.columns = ['patid','data_start']

    logging.debug('finding latest sysdates')
    latest_sysdates = all_entries.sort_values(by='sysdate',ascending=False).groupby('patid').first().reset_index().loc[:,['patid','sysdate']]
    latest_sysdates = latest_sysdates.loc[:,['patid','sysdate']]
    latest_sysdates.columns = ['patid','data_end']

    pt_features = pd.read_csv('data/pt_data/pt_features.csv',delimiter=',')

    logging.debug('merging pt_features with earliest sysdates')
    pt_features = pd.merge(pt_features,earliest_sysdates,how='left')
    logging.debug('merging pt_features with latest sysdates')
    pt_features = pd.merge(pt_features,latest_sysdates,how='left')

    # Remove pts without any sysdates
    logging.debug('removing patients without any events')
    pts_without_any_events = pt_features[pd.isnull(pt_features['data_start'])]
    pts_without_any_events['reason_for_removal']='Pt did not have any events'
    pts_without_any_events.to_csv('data/pt_data/removed_patients/pts_without_any_events.csv',index=False)

    logging.debug('writing all the patients with events to pt_features.csv')
    pt_features = pt_features[pd.notnull(pt_features['data_start'])]
    return pt_features
    # pt_features.to_csv('data/pt_data/pt_features.csv',index=False)

def add_length_of_data_pre_and_post_indexdate_to_pt_features(isCase):
    '''
    Calculates the length of data extracted before and after the index date.
    Requires isCase (i.e. whether pts are cases or controls) as an argument, because until they've been rematched,
    controls don't yet have an index date.
    '''
    pt_features = pd.read_csv('data/pt_data/pt_features.csv',delimiter=',', parse_dates=['index_date','data_start','data_end'], infer_datetime_format=True)

    row_index = pt_features['isCase']==isCase & pd.notnull(pt_features['data_start']) & pd.notnull(pt_features['data_end'])

    pt_features.loc[row_index,'days pre-indexdate'] = ((pt_features['index_date']-pt_features['data_start'])/np.timedelta64(1, 'D'))
    pt_features.loc[row_index,'days post-indexdate'] = ((pt_features['data_end']-pt_features['index_date'])/np.timedelta64(1, 'D'))

    pt_features.to_csv('data/pt_data/pt_features.csv',index=False)

def get_prodcodes_from_drug_name(codelist):
    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv')
    prodcodes = [pegprod.loc[pegprod['drug substance name'].str.contains(med,na=False,case=False)].loc[:,'prodcode'].tolist() for med in codelist]
    # now flatten the list (which contains lists within lists):
    prodcodes = [prodcode for list in prodcodes for prodcode in list]
    return prodcodes

def get_specific_prescription_count_then_add_to_pt_features(drugtype,column_name):
    all_prescriptions = pd.read_csv('data/pt_data/prescriptions.csv',delimiter=',')
    prodcodes = get_prodcodes_from_drug_name(drugtype)
    prescriptions = all_prescriptions[all_prescriptions['prodcode'].isin(prodcodes)][['patid','eventdate','prodcode']]
    prescriptions['eventdate'] = pd.to_datetime(prescriptions['eventdate'],format='%Y-%m-%d',errors='coerce')
    pt_features = pd.read_csv('data/pt_data/pt_features.csv',delimiter=',')
    prescriptions = pd.merge(prescriptions,pt_features, how='left')[['patid','eventdate','prodcode','index_date']]
    prescriptions['index_date']=pd.to_datetime(prescriptions['index_date'],errors='coerce',format='%Y-%m-%d')
    too_close_to_dx_period = timedelta(days=365)*Study_Design.years_between_exposure_measurement_and_index_date
    too_distant_from_dx_period = too_close_to_dx_period + timedelta(days=365)*Study_Design.years_of_exposure_measurement
    not_too_close_to_dx = prescriptions['eventdate']<(prescriptions['index_date']-too_close_to_dx_period)
    not_before_exposure_period = prescriptions['eventdate']>(prescriptions['index_date']-too_distant_from_dx_period)
    relev_prescriptions = prescriptions[not_too_close_to_dx & not_before_exposure_period]
    relev_prescriptions = relev_prescriptions['prodcode'].groupby(relev_prescriptions['patid']).count().reset_index()
    relev_prescriptions.columns=['patid',column_name]
    pt_features=pd.merge(pt_features,relev_prescriptions,how='left')
    pt_features.to_csv('data/pt_data/pt_features.csv',index=False)

def get_medcodes_from_readcodes(readcodes):
    pegmed = pd.read_csv('data/dicts/proc_pegasus_medical.csv')
    medcodes=[pegmed.loc[pegmed['readcode']==readcode,'medcode'].iloc[0] for readcode in readcodes]
    return medcodes

def add_insomnia_event_count_to_pt_features():
    """
    Calculates count of insomnia-months for each patient, and adds it to pt_features dataframe
    """
    # Create list of all insomnia entries, then group it to calculate each patient's insomnia count, broken down by month
    insomnia_medcodes = get_medcodes_from_readcodes(codelists.insomnia_readcodes)
    insom_events = df[df['medcode'].isin(insomnia_medcodes)]
    insom_events=insom_events[pd.notnull(insom_events['eventdate'])] #drops a small number of rows (only about 64) with NaN eventdates
    insom_events=insom_events[['patid','eventdate']].set_index('eventdate').groupby('patid').resample('M').count()
    #convert group_by object back to dataframe
    insom_events = insom_events.add_suffix('_count').reset_index()
    insom_events.columns=['patid','eventdate','insom_count']
    #delete zero counts
    insom_events=insom_events[insom_events['insom_count']>0]

    pt_features = pd.read_csv('data/pt_data/pt_features.csv',delimiter=',')

    # Remove insomnia events for patients who are no longer in study (e.g. because I've removed them for not having any enough data)
    insom_events['pat_in_study'] = insom_events['patid'].map(lambda x: x if any(pt_features.patid==x) else np.nan)

    insom_events=insom_events[pd.notnull(insom_events['pat_in_study'])]
    insom_events['pat_in_study']=insom_events['pat_in_study'].astype(int)

    insom_events['pat_index_date']=np.nan
    insom_events['pat_index_date'] = insom_events['patid'].map(lambda x: pt_features[pt_features['patid']==x]['index_date'].values[0])

    # Restrict insomnia event counts to those that occur during exposure period
    too_close_to_dx_period = timedelta(days=365)*Study_Design.years_between_exposure_measurement_and_index_date
    too_distant_from_dx_period = too_close_to_dx_period + timedelta(days=365)*Study_Design.years_of_exposure_measurement
    not_too_close_to_dx = insom_events['eventdate']<(insom_events['pat_index_date']-too_close_to_dx_period)
    not_before_exposure_period = insom_events['eventdate']>(insom_events['pat_index_date']-too_distant_from_dx_period)
    relev_insom_events = insom_events[not_too_close_to_dx & not_before_exposure_period]

    # Convert groupby object into a dataframe, and rename new column
    relev_insom_events_by_pt = relev_insom_events.groupby(by='patid')['eventdate'].count().reset_index()
    relev_insom_events_by_pt.columns=['patid','insomnia_event_count']

    # merge pt_features with new relev_insomnia_event dataframe
    merged_table = pd.merge(pt_features,relev_insom_events_by_pt, on='patid',how='outer')
    merged_table['insomnia_event_count'].fillna(0,inplace=True)
    merged_table['insomnia_event_count'] = merged_table['insomnia_event_count'].astype(int)

    merged_table.to_csv('data/pt_data/pt_features.csv',index=False)


def clean_matching():
    """
    Removes the 196 rows from the 'matching' dataframe where there is no control matching the case,
    then creates a files called 'unmatched_cases' for the lone cases, and a file called
    'matching_unmatched_removed.csv' for the cleaned up matched pairs
    """
    matching = pd.read_csv('data/pt_data/Matching_File.txt',delimiter='\t',parse_dates=['case_index'],infer_datetime_format=True,dayfirst=True)
    matching_unmatched_removed = matching[matching['control_pracid']!='.']
    matching_unmatched_removed.to_csv('data/pt_data/matching_unmatched_removed.csv',index=False)
    unmatched_cases = matching[matching['control_patid']=='.'][['case_patid','case_pracid','case_gender','case_birthyear','case_index']]
    unmatched_cases.columns=['patid','pracid','gender','birthyear','index_date']
    unmatched_cases['isCase']=True
    unmatched_cases.to_csv('data/pt_data/removed_patients/ummatched_cases.csv',index=False)

def match_cases_and_controls():
    pt_features = pd.read_csv('data/pt_data/pt_features.csv',delimiter=',',parse_dates=['index_date','data_start','data_end'])

    pt_features['matchid']=np.nan
    pt_features.sort_values(inplace=True,by='days_pre_indexdate',ascending=True) # To make matching more efficient, first try to match to controls the cases with with the LEAST amount of available data

    count=0
    for index,row in pt_features.iterrows():
        if(row['isCase']==True):
            if pd.isnull(row['matchid']):
                patid = row['patid']
                birthyear = row['birthyear']
                gender = row['gender']
                pracid = row['pracid']
                index_date = row['index_date']
                # Define matching criteria
                matches_birthyear = pt_features['birthyear']==birthyear
                matches_gender = pt_features['gender']==gender
                is_control = pt_features['isCase'] == False
                matches_practice = pt_features['pracid']==pracid
                is_not_already_matched = pd.isnull(pt_features['matchid'])
                enough_data_after_index_date = pt_features['data_start'] <= (index_date - timedelta(days=(365*Study_Design.total_years_required_pre_index_date)))
                enough_data_before_index_date = pt_features['data_end'] >= (index_date + timedelta(days=(365*Study_Design.years_of_data_after_index_date_required_by_controls)))
                matching_pt = pt_features[enough_data_before_index_date & enough_data_after_index_date & matches_birthyear & matches_gender & matches_practice & is_control & is_not_already_matched]
                # To make matching more efficient, first try to match cases with those controls with the LEAST amount of available data
                matching_pt['total_available_data']= pt_features['data_end'] - pt_features['data_start']
                matching_pt = matching_pt.sort_values(by='total_available_data',ascending=True).head(1)
                if len(matching_pt)>0:
                    matching_pt = pt_features[pt_features['patid'] == matching_pt['patid'].values[0]]
                    #give both the case and control a unique match ID (for convenience, I've used the iterrows index)
                    # matching_pt_id = matching_pt['patid'].values[0]
                    # if pd.notnull(matching_pt_id):
                    row['matchid']=index
                    # matching_pt_mask = pt_features['patid']==matching_pt_id
                    # pt_features.loc[index,'matchid']=index
                    # pt_features.loc[matching_pt_mask,'matchid']=index
                    # pt_features.loc[matching_pt_mask,'index_date']=index_date
                    matching_pt['matchid']=index
                    matching_pt['index_date']=index_date
                    count += 1
                    logging.debug('Matched {0} with {1}.'.format(patid,matching_pt['patid']))
                else:
                    logging.debug('No match found for ',patid)
        if count>100:
            pt_features.to_csv('data/pt_data/pt_features.csv',index=False)
            count=0

def delete_unmatched_controls():
    pt_features = pd.read_csv('data/pt_data/pt_features.csv',delimiter=',',parse_dates=['index_date','data_start','data_end'])
    removed_pts = pt_features[pd.isnull(pt_features['matchid'])]
    removed_pts['reason_for_removal']='Sent by CPRD to us unmatched'
    removed_pts.to_csv('data/pt_data/removed_patients/removed_unmatched_patients.csv',index=False)
    pt_features = pt_features[pd.notnull(pt_features['matchid'])]
    pt_features.to_csv('data/pt_data/pt_features.csv',index=False)

def delete_patients_if_not_enough_data(isCase):
    pt_features = pd.read_csv('data/pt_data/pt_features.csv',delimiter=',')
    del_index = (pt_features['days_pre_indexdate']<(Study_Design.total_years_required_pre_index_date*365)) \
            | (pt_features['days_post_indexdate']<(Study_Design.years_of_data_after_index_date_required_by_controls*365))
    del_index = del_index & (pt_features['isCase']==isCase)
    #delete cases and controls if not enough data prior to index dates
    pd.options.mode.chained_assignment = None  # default='warn'
    removed_pts = pt_features.loc[del_index]
    removed_pts['reason_for_removal']='Not enough available data prior or post index date'
    removed_pts.to_csv('data/pt_data/removed_patients/removed_pts_with_not_enough_data.csv',mode='a',index=False)

    pt_features=pt_features.loc[del_index == False]
    pt_features.to_csv('data/pt_data/pt_features.csv',index=False)


def create_pegmed():
    """
    Creates a cleaned up version of Pegasus Medical dictionary in csv form
    """
    pegmed = pd.read_csv('data/dicts/raw_pegasus_medical.txt',delimiter='\t',skiprows=[0,1,2],header=None)
    pegmed.columns=['medcode','readcode','clinical events','immunisation events','referral events','test events','read term','database build']
    pegmed.to_csv('data/dicts/proc_pegasus_medical.csv',index=False)

def create_pegprod():
    """
    Creates a cleaned up version of Pegasus Products dictionary in csv form
    """
    pegprod = pd.read_csv('data/dicts/raw_pegasus_product.txt',delimiter='\t',encoding='latin-1', skiprows=[0,1],header=None)
    pegprod.columns=['prodcode','XXX code','therapy events','product name','drug substance name','substance strength','formulation','route','BNF code','BNF header','database build','unknown column']
    pegprod.to_csv('data/dicts/proc_pegasus_prod.csv',index=False)

def create_specific_prescriptions(all_prescriptions,medlist,csv_name):
    #First get the drug product info from Pegasus
    pegprod = pd.read_csv('data/dicts/proc_pegasus_prod.csv', delimiter=',')
    pegprod['drug substance name'].fillna('',inplace=True)
    specific_pegprod = pegprod[pegprod['drug substance name'].str.contains('|'.join(medlist), case=False)]
    specific_pegprod=specific_pegprod[['prodcode', 'product name','drug substance name','substance strength', 'formulation','route']]

    #Select only relevant drugs from the list of all our sample's prescriptions
    relevant_prescriptions=all_prescriptions[all_prescriptions['prodcode'].isin(specific_pegprod['prodcode'])]

    #Now merge the relevant prescriptions with the Pegasus drug product info
    all_info = pd.merge(relevant_prescriptions,specific_pegprod,how='inner')
    all_info.to_csv('data/medlists/'+csv_name,index=False)

def create_prescriptions():
    logging.debug(entry_type['prescription'])
    logging.debug('reading presc1')
    presc1 = pd.read_csv('data/pt_data/raw_data/Extract_Therapy_001.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','prodcode','qty','ndd','numdays','numpacks','packtype','issueseq'])
    logging.debug('reading presc2')
    presc2 = pd.read_csv('data/pt_data/raw_data/Extract_Therapy_002.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','prodcode','qty','ndd','numdays','numpacks','packtype','issueseq'])
    logging.debug('concatenating')
    prescriptions = pd.concat([presc1,presc2])
    logging.debug('converting eventdate to datetime')
    prescriptions['eventdate'] = pd.to_datetime(prescriptions['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    logging.debug('converting sysdate to datetime')
    prescriptions['sysdate'] = pd.to_datetime(prescriptions['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    prescriptions['type']=entry_type['prescription']
    logging.debug('writing to csv')
    prescriptions.to_csv('data/pt_data/prescriptions.csv',index=False)

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
    clin1 = pd.read_csv('data/pt_data/raw_data/Extract_Clinical_001.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    #logging.debug('processing clinical - reading clin2')
    clin2 = pd.read_csv('data/pt_data/raw_data/Extract_Clinical_002.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    #logging.debug('processing clinical - concatenating')
    clinical = pd.concat([clin1,clin2])
    clinical['type']=entry_type['clinical']
    #logging.debug('processing clinical - converting to datetime - eventdate')
    clinical['eventdate'] = pd.to_datetime(clinical['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('processing clinical - converting to datetime - sysdate')
    clinical['sysdate'] = pd.to_datetime(clinical['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)

    #logging.debug('processing tests')
    test1 = pd.read_csv('data/pt_data/raw_data/Extract_Test_001.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    test2 = pd.read_csv('data/pt_data/raw_data/Extract_Test_002.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    #logging.debug('processing test - concatenating')
    test = pd.concat([test1,test2])
    test['type']=entry_type['test']
    #logging.debug('processing test - converting to datetime - eventdate')
    test['eventdate'] = pd.to_datetime(test['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('processing test - converting to datetime - sysdate')
    test['sysdate'] = pd.to_datetime(test['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)

    #logging.debug('processing referrals')
    referral = pd.read_csv('data/pt_data/raw_data/Extract_Referral_001.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    referral['type']=entry_type['referral']
    #logging.debug('processing referrals - converting to datetime - eventdate')
    referral['eventdate'] = pd.to_datetime(referral['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('processing referrals - converting to datetime - sysdate')
    referral['sysdate'] = pd.to_datetime(referral['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)

    #logging.debug('processing immunisations')
    immunisations = pd.read_csv('data/pt_data/raw_data/Extract_Immunisation_001.txt',delimiter='\t',usecols=['patid','sysdate','eventdate','medcode'])
    immunisations['type']=entry_type['immunisation']
    #logging.debug('processing immunisations - converting to datetime - eventdate')
    immunisations['eventdate'] = pd.to_datetime(immunisations['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('processing  immunisations - converting to datetime - sysdate')
    immunisations['sysdate'] = pd.to_datetime(immunisations['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)

    #logging.debug('concatenating the different entry types')
    medcoded_entries = pd.concat([clinical,test,referral,immunisations])

    #logging.debug('writing to csv')
    medcoded_entries.to_csv('data/pt_data/medcoded_entries.csv',index=False)

def create_consultations():
    """
    Creates a csv file containing all the data from Extract_Consultation_001.txt and Extract_Consultation_002.txt
    """
    #logging.debug('reading Extract_Consultation_001.txt')
    cons1 = pd.read_csv('data/pt_data/raw_data/Extract_Consultation_001.txt',delimiter='\t')
    #logging.debug('reading Extract_Consultation_002.txt')
    cons2 = pd.read_csv('data/pt_data/raw_data/Extract_Consultation_002.txt',delimiter='\t')
    #logging.debug('concatenating')
    consultations = pd.concat([cons1,cons2])[['patid','sysdate','eventdate']]
    #logging.debug('converting to datetime - eventdate')
    consultations['eventdate'] = pd.to_datetime(consultations['eventdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('converting to datetime - sysdate')
    consultations['sysdate'] = pd.to_datetime(consultations['sysdate'],dayfirst=True,errors='coerce', infer_datetime_format=True)
    #logging.debug('adding type column')
    consultations['type']= entry_type['consultation']
    #logging.debug('writing to csv')
    consultations.to_csv('data/pt_data/consultations.csv',index=False)

def create_all_entries():
    """
    Creates a csv file (all_entries.csv) containing all entries (consultations, prescriptions, clinicals, tests, referrals)
    """
    #logging.debug('reading consultations')
    consultations = pd.read_csv('data/pt_data/consultations.csv',delimiter=',')
    #logging.debug('reading medcoded entries')
    medcoded_entries = pd.read_csv('data/pt_data/medcoded_entries.csv',delimiter=',')
    #logging.debug('reading prescriptions')
    prescriptions = pd.read_csv('data/pt_data/prescriptions.csv',delimiter=',',usecols=['patid','eventdate','sysdate','prodcode','type'])
    #logging.debug('concatenating...')
    all_entries = pd.concat([consultations,medcoded_entries,prescriptions],ignore_index=True)
    #logging.debug('writing to file...')
    all_entries.to_csv('data/pt_data/all_entries.csv',index=False)
