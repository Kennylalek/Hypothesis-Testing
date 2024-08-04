import scipy.stats as stats
import math

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