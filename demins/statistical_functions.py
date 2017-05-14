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


def purposefully_select_covariates(pt_features,covariates,main_variable):
    '''
    Selects covariates to keep in final model.
    Based on a model-building technique described here: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2633005/.
    '''
    starting_covariates = remove_covariates_causing_maximum_likelihood_error(pt_features, covariates)

    #stage 1 - remove covariates with univariate p value of >0.25

    univariate_results = pd.DataFrame(columns=['odds_ratio','p_value'])
    for covariate in starting_covariates:
        logit = sm.Logit(pt_features['isCase'], pt_features[covariate])
        result = logit.fit(disp=0)
        OR = round(np.exp(result.params).astype(float),4)
        p_value = round(result.pvalues.astype(float),3)
        univariate_results.loc[covariate] = [OR.values[0],p_value.values[0]]

    stage_1_selection_mask = (univariate_results['p_value']<=0.25)|(univariate_results.index==main_variable)|(univariate_results.index=='intercept')
    stage_1_selected_covariates = univariate_results.loc[stage_1_selection_mask]
    stage_1_unwanted_covariates = univariate_results.loc[~stage_1_selection_mask]

    print('*Stage 1*\nUnivariate results')
    print(univariate_results)
    print('\nThe following covariates were retained during stage 1:\n')
    print(list(stage_1_selected_covariates.index))
    print('\nThe following covariates were NOT retained during stage 1, as p value > 0.25:\n')
    print(list(stage_1_unwanted_covariates.index))

    #stage 2 - remove covariates from multivariable model if p value of >0.1

    logit = sm.Logit(pt_features['isCase'], pt_features[list(stage_1_selected_covariates.index)])
    result = logit.fit(disp=0)
    multivariate_results = pd.concat([round(np.exp(result.params),4),round(result.pvalues,3)],axis=1)
    multivariate_results.columns=['odds_ratio','p_value']

    stage_2_selection_mask=(multivariate_results['p_value']<0.1)|(multivariate_results.index==main_variable)|(multivariate_results.index=='insomnia_consultations')
    stage_2_selected_covariates = multivariate_results.loc[stage_2_selection_mask]
    stage_2_unwanted_covariates = multivariate_results.loc[~stage_2_selection_mask]

    print('\n\n*Stage 2\nmultivariate_results (using just the covariates selected in stage 1):')
    print(multivariate_results)
    print('\nThe following covariates were retained during stage 2:\n',list(stage_2_selected_covariates.index))
    print('\nThe following covariates NOT were retained during stage 2, as p value > 0.1:\n',list(stage_2_unwanted_covariates.index),'\n\n')
    # multivariate_results.columns=['odds_ratio','p_value']
    # multivariate_summary = result.summary()

    #stage 3 - test if the unwanted covariates from the previous stage, when added back in,
    # lead to a 15% change in any remaining OR - if so, we still want them

    stage3_selected_covariates = list(stage_2_selected_covariates.index)
    stage3_unwanted_covariates = []
    print('*Stage 3*')
    for covariate in stage_2_unwanted_covariates.index:
        print('\nStage 2 multivariate analysis repeated, but without',covariate,'\n')
        stage_1_selected_covariates_with_one_removed = list(stage_1_selected_covariates.index)
        stage_1_selected_covariates_with_one_removed.remove(covariate)
        # print(stage_1_selected_covariates_with_one_removed)
        logit = sm.Logit(pt_features['isCase'], pt_features[stage_1_selected_covariates_with_one_removed])
        result = logit.fit(disp=0)
        one_removed_results = pd.concat([round(np.exp(result.params),4),round(result.pvalues,3)],axis=1)
        one_removed_results.columns=['OR_1_removed','p_value']
        # print(one_removed_results)
        concat_results = (pd.concat([multivariate_results['odds_ratio'],one_removed_results['OR_1_removed']],axis=1))
        concat_results['change_in_OR']=abs(concat_results['odds_ratio']-concat_results['OR_1_removed'])/concat_results['odds_ratio']
        print(concat_results)
        print('\nmax change in OR: ',concat_results['change_in_OR'].max())
        if concat_results['change_in_OR'].max() >= 0.15:
            print('{0} has a large confounding effect, therefore to be retained in model'.format(covariate))
            stage3_selected_covariates.append(covariate)
        else:
            print('{0} does not have a large confounding effect, so will not be retained in model'.format(covariate))
            stage3_unwanted_covariates.append(covariate)

    #stage 4 - Add in the covariates removed from the stage 1 model one by one - keep them if p<0.15
    print('\n\n*Stage 4*')

    print('\nAdd in the covariates removed from the stage 1 model one by one - keep them if p<0.15:')
    for covariate in stage_1_unwanted_covariates.index:
        stage3_selected_covariates.append(covariate)
        print('\nCovariate being added:',covariate)
        logit = sm.Logit(pt_features['isCase'], pt_features[stage3_selected_covariates])
        result = logit.fit(disp=0)
        multivariate_results = pd.concat([round(np.exp(result.params),4),round(result.pvalues,3)],axis=1)
        multivariate_results.columns=['odds_ratio','p_value']
        print(multivariate_results)
        p_value = multivariate_results.loc[covariate,'p_value']
        if p_value<0.1:
            print('\n{0} is being added to selected covariates, as p_value is {1}'.format(covariate,p_value))
        else:
            print('\n{0} is being removed, as p_value is {1}'.format(covariate,p_value))
            stage3_selected_covariates.remove(covariate)

    print('Final list of covariates:\n',stage3_selected_covariates)

    print('***Final multivariate analysis***\n')
    logit = sm.Logit(pt_features['isCase'], pt_features[stage3_selected_covariates])
    result = logit.fit(disp=0)
    multivariate_results = pd.concat([round(np.exp(result.params),4),round(result.pvalues,3)],axis=1)
    multivariate_results.columns=['odds_ratio','p_value']
    print(multivariate_results)

    result_df = pd.DataFrame(columns=['OR','coef','p','[0.025','0.975]'],index=result.pvalues.index)
    result_df['p']= result.pvalues
    result_df[['[0.025','0.975]']]=result.conf_int()
    result_df['OR']= np.exp(result.params)
    result_df['coef']= result.params

    summary_table = result.summary().tables[0]

    return summary_table,result_df


def remove_covariates_causing_maximum_likelihood_error(pt_features,training_cols):
    filtered_training_cols = []
    for col in training_cols:
        # pt_features[col] = pt_features[col].astype(int)
        if pt_features[col].mean()>0.01: #arbitary number which seems to prevent 'Maximum Likelihood optimization failed to converge' warnings
            filtered_training_cols.append(col)
            # print(col, pt_features[col].mean())
    return filtered_training_cols

def get_univariate_and_multivariate_results(pt_features,training_cols):
    #first convert booleans to 1 or 0; and do not include columns where the mean value (if continuous) is 0
    training_cols = remove_covariates_causing_maximum_likelihood_error(pt_features,training_cols)
    # get univariate results
    univariate_results = pd.DataFrame(columns=['odds_ratio','p_value'])
    for covariate in training_cols:
        logit = sm.Logit(pt_features['isCase'], pt_features[covariate])
        result = logit.fit(disp=0,maxiter=500)
        OR = round(np.exp(result.params).astype(float),4)
        p_value = round(result.pvalues.astype(float),3)
        univariate_results.loc[covariate] = [OR.values[0],p_value.values[0]]

    # get multivariate results
    logit = sm.Logit(pt_features['isCase'], pt_features[training_cols])
    result = logit.fit()
    multivariate_results = pd.concat([round(np.exp(result.params),4),round(result.pvalues,3)],axis=1)
    multivariate_results.columns=['odds_ratio','p_value']
    multivariate_summary = result.summary()

    return univariate_results, multivariate_results, multivariate_summary
