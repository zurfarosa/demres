entry_type = {
    'consultation':0,
    'referral':1,
    'clinical':2,
    'test':3,
    'immunisation':4,
    'prescription':5
}
#
# class Entry_Type:
#     consultation = 0
#     referral = 1
#     clinical = 2
#     test = 3
#     immunisation = 4
#     prescription = 5
#     look_up = {consultation:'consultation',referral:'referral',clinical:'clinical',test:'test',immunisation:'immunisation',prescription:'prescription'}

class Study_Design:
    years_between_exposure_measurement_and_index_date = 10
    years_of_exposure_measurement = 5
    total_years_required_pre_index_date = years_of_exposure_measurement + years_of_exposure_measurement
    years_of_data_after_index_date_required_by_controls = 2 #allows us to check to see if they were later diagnosed with dementia
