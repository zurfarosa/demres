from datetime import date, timedelta

class Study_Design:
    req_yrs_post_index = 1 #allows us to check to see if they were later diagnosed with dementia
    acceptable_number_of_registration_gap_days = 0 # Number of missing days (due to not being registered at surgery) considered acceptable per patient
    window_length_in_years = 5

    exposure_windows = [
        {'name':'12_to_7','start_year':-12},
        {'name':'10_to_5','start_year':-10},
        {'name':'8_to_3','start_year':-8}
    ]
