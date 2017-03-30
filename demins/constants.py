from datetime import date, timedelta

class Study_Design:
    years_of_data_after_index_date_required_by_controls = 2 #allows us to check to see if they were later diagnosed with dementia
    acceptable_number_of_registration_gap_days = 0 # Number of missing days (due to not being registered at surgery) considered acceptable per patient
    window_length_in_years = 5
    years_between_last_window_and_index_date = 0
    number_of_windows = 2
    total_years_required_pre_index_date = (window_length_in_years * number_of_windows) + years_between_last_window_and_index_date
