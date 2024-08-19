import numpy as np
import scipy.stats as stats
import math
from critical_values import *

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
        symbol = r"\;" + f"z_{{{alpha / 2}}} = {critical_value}"
        critical_region = r"\;" + f"[{-critical_value}, {critical_value}]"
        acceptance =  Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.norm.ppf(1 - alpha, loc = 0, scale = 1), 3)
        symbol = r"\;" + f"z_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = r"\;]- \infty" + f", {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = r"\;" + f"[{-critical_value}" + r", +\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= -critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol
        

def mean_conformity_T_test(sample_mean, test_value, standard_deviation, sample_size, alpha, test_type) :
    Statistic = (sample_mean - test_value) / (standard_deviation / math.sqrt(sample_size))

    formula = r'\;T = \frac{\bar{X} - \mu}{S / \sqrt{n}}'

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value = round(stats.t.ppf(1 - alpha / 2,sample_size - 1), 3)
        symbol = r"\;" + f"t_{{{alpha / 2}}} = {critical_value}"
        critical_region = r"\;" + f"[{-critical_value}, {critical_value}]"
        acceptance = Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.t.ppf(1 - alpha, sample_size - 1), 3)
        symbol = r"\;" + f"t_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = r"\;]- \infty" + f", {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = r"\;" + f"[{-critical_value}" + r", +\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= -critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol
        

def proportion_conformity_test(estimated_proportion, test_value, sample_size, alpha, test_type) :
    Statistic = (math.sqrt(sample_size) * (estimated_proportion - test_value)) / math.sqrt(test_value * (1 - test_value))

    formula = r'\;Z = \frac{\hat{p} - p}{\sqrt{p(1 - p) / n}}'

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value = round(stats.norm.ppf(1 - alpha / 2, loc = 0, scale = 1), 3)
        symbol = r"\;" + f"z_{{{alpha / 2}}} = {critical_value}"
        critical_region = r"\;" + f"[{-critical_value}, {critical_value}]"
        acceptance = Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.norm.ppf(1 - alpha, loc = 0, scale = 1), 3)
        symbol = r"\;" + f"z_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            test_type = 'Left-tailed'
            critical_region = r"\;]-\infty," + f" {critical_value}]"
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = r"\;" + f"[{-critical_value}," +  r" +\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= -critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol
        

def variance_conformity_test(standard_deviation, test_value, sample_size, alpha, test_type) :
    Statistic = (sample_size * standard_deviation ** 2) / (test_value ** 2)

    formula = r"\;\chi^2 = \frac{(n-1)s^2}{\sigma^2}"

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value_1 = round(stats.chi2.ppf(alpha / 2, sample_size - 1), 3)
        critical_value_2 = round(stats.chi2.ppf(1 - alpha / 2, sample_size - 1), 3)

        critical_value = (critical_value_1, critical_value_2)

        symbol = r"\;\chi^2_" + f"{{{1 - alpha / 2}}} = {critical_value_1}," + r"\chi^2_" + f"{{{alpha / 2}}} = {critical_value_2}"

        critical_region = r"\;" + f"[{critical_value_1}, {critical_value_2}]"

        acceptance =  Statistic <= critical_value_2 and Statistic >= critical_value_1
    
    else :
        critical_value = round(stats.chi2.ppf(1 - alpha, sample_size - 1), 3)
        symbol = r"\;\chi^2_" + f"{{{1 - alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = r"\;" + f"[0, {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value and Statistic >= 0
        elif test_type == 2 :
            critical_region = r"\;" + f"[{critical_value}," + r" +\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol


def mean_comparison_Z_test(n_1, n_2, test_type, alpha, mean_1, mean_2, std_1, std_2) :

    Statistic = (mean_1 - mean_2) / math.sqrt(std_1 ** 2 / n_1 + std_2 ** 2 / n_2)

    formula = r"\;Z = \frac{\bar{X_1} - \bar{X_2}}{\sqrt{\frac{\sigma^2_1}{n_1} + \frac{\sigma^2_2}{n_2}}}"

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value = round(stats.norm.ppf(1 - alpha / 2, loc = 0, scale = 1), 3)

        symbol = r"\;" + f"z_{{{alpha / 2}}} = {critical_value}"

        critical_region = r"\;" + f"[{-critical_value}, {critical_value}]"

        acceptance =  Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.norm.ppf(1 - alpha, loc = 0, scale = 1), 3)
        symbol = r"\;" + f"z_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = r"\;]-\infty," + f" {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = r"\;" + f"[{-critical_value}," + r" +\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= -critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol


def mean_comparison_T_test(n_1, n_2, test_type, alpha, mean_1, mean_2, std_1, std_2) :

    Statistic = (mean_1 - mean_2) / math.sqrt((1 / n_1 + 1/ n_2) * ((n_1 * std_1 ** 2 + n_2 * std_2 ** 2) / (n_1 + n_2 - 2)))

    formula = r"\;T = \frac{\bar{X_1} - \bar{X_2}}{\sqrt{(\frac{1}{n_1} + \frac{1}{n_2})(\frac{n_1 S_1^2 + n_2 S_2^2}{n_1 + n_2 - 2})}}"

    if test_type == 0 :
        test_type = 'Two-tailed'
        critical_value = round(stats.t.ppf(1 - alpha / 2, n_1 + n_2 - 2), 3)

        symbol = r"\;" + f"t_{{{alpha / 2}}} = {critical_value}"

        critical_region = r"\;" + f"[{-critical_value}, {critical_value}]"

        acceptance =  Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.t.ppf(1 - alpha, n_1 + n_2 - 2), 3)
        symbol = r"\;" + f"t_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = r"\;]-\infty," + f" {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = r"\;" + f"[{-critical_value}," + r" +\infty["
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
        symbol = r"\;" + f"z_{{{alpha / 2}}} = {critical_value}"
        critical_region = r"\;" + f"[{-critical_value}, {critical_value}]"
        acceptance = Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = round(stats.norm.ppf(1 - alpha, loc = 0, scale = 1), 3)
        symbol = r"\;" + f"z_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            test_type = 'Left-tailed'
            critical_region = r"\;]-\infty," + f" {critical_value}]"
            acceptance = Statistic <= critical_value
        elif test_type == 2 :
            critical_region = r"\;" + f"[{-critical_value}," + r" +\infty["
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

        symbol = r"\;" + f"f_{{{alpha / 2}}} = {critical_value_1},f_{{{1 - alpha / 2}}} = {critical_value_2}"

        critical_region = r"\;" + f"[{critical_value_2}, {critical_value_1}]"

        acceptance =  Statistic <= critical_value_1 and Statistic >= critical_value_2
    
    else :
        critical_value = round(stats.f.ppf(1 - alpha, dfn = n_1 - 1, dfd = n_2 - 1), 3)
        symbol = r"\;" + f"f_{{{alpha}}} = {critical_value}"

        if test_type == 1 :
            critical_region = r"\;" + f"[0, {critical_value}]"
            test_type = 'Left-tailed'
            acceptance = Statistic <= critical_value and Statistic >= 0
        elif test_type == 2 :
            critical_region = r"\;" + f"[{critical_value}," + r" +\infty["
            test_type = 'Right-tailed'
            acceptance = Statistic >= critical_value

    return acceptance, test_type, Statistic, formula, critical_value, critical_region, symbol


def categorical_variables_test(original_array, alpha, rows, cols) :
    array = np.array(original_array)

    row_sums = np.sum(array, axis = 1)
    col_sums = np.sum(array, axis = 0)
    total_sum = np.sum(array)

    C_array = np.outer(row_sums, col_sums) / total_sum

    num_of_C = sum(1 for sample in C_array for x in sample if x < 5)
    num_of_elem = len(original_array[0]) * len(original_array)

    if num_of_C / num_of_elem >= 0.2 :
        appliquable = 'no'
    else :
        appliquable = 'yes'

    final = (array - C_array) ** 2 / C_array

    statistic = np.sum(final)

    formula = r'\;\chi_c^2 = \sum_{i, j} \frac{(n_{ij} - C_{ij})^2}{C_{ij}}'

    critical_value = round(stats.chi2.ppf(1 - alpha, (rows - 1) * (cols - 1)), 3)

    critical_region = r"\;" + f"[0, {critical_value}]"
    
    symbol = r"\;\chi^2_" + f"{{{alpha}}} = {critical_value}"

    acceptance = statistic < critical_value

    return acceptance, formula, symbol, critical_value, critical_region, statistic, appliquable


def null_correlation_test(original_array, alpha, sample_size) :
    arr_1 = np.array(original_array[0])
    arr_2 = np.array(original_array[1])

    cov_matrix = np.cov(arr_1, arr_2)
    covariance = cov_matrix[0, 1]

    std_1 = np.std(arr_1, ddof = 1)
    std_2 = np.std(arr_2, ddof = 1)

    r = round(covariance / (std_1 * std_2), 3)

    statistic = (r * math.sqrt(sample_size - 2)) / math.sqrt(1 - r ** 2)

    formula = r"\;T = \frac{R \sqrt{n \;- \;2}}{\sqrt{1\; - \;R^2}}"

    critical_value = round(stats.t.ppf(1 - alpha / 2,sample_size - 2), 3)
        
    symbol = r"\;" + f"t_{{{alpha / 2}}} = {critical_value}"
        
    critical_region = r"\;" + f"[{-critical_value}, {critical_value}]"
    
    acceptance = statistic <= critical_value and statistic >= -critical_value
    appliquable = 'yes'

    return acceptance, formula, symbol, critical_value, critical_region, statistic, appliquable
 

def spearman_test(original_array, alpha, sample_size) :
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

    critical_region = r"\;" + f"[0, {critical_value}["
    symbol = r"\;" + f"r_{{{alpha}}} = {critical_value}"

    acceptance = abs(statistic) <= critical_value
    appliquable = 'yes'

    return acceptance, formula, symbol, critical_value, critical_region, statistic, appliquable


def ANOVA(data, sample_count, alpha):

    formula = r"\;F = \frac{\frac{S_F^2}{k - 1}}{\frac{S_R^2}{n - k}}"

    statistic, p_value = stats.f_oneway(*data)

    lengths = [len(sample) for sample in data]
    flattened_data = [item for sample in data for item in sample]
    n = sum(lengths)

    mean = np.mean(flattened_data)
    variance = np.var(flattened_data)

    variances = [np.var(sample) for sample in data]
    mean_of_variances = round(np.mean(variances), 3)

    means = [np.mean(sample) for sample in data]
    variance_of_means = round(np.var(means), 3)

    critical_value = round(stats.f.ppf(1 - alpha, dfn = sample_count - 1, dfd = n - sample_count), 3)
    symbol = r"\;" + f"f_{{{alpha}}} = {critical_value}"

    critical_region = r"\;" + f"[0, {critical_value}]"
    acceptance = statistic <= critical_value and statistic >= 0

    return acceptance, formula, symbol, critical_value, critical_region, statistic, mean, variance, mean_of_variances, variance_of_means


def Bartlett_test(data, sample_count, alpha) :
    # lengths = [len(sample) for sample in data]
    # l = 1 + (1 / (3 * (sample_count - 1))) * (sum([1 / (length - 1) for length in lengths]) - 1 / (n - sample_count))

    B, p = stats.bartlett(*data)

    critical_value = round(stats.chi2.ppf(1 - alpha, sample_count - 1), 3)

    formula_l = r"\; \lambda = 1 + \frac{1}{3(k\;-\;1)} \left[\left (\sum\limits_{i = 1}^k \frac{1}{n_i\;-\;1} \right) - \frac{1}{n\;-\;k} \right]"

    formula_b = r"\;B = \frac{1}{\lambda} \left[(n\;-\;k)\;ln\;S_R^2\;-\; \sum\limits_{i = 1}^k (n_i - 1)\;ln\;S_i^2 \right]"

    critical_region = r"\;" + f"[0, {critical_value}]"
    symbol = r"\;\chi^2_" + f"{{{alpha}}} = {critical_value}"

    acceptance = B < critical_value

    return acceptance, formula_b, symbol ,critical_value, critical_region, B, formula_l


def Kruskal_Wallis_test(data, sample_count, alpha) :
    lengths = [len(sample) for sample in data]
    lengths.sort(reverse = True)
    tup = tuple(lengths)

    formula = r"\;h = \frac{12}{n(n\;+\;1)} \left ( \sum\limits_{i=1}^k \frac{r_i^2}{n_i} \right) - 3(n + 1)"

    statistic, p_value = stats.kruskal(*data)

    if sample_count <= 5 :
        limit = True

        for length in lengths :
            if length > 16 / sample_count :
                limit = False
                break
        
        if limit :
            critical_value = kruskal_wallis_critical_values[alpha][tup]
            symbol = r"\;" + f"h_{{{alpha}}} = {critical_value}"
        else :
            critical_value = round(stats.chi2.ppf(1 - alpha, sample_count - 1), 3)
            symbol = r"\;\chi^2_" + f"{{{alpha}}} = {critical_value}"
    else :
        critical_value = round(stats.chi2.ppf(1 - alpha, sample_count - 1), 3)
        symbol = r"\;\chi^2_" + f"{{{alpha}}} = {critical_value}"



    critical_region = r"\;" + f"[0, {critical_value}]"
    acceptance = statistic <= critical_value and statistic >= 0

    return acceptance, formula, symbol, critical_value, critical_region, statistic


def Mann_Withney_test(sample_1, sample_2, alpha) :
    n1, n2 = len(sample_1), len(sample_2)
    u1, p_value = stats.mannwhitneyu(sample_1, sample_2)
    u2 = n1 * n2 - u1

    u = min(u1, u2)

    if n1 <= 20 and n2 <= 20 :
        tup = (n1, n2)
        critical_value = mann_withney_critical_values[alpha][tup]

        formula = r"\;u = min\{u_1, u_2\}"
        symbol = r"\;" + f"m_{{{alpha}}} = {critical_value}"
        critical_region = r"\;" + f"[{critical_value}," + r" +\infty["

        acceptance = u > critical_value

    else :
        mu = n1 * n2 / 2
        sigma = math.sqrt((n1 * n2 * (n1 + n2 + 1)) / 12)
        U_alpha = stats.norm.ppf(1 - alpha, loc = 0, scale = 1)

        critical_value = (U_alpha - mu) / sigma
        
        symbol = r"\;" + f"z_{{{alpha}}} = {critical_value}"
        critical_region = r"\;" + f"]{-critical_value}, {critical_value}["

        acceptance =  u <= critical_value and u >= -critical_value

    
    return acceptance, formula, symbol, critical_value, critical_region, u, u1, u2


def wilcoxon_test(sample_1, sample_2, alpha) :

    w, p_value = stats.wilcoxon(sample_1, sample_2)
    first = np.array(sample_1)
    second = np.array(sample_2)
    differences = first - second
    differences = differences[differences != 0]
    n = len(differences)

    ranks = stats.rankdata(np.abs(differences), method='average')
    w_plus = np.sum(ranks[differences > 0])
    w_minus = np.sum(ranks[differences < 0])
    

    if n <= 25 :
        critical_value = wilcoxon_critical_values[alpha][n]

        formula = r"\;u = min\{w_+, w_-\}"
        symbol = r"\;" + f"w_{{{alpha}}} = {critical_value}"
        critical_region = r"\;" + f"[0, {critical_value}["

        acceptance = w < critical_value

    else :
        mu = n * (n + 1) / 2
        sigma = math.sqrt((n * (n + 1) * (2 * n + 1)) / 24)
        U_alpha = stats.norm.ppf(1 - alpha, loc = 0, scale = 1)

        critical_value = (U_alpha - mu) / sigma
        
        symbol = r"\;" + f"z_{{{alpha}}} = {critical_value}"
        critical_region = r"\;" + f"]{-critical_value}, {critical_value}["

        acceptance =  w <= critical_value and w >= -critical_value

    return acceptance, formula, symbol, critical_value, critical_region, w, w_plus, w_minus

 
def chi_square_test(data, initial, r, k, alpha, distribution, params) :
    values = []
    middle_values = []
    n = sum(data)

    if r == 0 :
        for i in range(k) :
            values.append(initial + i)
        middle_values = values
    else :
        for i in range(k) :
            values.append(initial + (i + 1) * r)
            middle_values.append(initial + (2 * i + 1) * r / 2)

    values = np.array(values)

    if params == 'k' :
        weighted_sum = sum(value * freq for value, freq in zip(middle_values, data))
        total_frequency = sum(data)
        mean = weighted_sum / total_frequency

        # Calculate standard deviation
        variance = sum(freq * (value - mean) ** 2 for value, freq in zip(middle_values, data)) / total_frequency
        std_dev = math.sqrt(variance)

        p = (mean, std_dev)
    
    else :
        p = params

    if distribution == 'norm' :
        theoritical = np.array([n * (stats.norm.cdf(element, loc = p[0], scale = p[1]) - stats.norm.cdf(element - r, loc = p[0], scale = p[1])) for element in values])
        dist = r"\;N" + f"({p[0]}, {round(p[1] ** 2, 2)})"
        num_p = 2

    elif distribution == 'expon' :
        theoritical = np.array([n * (stats.expon.cdf(element, loc = p[0]) - stats.expon.cdf(element - r, loc = p[0]) for element in values)])
        dist = r"\;\text{Exp}" + f"({1 / p[0]}"
        num_p = 1

    elif distribution == 'poisson' :
        theoritical = np.array([n * stats.poisson.pmf(element, p[0]) for element in values])
        dist = r"\; Poisson" + f"({p[0]})"
        num_p = 1

    num_of_C = sum(1 for x in theoritical if x < 5)

    if num_of_C / len(data) >= 0.2 :
        appliquable = 'no'
    else :
        appliquable = 'yes'

    differences = data - theoritical
    differences = [round(element ** 2, 3) for element in differences]

    final = differences / theoritical

    statistic = sum(final)
    critical_value = round(stats.chi2.ppf(1 - alpha, k - 1 - num_p), 3)
    
    acceptance = statistic < critical_value

    formula = r"\;\chi_c^2 = \sum\limits_{i = 1}^k \frac{(O_i - C_i)^2}{C_i}"
    symbol = r"\;\chi^2_" + f"{{{alpha}}} = {critical_value}"
    critical_region = r"\;" + f"[0, {critical_value}["

    return acceptance, formula, symbol, critical_value, critical_region, statistic, dist, appliquable


def kolmogorov_sminrov_test_grouped_data(data, initial, r, k, alpha, distribution, params) :
        
    values = []
    middle_values = []

    if r == 0 :
        for i in range(k) :
            values.append(initial + i)
        middle_values = values
    else :
        for i in range(k) :
            values.append(initial + (i + 1) * r)
            middle_values.append(initial + (2 * i + 1) * r / 2)

    
    if params == 'k' :
        weighted_sum = sum(value * freq for value, freq in zip(middle_values, data))
        total_frequency = sum(data)
        mean = weighted_sum / total_frequency

        # Calculate standard deviation
        variance = sum(freq * (value - mean) ** 2 for value, freq in zip(middle_values, data)) / total_frequency
        std_dev = math.sqrt(variance)

        p = (mean, std_dev)
    
    else :
        p = params

    cumulative_sum = np.cumsum(data)
    total_sum = cumulative_sum[-1]

    relative_cumultive = cumulative_sum / total_sum

    if distribution == 'norm' :
        initial_value = stats.norm.cdf(initial, loc = p[0], scale = p[1])
        values = np.array([stats.norm.cdf(element, loc = p[0], scale = p[1]) - initial_value for element in values])
        dist = r"\;N" + f"({p[0]}, {round(p[1] ** 2, 2)})"
    elif distribution == 'expon' :
        initial_value = stats.expon.cdf(initial, scale = p[0])
        values = np.array([stats.expon.cdf(element, loc = p[0]) - initial_value for element in values])
        dist = r"\;{Exp}" + f"({1 / p[0]}"
    elif distribution == 'poisson' :
        values = np.array([stats.poisson.cdf(element, p[0]) for element in values])
        dist = r"\;{Poisson}" + f"({p[0]})"

    differences = values - relative_cumultive
    differences = [round(abs(element), 3) for element in differences]


    statistic = max(differences)

    if total_sum <= 40 :
        critical_value = kolmogorov_sminrov_critical_values[alpha][total_sum] # / math.sqrt(total_sum)
    else :
        dividors = {
            0.01 : 1.63,
            0.05 : 1.36,
            0.1 : 1.22
        }
        critical_value = dividors[alpha] / math.sqrt(total_sum)

    critical_value = round(critical_value, 3)

    acceptance = statistic < critical_value

    formula = r"\;D_n = sup|F_n(x) - F(x)|"
    symbol = r"\;\frac{c}{\sqrt{n}} = " + f"{critical_value}"
    critical_region = r"\;" + f"[0, {critical_value}["

    appliquable = 'yes'

    return acceptance, formula, symbol, critical_value, critical_region, statistic, dist, appliquable

        
def kolmogorov_sminrov_test_raw_data(data, n, alpha, distribution, params) :

    if params == 'k' :
        mean = np.mean(data)
        std = np.std(data)
        p = (mean, std)
    else :
        p = params

    distributions = {
        'expon' : r"\;\text{Exp}" + f"({1 / p[0]}",
        'norm' : r"\;\mathcal{N}" + f"({p[0]}, {p[1] ** 2}",
        'poisson' : r"\;\text{Poisson}" + f"({p[0]})"
    }

    dist = distributions[distribution]

    D, p = stats.kstest(data, distribution, args = p)
    
    if n <= 40 :
        critical_value = kolmogorov_sminrov_critical_values[alpha][n] # / math.sqrt(total_sum)
    else :
        dividors = {
            0.01 : 1.63,
            0.05 : 1.36,
            0.1 : 1.22
        }
        critical_value = dividors[alpha] / math.sqrt(n)

    acceptance = D < critical_value

    formula = r"\;D_n = sup|F_n(x) - F(x)|"
    symbol = r"\;\frac{c}{\sqrt{n} = }" + f"{critical_value}"
    critical_region = r"\;" + f"[0, {critical_value}["

    return acceptance, formula, symbol, critical_value, critical_region, D, dist