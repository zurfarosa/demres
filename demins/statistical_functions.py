import os
import sys

import pandas as pd
import numpy as np
from datetime import date, timedelta
from scipy.stats import chi2_contingency
import statsmodels.api as sm
from statsmodels.tools.tools import add_constant
from scipy import stats
import pylab as pl


import demres
from demres.common.constants import entry_type
from demres.common import codelists
from demres.common.helper_functions import *
import statsmodels.api as sm
from pprint import pprint


def get_IQR(x):
    q75, q25 = np.percentile(x, [75 ,25])
    iqr = '{0} - {1}'.format(str(q25),str(q75))
    return iqr


def add_baseline_characteristics(baseline_df,variables,pt_features):
    baseline_contin = pd.DataFrame(columns=['Cases - mean','Cases - median','Cases - IQR','Controls - mean','Controls - median','Controls - IQR','P value'])
    baseline_dichot = pd.DataFrame(columns=['Cases','Controls','P value'])
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
            if (len(positive_cases)>0) & (len(negative_cases)>0):
                obs = np.array([[len(positive_cases),len(negative_cases)],[len(positive_controls),len(negative_controls)]])
                chi2, p, dof, ex = chi2_contingency(obs, correction=False)
                baseline_dichot.loc[variable,'P value'] =  "{0:.3f}".format(p)
            else:
                baseline_dichot.loc[variable,'P value'] =  '-'
        else: #if it is a continuous variable
            cases = pt_features.loc[pt_features['isCase']==1,variable].values
            controls = pt_features.loc[pt_features['isCase']==0,variable].values
            baseline_contin.loc[variable,'Cases - mean'] = "{0:.2f}".format(np.mean(cases))
            baseline_contin.loc[variable,'Cases - median'] = "{0:.2f}".format(np.median(cases))
            baseline_contin.loc[variable,'Cases - IQR'] = get_IQR(cases)
            baseline_contin.loc[variable,'Controls - median'] = "{0:.2f}".format(np.median(controls))
            baseline_contin.loc[variable,'Controls - mean'] = "{0:.2f}".format(np.mean(controls))
            baseline_contin.loc[variable,'Controls - IQR'] = get_IQR(controls)
            t_stat,p = stats.ttest_ind(cases,controls)
            baseline_contin.loc[variable,'P value'] = "{0:.3f}".format(p)
    return baseline_dichot.sort_index(),baseline_contin

def purposefully_select_covariates(pt_features,covariates,main_variables):
    '''
    Selects covariates to keep in final model.
    Based on a model-building technique described here: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2633005/.
    '''
    starting_covariates = remove_covariates_causing_maximum_likelihood_error(pt_features, covariates)

    #stage 1 - remove covariates with univariate p value of >0.25

    univariate_results = pd.DataFrame(columns=['Univariate OR','p value','[0.025','0.975]'])

    for covariate in sorted(starting_covariates):
        logit = sm.Logit(pt_features['isCase'], pt_features[covariate])
        result = logit.fit(disp=0,maxiter=500)
        OR = round(np.exp(result.params).astype(float),3)
        p_value = round(result.pvalues.astype(float),3)
        conf_ints = np.round(np.exp(result.conf_int()),3)

        univariate_results.loc[covariate] = [OR.values[0],p_value.values[0],conf_ints.values[0][0],conf_ints.values[0][1]]

    stage_1_selection_mask = (univariate_results['p value']<=0.25)|(univariate_results.index.isin(main_variables))|(univariate_results.index=='intercept')
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
    result = logit.fit(disp=0,maxiter=500)
    multivariate_results = pd.concat([round(np.exp(result.params),4),round(result.pvalues,3)],axis=1)
    multivariate_results.columns=['odds_ratio','p_value']

    stage_2_selection_mask=(multivariate_results['p_value']<0.1)|(multivariate_results.index.isin(main_variables))
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
        result = logit.fit(disp=0,maxiter=500)
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
        result = logit.fit(disp=0,maxiter=500)
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
    result = logit.fit(disp=0,maxiter=500)
    multivariate_results = pd.concat([round(np.exp(result.params),3),round(result.pvalues,3),np.round(np.exp(result.conf_int()),3)],axis=1)
    multivariate_results.columns=['Multivariate OR','p value','[0.025','0.975]']
    multivariate_results.sort_index(inplace=True)
    print(multivariate_results)

    univariate_and_multivariate_results = pd.concat([univariate_results,multivariate_results],axis=1,join_axes=[multivariate_results.index])
    summary_table = result.summary().tables[0]

    return summary_table,univariate_and_multivariate_results


def remove_covariates_causing_maximum_likelihood_error(pt_features,training_cols):
    filtered_training_cols = []
    for col in training_cols:
        if pt_features[col].mean()>0: #prevents singular matrix warning
            print(col,' being retained as mean < 0')
            filtered_training_cols.append(col)
            # print(col, pt_features[col].mean())
        else:
            print(col, ' being removed as mean = 0')
    print('\n')
    return filtered_training_cols
