import os
import sys

import pandas as pd
import numpy as np
from datetime import date, timedelta
from scipy.stats import chi2_contingency
import statsmodels.api as sm
from statsmodels.tools.tools import add_constant
from scipy import stats
# import pylab as pl


import demres
from demres.common.constants import entry_type
from demres.common import codelists
from demres.common.helper_functions import *
import statsmodels.api as sm
from pprint import pprint


def convert_final_dementia_dx_from_medcode_to_readcode(pt_features):
    pegmed = pd.read_csv('dicts/proc_pegasus_medical.csv')
    just_dementia_diagnoses = pt_features[pd.notnull(pt_features['final dementia medcode'])].copy()
    just_dementia_diagnoses['final dementia Readcode'] = (just_dementia_diagnoses['final dementia medcode'].map(lambda x: pegmed.loc[pegmed['medcode']==x,'readcode'].item()))
    pt_features = pd.merge(pt_features,just_dementia_diagnoses,how='left')
    return pt_features

def add_final_dementia_medcode_dummies(pt_features):
    '''
    Adds dummy columns for final_dementia_medcode (i.e. our best guess at the dementia subtype) to be used as baseline characteristics
    '''
    just_dementia_diagnoses = pt_features[pd.notnull(pt_features['final dementia Readcode'])].copy()

    just_dementia_diagnoses['final dementia group'] = just_dementia_diagnoses['final dementia Readcode'].map(lambda x: codelists.alzheimer_vascular_and_non_specific_dementias['subtype_groupings'][x])
    pt_features = pd.merge(pt_features,just_dementia_diagnoses,how='left')

    # if isCase is True but there is no final dementia Readcode, classify them as Alzheimers (because these are the patients who were diagnosed with dementia based on antidementia medication)
    pt_features.loc[(pd.isnull(pt_features['final dementia Readcode']))&(pt_features['isCase']==True),'final dementia group'] = 'Alzheimers'
    # pts_diagnosed_on_basis_of_antidementia_meds_only['final dementia group'] = 'Alzheimers'
    # display(pts_diagnosed_on_basis_of_antidementia_meds_only)
    # pt_features = pd.merge(pt_features,pts_diagnosed_on_basis_of_antidementia_meds_only,how='left')

    pt_features = pd.get_dummies(pt_features,columns=['final dementia group'],prefix='dx')
    return pt_features


def add_baseline_characteristics(variables,pt_features):
    baseline_dichot = pd.DataFrame(columns=['Cases','Controls'])
    all_cases = pt_features.loc[pt_features['isCase']==True]
    all_controls = pt_features.loc[pt_features['isCase']==False]
    for variable in variables:
        if set(pt_features[variable]) in [{0,1},{0}]: #if it is a boolean 1 or 0 variable
            positive_cases = pt_features.loc[(pt_features[variable]==1)&(pt_features['isCase']==1)]
            negative_cases = pt_features.loc[(pt_features[variable]==0)&(pt_features['isCase']==1)]
            positive_controls = pt_features.loc[(pt_features[variable]==1)&(pt_features['isCase']==0)]
            negative_controls = pt_features.loc[(pt_features[variable]==0)&(pt_features['isCase']==0)]
            baseline_dichot.loc[variable,'Cases'] = "{0:.0f} ({1:.1%})".format(len(positive_cases),len(positive_cases)/len(all_cases))
            baseline_dichot.loc[variable,'Controls'] = "{0:.0f} ({1:.1%})".format(len(positive_controls),len(positive_controls)/len(all_controls))
            # if (len(positive_cases)>0) & (len(negative_cases)>0):
            #     obs = np.array([[len(positive_cases),len(negative_cases)],[len(positive_controls),len(negative_controls)]])
            #     chi2, p, dof, ex = chi2_contingency(obs, correction=False)
            #     # baseline_dichot.loc[variable,'P value'] =  "{0:.3f}".format(p)
            # else:
            #     # baseline_dichot.loc[variable,'P value'] =  '-'
    return baseline_dichot

def calculate_univariate_and_multivariate_ORs(pt_features,covariates,main_variables):
    '''
    '''
    starting_covariates = remove_covariates_causing_maximum_likelihood_error(pt_features, covariates)


    univariate_results = pd.DataFrame(columns=['Univariate OR','[0.025','0.975]','p value'])

    for covariate in sorted(starting_covariates):
        logit = sm.Logit(pt_features['isCase'], pt_features[covariate])
        result = logit.fit(disp=0,maxiter=500)
        OR = np.exp(result.params).astype(float)
        p_value = result.pvalues.astype(float)
        conf_ints = np.exp(result.conf_int())

        univariate_results.loc[covariate] = [OR.values[0],conf_ints.values[0][0],conf_ints.values[0][1],p_value.values[0]]

    # Calculate multivariate results
    logit = sm.Logit(pt_features['isCase'], pt_features[list(univariate_results.index)])
    result = logit.fit(disp=0,maxiter=500)
    multivariate_results = pd.concat([np.exp(result.params),result.pvalues],axis=1)
    multivariate_results = pd.concat([np.exp(result.params),np.exp(result.conf_int()),result.pvalues],axis=1)
    multivariate_results.columns=['Multivariate OR','multi [0.025','multi 0.975]','multi p value']
    multivariate_results.sort_index(inplace=True)

    univariate_and_multivariate_results = pd.concat([univariate_results,multivariate_results],axis=1,join_axes=[multivariate_results.index])

    univariate_and_multivariate_results_formatted = pd.DataFrame(columns=['Univariate OR', 'Multivariate OR'])
    univariate_and_multivariate_results_formatted['Univariate OR']=univariate_and_multivariate_results['Univariate OR'].map(lambda x: "{:.2f},".format(x)) + ' ('+  univariate_and_multivariate_results['[0.025'].map(lambda x: "{:.2f}".format(x)) + ', ' + univariate_and_multivariate_results['0.975]'].map(lambda x: "{:.2f})".format(x)) + ', P=' + univariate_and_multivariate_results['p value'].map(lambda x: "{:.3f}".format(x))
    univariate_and_multivariate_results_formatted['Multivariate OR']=univariate_and_multivariate_results['Multivariate OR'].map(lambda x: "{:.2f},".format(x)) + ' ('+  univariate_and_multivariate_results['multi [0.025'].map(lambda x: "{:.2f}".format(x)) + ', ' + univariate_and_multivariate_results['multi 0.975]'].map(lambda x: "{:.2f})".format(x)) + ', P=' + univariate_and_multivariate_results['p value'].map(lambda x: "{:.3f}".format(x))
    new_index = [row.capitalize().replace('_',' ').replace('100 pdds','(100 PDDs)').replace('gp','GP').replace('Non ','Non-').replace('Benzo and z drugs','Benzodiazepines and z-drugs') for row in univariate_and_multivariate_results_formatted.index]
    univariate_and_multivariate_results_formatted.index = new_index


    summary_table = result.summary().tables[0]



    return summary_table,univariate_and_multivariate_results_formatted

def remove_covariates_causing_maximum_likelihood_error(pt_features,training_cols):
    filtered_training_cols = []
    for col in training_cols:
        if pt_features[col].mean()>0: #prevents singular matrix warning
            # print(col,' being retained as mean > 0')
            filtered_training_cols.append(col)
        else:
            print(col, ' being removed as mean == 0')
    return filtered_training_cols
