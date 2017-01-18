class Entry_Type:
    consultation = 0
    referral = 1
    clinical = 2
    test = 3
    look_up = {consultation:'consultation',referral:'referral',clinical:'clinical',test:'test'}

class Study_Design:
    years_between_exposure_measurement_and_index_date = 5
    years_of_exposure_measurement = 5
    total_years_required_pre_index_date = years_of_exposure_measurement + years_of_exposure_measurement
