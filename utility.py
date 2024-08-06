import numpy as np
import scipy.stats as stats
import math
from spearman import spearman_critical_values

def pearson_critical_value(alpha, df):
    # Calculate the critical value for the t-distribution
    t_critical = stats.t.ppf(1 - alpha / 2, df)
    
    # Convert t-value to Pearson correlation coefficient
    r_critical = np.sqrt(t_critical ** 2 / (t_critical ** 2 + df))
    
    return r_critical

def mean_conformity_Z_test(sample_mean, test_value, standard_deviation, sample_size, alpha, test_type) :
    Statistic = (sample_mean - test_value) / (standard_deviation / math.sqrt(sample_size))

    formula = r"\;Z = \frac{\bar{X} - \mu}{\sigma / \sqrt{n}}"
  
    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value = round(stats.norm.ppf(1 - alpha / 2, loc = 0, scale = 1), 3)
        symbol = f"\;z_{{{alpha / 2}}} = {critical_value}"
        critical_region = f"\;[{-critical_value}, {critical_value}]"
        acceptance =  Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.norm.ppf(1 - alpha, loc = 0, scale = 1), 3)
        symbol = f"\;z_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = f"\;]-\\infty, {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = f"\;[{-critical_value}, +\\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= -critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol
        

def mean_conformity_T_test(sample_mean, test_value, standard_deviation, sample_size, alpha, test_type) :
    Statistic = (sample_mean - test_value) / (standard_deviation / math.sqrt(sample_size))

    formula = r'\;T = \frac{\bar{X} - \mu}{S / \sqrt{n}}'

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value = round(stats.t.ppf(1 - alpha / 2,sample_size - 1), 3)
        symbol = f"\;t_{{{alpha / 2}}} = {critical_value}"
        critical_region = f"\;[{-critical_value}, {critical_value}]"
        acceptance = Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.t.ppf(1 - alpha, sample_size - 1), 3)
        symbol = f"\;t_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = f"\;]-\\infty, {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = f"\;[{-critical_value}, +\\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= -critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol
        

def proportion_comformity_test(estimated_proportion, test_value, sample_size, alpha, test_type) :
    Statistic = (math.sqrt(sample_size) * (estimated_proportion - test_value)) / math.sqrt(test_value * (1 - test_value))

    formula = r'\;Z = \frac{\hat{p} - p}{\sqrt{p(1 - p) / n}}'

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value = round(stats.norm.ppf(1 - alpha / 2, loc = 0, scale = 1), 3)
        symbol = f"\;z_{{{alpha / 2}}} = {critical_value}"
        critical_region = f"\;[{-critical_value}, {critical_value}]"
        acceptance = Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.norm.ppf(1 - alpha, loc = 0, scale = 1), 3)
        symbol = f"\;z_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            test_type = 'Left-tailed'
            critical_region = f"\;]-\\infty, {critical_value}]"
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = f"\;[{-critical_value}, +\\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= -critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol
        

def variance_comformity_test(standard_deviation, test_value, sample_size, alpha, test_type) :
    Statistic = (sample_size * standard_deviation ** 2) / (test_value ** 2)

    formula = r"\;\chi^2 = \frac{(n-1)s^2}{\sigma^2}"

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value_1 = round(stats.chi2.ppf(alpha / 2, sample_size - 1), 3)
        critical_value_2 = round(stats.chi2.ppf(1 - alpha / 2, sample_size - 1), 3)

        critical_value = (critical_value_1, critical_value_2)

        symbol = f"\;\chi^2_{{{alpha}}} = {critical_value_1},\chi^2_{{{1 - alpha}}} = {critical_value_2}"

        critical_region = f"\;[{critical_value_1}, {critical_value_2}]"

        acceptance =  Statistic <= critical_value_2 and Statistic >= critical_value_1
    
    else :
        critical_value = round(stats.chi2.ppf(1 - alpha, sample_size - 1), 3)
        symbol = f"\;\chi^2_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = f"\;[0, {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value and Statistic >= 0
        elif test_type == 2 :
            critical_region = f"\;[{critical_value}, +\\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol


def mean_comparison_Z_test(n_1, n_2, test_type, alpha, mean_1, mean_2, std_1, std_2) :

    Statistic = (mean_1 - mean_2) / math.sqrt(std_1 ** 2 / n_1 + std_2 ** 2 / n_2)

    formula = r"\;Z = \frac{\bar{X_1} - \bar{X_2}}{\sqrt{\frac{\sigma^2_1}{n_1} + \frac{\sigma^2_2}{n_2}}}"

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value = round(stats.norm.ppf(1 - alpha / 2, loc = 0, scale = 1), 3)

        symbol = f"\;z_{{{alpha / 2}}} = {critical_value}"

        critical_region = f"\;[{-critical_value}, {critical_value}]"

        acceptance =  Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.norm.ppf(1 - alpha, loc = 0, scale = 1), 3)
        symbol = f"\;z_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = f"\;]-\\infty, {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = f"\;[{-critical_value}, +\\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= -critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol


def mean_comparison_T_test(n_1, n_2, test_type, alpha, mean_1, mean_2, std_1, std_2) :

    Statistic = (mean_1 - mean_2) / math.sqrt((1 / n_1 + 1/ n_2) * ((n_1 * std_1 ** 2 + n_2 * std_2 ** 2) / (n_1 + n_2 - 2)))

    formula = r"\;T = \frac{\bar{X_1} - \bar{X_2}}{\sqrt{(\frac{1}{n_1} + \frac{1}{n_2})(\frac{n_1 S_1^2 + n_2 S_2^2}{n_1 + n_2 - 2})}}"

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value = round(stats.t.ppf(1 - alpha / 2, n_1 + n_2 - 2), 3)

        symbol = f"\;t_{{{alpha / 2}}} = {critical_value}"

        critical_region = f"\;[{-critical_value}, {critical_value}]"

        acceptance =  Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.t.ppf(1 - alpha, n_1 + n_2 - 2), 3)
        symbol = f"\;t_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = f"\;]-\\infty, {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = f"\;[{-critical_value}, +\\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= -critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol


def proportion_comparison_test(p_1, p_2, n_1, n_2, test_type, alpha) :

    p = (n_1 * p_1 + n_2 * p_2) / (n_1 + n_2)
    Statistic = (p_1 - p_2) / math.sqrt(p * (1 - p) * (1 / n_1 + 1 / n_2))

    formula = r'\;Z = \frac{f_1 - f_2}{\sqrt{\hat{p}(1 - \hat{p})(\frac{1}{n_1} + \frac{1}{n_2})}}'

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value = round(stats.norm.ppf(1 - alpha / 2, loc = 0, scale = 1), 3)
        symbol = f"\;z_{{{alpha / 2}}} = {critical_value}"
        critical_region = f"\;[{-critical_value}, {critical_value}]"
        acceptance = Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.norm.ppf(1 - alpha, loc = 0, scale = 1), 3)
        symbol = f"\;z_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            test_type = 'Left-tailed'
            critical_region = f"\;]-\\infty, {critical_value}]"
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = f"\;[{-critical_value}, +\\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= -critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol


def variance_comparison_test(n_1, n_2, std_1, std_2, test_type, alpha) :
    Statistic = ((n_2 - 1) / (n_1 - 1)) * ((n_1 * std_1) / (n_2 * std_2))

    formula = r"\;F = \frac{n_2 - 1}{n_1 - 1} \frac{n_1 S_1^2}{n_2 S_2^2}"

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value_1 = round(stats.f.ppf(1 - alpha / 2, dfn = n_1 - 1, dfd = n_2 - 1), 3)
        critical_value_2 = round(stats.f.ppf(alpha / 2, dfn = n_1 - 1, dfd = n_2 - 1), 3)

        critical_value = (critical_value_1, critical_value_2)

        symbol = f"\;f_{{{alpha}}} = {critical_value_1},f^2_{{{1 - alpha}}} = {critical_value_2}"

        critical_region = f"\;[{critical_value_1}, {critical_value_2}]"

        acceptance =  Statistic <= critical_value_2 and Statistic >= critical_value_1
    
    else :
        critical_value = round(stats.f.ppf(1 - alpha, dfn = n_1 - 1, dfd = n_2 - 1), 3)
        symbol = f"\;f_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = f"\;[0, {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value and Statistic >= 0
        elif test_type == 2 :
            critical_region = f"\;[{critical_value}, +\\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol


def qualitative_variables_test(original_array, alpha, rows, cols) :
    array = np.array(original_array)

    row_sums = np.sum(array, axis = 1)
    col_sums = np.sum(array, axis = 0)
    total_sum = np.sum(array)

    C_array = np.outer(row_sums, col_sums) / total_sum

    final = (array - C_array) ** 2 / C_array

    statistic = np.sum(final)

    formula = r'\;\chi_c^2 = \sum_{i, j} \frac{(n_{ij} - C_{ij})^2}{C_{ij}}'

    critical_value = round(stats.chi2.ppf(1 - alpha, (rows - 1) * (cols - 1)), 3)

    critical_region = f"\;[0, {critical_value}]"
    
    symbol = f"\;\chi^2_{{{alpha}}} = {critical_value}"

    acceptance = statistic < critical_value

    return acceptance, formula, symbol, critical_value, critical_region, statistic


def null_correlation_test(original_array, alpha, sample_size) :
    array = np.array(original_array)
    arr_1 = np.array(original_array[0])
    arr_2 = np.array(original_array[1])

    cov_matrix = np.cov(array)
    covariance = cov_matrix[0, 1]

    print(covariance)
    std_1 = np.std(arr_1)
    std_2 = np.std(arr_2)

    r = covariance / (std_1 * std_2)
    print("r = ", r)

    statistic = (r * math.sqrt(sample_size - 2)) / math.sqrt(1 - r ** 2)

    formula = r"\;T = \frac{R \sqrt{n \;- \;2}}{\sqrt{1\; - \;R^2}}"

    critical_value = round(stats.t.ppf(1 - alpha / 2,sample_size - 2), 3)
        
    symbol = f"\;t_{{{alpha / 2}}} = {critical_value}"
        
    critical_region = f"\;[{-critical_value}, {critical_value}]"
    
    acceptance = statistic <= critical_value and statistic >= -critical_value

    return acceptance, formula, symbol, critical_value, critical_region, statistic
 

def spearman_test(original_array, alpha, sample_size) :
    array = np.array(original_array)
    arr_1 = np.array(original_array[0])
    arr_2 = np.array(original_array[1])

    ranks_1 = stats.rankdata(arr_1, method='average')
    ranks_2 = stats.rankdata(arr_2, method='average')

    final = (ranks_1 - ranks_2) ** 2

    statistic = 1 - (6 * np.sum(final)) / (sample_size * (sample_size ** 2 - 1))

    formula = r"\;r_s = 1 - \frac{6 \sum (x^{'} - y^{'})^2}{n(n^2 - 1)}"

    if sample_size <= 13 :
        critical_value = spearman_critical_values[alpha][sample_size]

    else :
        critical_value = pearson_critical_value(alpha, sample_size - 2)

    critical_region = f"\;[0, {critical_value}["
    symbol = f"\;r_{{{alpha}}} = {critical_value}"

    acceptance = abs(statistic) <= critical_value

    return acceptance, formula, symbol, critical_value, critical_region, statistic

data = [[1.0, 2.0, 3.0, 4.0, 5.0], [6.0, 7.0, 8.0, 9.0, 0.0]]
print(null_correlation_test(data, 0.05, 5))