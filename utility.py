import numpy as np
import scipy.stats as stats
import math

def mean_conformity_Z_test(sample_mean, test_value, standard_deviation, sample_size, alpha, test_type) :
    Statistic = (sample_mean - test_value) / (standard_deviation / math.sqrt(sample_size))

    if test_type == 0 :
        critical_value = stats.norm.ppf(1 - alpha / 2, loc = 0, scale = 1)
        return Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = stats.norm.ppf(1 - alpha, loc = 0, scale = 1)

        if test_type == 1 :
            return Statistic <= critical_value
        elif test_type == 2 :
            return Statistic >= -critical_value
        

def mean_conformity_T_test(sample_mean, test_value, standard_deviation, sample_size, alpha, test_type) :
    Statistic = (sample_mean - test_value) / (standard_deviation / math.sqrt(sample_size))

    if test_type == 0 :
        critical_value = stats.t.ppf(1 - alpha / 2,sample_size - 1)
        return Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = stats.t.ppf(1 - alpha, sample_size - 1)

        if test_type == 1 :
            return Statistic <= critical_value
        elif test_type == 2 :
            return Statistic >= -critical_value
        

def proportion_comformity_test(estimated_proportion, test_value, sample_size, alpha, test_type) :
    Statistic = (math.sqrt(sample_size) * (estimated_proportion - test_value)) / math.sqrt(test_value * (1 - test_value))

    if test_type == 0 :
        critical_value = stats.norm.ppf(1 - alpha / 2, loc = 0, scale = 1)
        return Statistic <= critical_value and Statistic >= -critical_value
    else :
        critical_value = stats.norm.ppf(1 - alpha, loc = 0, scale = 1)

        if test_type == 1 :
            return Statistic <= critical_value
        elif test_type == 2 :
            return Statistic >= -critical_value
        

def variance_comformity_test(standard_deviation, test_value, sample_size, alpha, test_type) :
    Statistic = (sample_size * standard_deviation ** 2) / (test_value ** 2)

    if test_type == 0 :
        critical_value_1 = stats.chi2.ppf(alpha / 2, sample_size - 1)
        critical_value_2 = stats.chi2.ppf(1 - alpha / 2, sample_size - 1)

        return Statistic <= critical_value_2 and Statistic >= critical_value_1
    
    else :
        critical_value = stats.chi2.ppf(1 - alpha, sample_size - 1)

        if test_type == 1 :
            return Statistic <= critical_value and Statistic >= 0
        elif test_type == 2 :
            return Statistic >= critical_value