import os
import sys

import pandas as pd
import numpy as np
from datetime import date, timedelta

import demres
from demres.common.constants import entry_type
from demres.common import codelists
from demres.common.helper_functions import *
import statsmodels.api as sm
from pprint import pprint


def get_univariate_and_multivariate_results(pt_features,training_cols):
    #first convert booleans to 1 or 0; and do not include columns where the mean value (if continuous) is 0
    temp = []
    for col in training_cols:
        pt_features[col] = pt_features[col].astype(int)
        if pt_features[col].mean()>0.03: #arbitary number which seems to prevent 'Maximum Likelihood optimization failed to converge' warnings
            temp.append(col)
            # print(col, pt_features[col].mean())
    training_cols = temp

    # get univariate results
    univariate_results = pd.DataFrame(columns=['odds_ratio','p_value'])
    for col in training_cols:
        logit = sm.Logit(pt_features['isCase'], pt_features[col])
        result = logit.fit(disp=0,maxiter=500)
        OR = round(np.exp(result.params).astype(float),4)
        p_value = round(result.pvalues.astype(float),3)
        univariate_results.loc[col] = [OR.values[0],p_value.values[0]]

    # get multivariate results
    logit = sm.Logit(pt_features['isCase'], pt_features[training_cols])
    result = logit.fit()
    multivariate_results = pd.concat([round(np.exp(result.params),4),round(result.pvalues,3)],axis=1)
    multivariate_results.columns=['odds_ratio','p_value']
    multivariate_summary = result.summary()

    return univariate_results, multivariate_results, multivariate_summary
