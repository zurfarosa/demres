class Constants:
    exposure_start = 5 #minimum years prior to index date that insomnia episodes are counted as exposure
    exposure_end = 10 #maximum years prior to index date that insomnia episodes are counted as exposure

class Entry_Type:
    consultation = 0
    referral = 1
    clinical = 2
    test = 3
    look_up = {consultation:'consultation',referral:'referral',clinical:'clinical',test:'test'}
