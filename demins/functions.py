def get_insomnia_event_count(entries=None):
    """
    Calculates count of insomnia-months for each patient, and adds it to pt_features dataframe
    Can receive an optional all_entries or medcoded_entries dataframe as an argument
    """
    # Create list of all insomnia entries, then group it to calculate each patient's insomnia count, broken down by month
    if entries is None:
        entries = pd.read_csv('data/pt_data/medcoded_entries.csv',delimiter=',',parse_dates=['eventdate'],infer_datetime_format=True)
    insomnia_medcodes = get_medcodes_from_readcodes(codelists.insomnia_readcodes)
    insom_events = entries[entries['medcode'].isin(insomnia_medcodes)]
    insom_events = insom_events[pd.notnull(insom_events['eventdate'])] #drops a small number of rows (only about 64) with NaN eventdates
    insom_events = insom_events[['patid','eventdate']].set_index('eventdate').groupby('patid').resample('M').count()
    #convert group_by object back to dataframe
    insom_events = insom_events.add_suffix('_count').reset_index()
    insom_events.columns=['patid','eventdate','insom_count']
    #delete zero counts
    insom_events = insom_events[insom_events['insom_count']>0]
    # Remove insomnia events for patients who are no longer in study (e.g. because I've removed them for not having any enough data)
    pt_features = pd.read_csv('data/pt_data/pt_features.csv',delimiter=',',parse_dates=['index_date'],infer_datetime_format=True)
    insom_events = pd.merge(insom_events,pt_features,how='inner')[['patid','eventdate','insom_count','index_date']]
    # Restrict insomnia event counts to those that occur during exposure period
    interim_period = timedelta(days=365)*Study_Design.years_between_end_of_exposure_period_and_index_date
    relevant_event_mask = (insom_events['eventdate']<=(insom_events['index_date']-interim_period)) & (insom_events['eventdate']>=(insom_events['index_date']-timedelta(days=365)*Study_Design.total_years_required_pre_index_date))
    insom_events = insom_events.loc[relevant_event_mask]
    insom_events = insom_events.groupby('patid')['insom_count'].count().reset_index()
    # merge pt_features with new insomnia_event dataframe
    pt_features = pd.merge(pt_features,insom_events,how='left')
    pt_features['insom_count'].fillna(0,inplace=True)
    pt_features['insom_count'] = pt_features['insom_count'].astype(int)

    # return pt_features
    pt_features.to_csv(ROOT_DIR + '/data/pt_data/pt_features.csv',index=False)
