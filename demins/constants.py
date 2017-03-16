class Study_Design:
    years_between_end_of_exposure_period_and_index_date = 5
    duration_of_exposure_measurement = 5
    total_years_required_pre_index_date = duration_of_exposure_measurement + years_between_end_of_exposure_period_and_index_date
    years_of_data_after_index_date_required_by_controls = 2 #allows us to check to see if they were later diagnosed with dementia
    acceptable_number_of_registration_gap_days = 0 # Number of missing days (due to not being registered at surgery) considered acceptable per patient
