from flask import Flask, render_template, redirect, request, jsonify
from utility import *
import numpy as np

app = Flask(__name__)


# main route
@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/construction')
def construction() :
    return render_template('under-construction.html')

# routes for different tests
@app.route('/tests')
def tests() :
    return render_template('tests.html')

@app.route('/conformity-tests')
def conformity_tests() :
    return render_template('conformity-tests.html')

@app.route('/comparison-tests')
def comparison_tests() :
    return render_template('comparison-tests.html')

@app.route('/independence-tests')
def independnce_tests() :
    return render_template('independence-tests.html')

@app.route('/multiple-samples-tests')
def multiple_sample_tests() :
    return render_template('multiple-samples-tests.html')

@app.route('/non-parametric-tests')
def non_parametric_tests() :
    return render_template('non-parametric.html')

@app.route('/homogeneity-tests')
def homogeneity_tests() :
    return render_template('homogeneity-tests.html')

# routes for receiving data from data forms
@app.route('/conformity', methods = ['POST'])
def conformity() :

    try :
        # we get data from form inputs and selects
        parameter = request.form['parameter']
        n = int(request.form['sample-size'])
        hypothesis = int(request.form['hypothesis'])
        test_value = float(request.form['test-value'])
        alpha = int(request.form['alpha'])

        # here we get the remaining data accordingly and maake the appropriate function call
        if parameter == 'Mean' :
            sample_mean = float(request.form['sample-mean'])
            std = float(request.form['std'])
            std_known = request.form['known']

            if std_known == 'yes' :
                result = mean_conformity_Z_test(sample_mean, test_value, std, n, alpha / 100, hypothesis)
            else :
                result = mean_conformity_T_test(sample_mean, test_value, std, n, alpha / 100, hypothesis)

        elif parameter == 'Variance' :
            std = float(request.form['std'])
            result = variance_conformity_test(std, test_value, n, alpha / 100, hypothesis)
        
        elif parameter == 'Proportion' :
            proportion = float(request.form['sample-mean'])
            result = proportion_conformity_test(proportion, test_value, n, alpha / 100, hypothesis)
        

        # we interpret the results (we show the results in latex format)
        if result[0] :
            text = r'we\;can\;not\;reject\;H_0'
            desc = r"Since\;" + str(round(result[2], 3)) + r" \in " + result[5] + r',\;then\;'
        else :
            text = r'we\;reject\;H_0'
            desc = r"Since\;" + str(round(result[2], 3)) + r" \notin " + result[5] + r',\;then\;'
        
        # we orgnize the returned data
        data = {
            "parameter" : parameter,
            "test_type" : result[1],
            "test_value" : test_value,
            "alpha" : alpha / 100,
            "formula" : result[3],
            "stat_value" : round(result[2], 3),
            "critical_region" : result[5],
            "symbol" : result[6],
            "desc" : desc,
            "text" : text
        }

    except Exception as e :
        return e
        
    # we return the data in json format
    return jsonify(data)



@app.route('/comparison', methods = ['POST'])
def comparison() :

    try :
        # we get data from form inputs and selects
        parameter = request.form['parameter']
        n_1 = int(request.form['sample-size-1'])
        n_2 = int(request.form['sample-size-2'])
        test_type = int(request.form['hypothesis'])
        alpha = int(request.form['alpha'])
        
        # here we get the remaining data accordingly and maake the appropriate function call
        if parameter == 'Mean' :
            mean_1 = float(request.form['sample-mean-1'])
            mean_2 = float(request.form['sample-mean-2'])

            std_1 = float(request.form['std-1'])
            std_2 = float(request.form['std-2'])

            std_known = request.form['known']

            if std_known == 'yes' :
                result = mean_comparison_Z_test(n_1, n_2, test_type, alpha / 100, mean_1, mean_2, std_1, std_2)
            else :
                result = mean_comparison_T_test(n_1, n_2, test_type, alpha / 100, mean_1, mean_2, std_1, std_2)
        

        elif parameter == 'Variance' :
            std_1 = float(request.form['std-1'])
            std_2 = float(request.form['std-2'])

            result = variance_comparison_test(n_1, n_2, std_1, std_2, test_type, alpha / 100)

        elif parameter == 'Proportion' :
            mean_1 = float(request.form['sample-mean-1'])
            mean_2 = float(request.form['sample-mean-2'])

            result = proportion_comparison_test(mean_1, mean_2, n_1, n_2, test_type, alpha / 100)


        # we interpret the results (we show the results in latex format)
        if result[0] :
            text = r'we\;can\;not\;reject\;H_0'
            desc = r"Since\;" + str(round(result[2], 3)) + r" \in " + result[5] + r',\;then\;'
        else :
            text = r'we\;reject\;H_0'
            desc = r"Since\;" + str(round(result[2], 3)) + r" \notin " + str(result[5]) + r',\;then\;'


        # orgnizing the returned data
        data = {
            "parameter" : parameter,
            "test_type" : result[1],
            "alpha" : alpha / 100,
            "text" : text,
            "formula" : result[3],
            "stat_value" : round(result[2], 3),
            "critical_region" : result[5],
            "symbol" : result[6],
            "desc" : desc,
            "text" : text
        }

    except Exception as e :
        print(e)
            
    # we return the data in json format
    return jsonify(data)



@app.route('/get-table-data', methods = ['POST'])
def table() :
    data = request.json.get('data')

    if data:
        data = [float(x) for x in data]
        mean_value = np.mean(data)
        print(mean_value)
        std_value = np.std(data)
    else:
        mean_value = None
        std_value = None

    result = {
        'success' : True,
        'mean' : mean_value,
        'std' : std_value
    }

    return jsonify(result)


@app.route('/independence', methods = ['POST'])
def independence() :
    try :
        recieved = request.json
        form_data = recieved.get('form')
        table_data = recieved.get('table')

        table_data = [[float(element) for element in row] for row in table_data]

        character = form_data['character']
        alpha = int(form_data['alpha'])

        rows = form_data['rows']
        cols = form_data['cols']

        if character == 'qualitative' :
            rows = int(rows)
            cols = int(cols)
            result = categorical_variables_test(table_data, alpha / 100, rows, cols)
            n = (rows - 1) * (cols - 1)

        else :
            test_type = form_data['test-type']
            n = int(form_data['sample-size'])

            if test_type == 'parametric' :
                result = null_correlation_test(table_data, alpha / 100, n)
            else :
                result = spearman_test(table_data, alpha / 100, n)

            n -= 2

        if bool(result[0]) :
            text = r'we\;accept\;H_0'
            desc = r"Since\;" + str(round(result[5], 3)) + r" \in " + str(result[4]) + r",\;then\;"
            
        else :
            text = r'we\;reject\;H_0'
            desc = r"Since\;" + str(round(result[5], 3)) +  r" \notin " + str(result[4]) + r',\;then\;'
            
        data = {
            "appliquable" : result[6],
            "character" : character,
            "rows" : rows,
            "cols" : cols,
            "alpha" : alpha / 100,
            "formula" : result[1],
            "stat_value" : round(result[5], 3),
            "critical_region" : result[4],
            "symbol" : result[2],
            "desc" : desc,
            "text" : text,
            "dof" : n
        }
    
    except Exception as e :
        return e
    
    return jsonify(data)


@app.route('/multiple-samples', methods = ['POST'])
def multiple_samples() :
    try :
        test_type = ''

        recieved = request.json
        form_data = recieved.get('form')
        table_data = recieved.get('table')

        table_data = [[float(element) for element in row] for row in table_data]

        parameter = form_data['parameter']
        alpha = int(form_data['alpha'])

        n = sum([len(sample) for sample in table_data])
        k = int(form_data['rows'])
        

        print(table_data)

        if parameter == 'mean' :
            test_type = form_data['test-type']
            if test_type == 'parametric' :
                t = 'ANOVA'
                result = ANOVA(table_data, k, alpha / 100)
            else :
                t = 'KW'
                result = Kruskal_Wallis_test(table_data, k, alpha / 100)

        else :
            t = 'Bartlett'
            result = Bartlett_test(table_data, k, alpha / 100)


        if bool(result[0]) :
            text = r'we\;accept\;H_0'
            desc = r"Since\;" + str(round(result[5], 3)) + r" \in " + str(result[4]) + r",\;then\;"
            
        else :
            text = r'we\;reject\;H_0'
            desc = r"Since\;" + str(round(result[5], 3)) +  r" \notin " + str(result[4]) + r',\;then\;'
            
        data = {
            "t" : t,
            "n" : n,
            "k" : k,
            "alpha" : alpha / 100,
            "formula" : result[1],
            "stat_value" : round(result[5], 3),
            "critical_region" : result[4],
            "symbol" : result[2],
            "desc" : desc,
            "text" : text
        }

        if parameter == 'mean' and test_type == 'parametric' :
            data['mean'] = result[6]
            data['variance'] = result[7]
            data['SR'] = round(n * result[8], 3)
            data['SF'] = round(n * result[9], 3)
            data["S"] = round(n * (result[8] + result[9]), 3)

        elif parameter == 'variance' :
            data['lambda'] = result[6]

    
    except Exception as e :
        return e
    
    return jsonify(data)


@app.route('/non-parametric', methods = ['POST'])
def non_parametric() :
    try :
        recieved = request.json
        form_data = recieved.get('form')
        table_1_data = recieved.get('table_1')
        table_2_data = recieved.get('table_2')
        test = form_data['test']

        if test == 'MW' :
            table_1_data = table_1_data[0]
            table_2_data = table_2_data[0]
            table_1_data = [float(element) for element in table_1_data]
            table_2_data = [float(element) for element in table_2_data]
        else :
            table_1_data = [[float(element) for element in row] for row in table_1_data]

        alpha = int(form_data['alpha'])
        n1 = int(form_data['sample-size-1'])

        if test == 'MW' :
            n2 = int(form_data['sample-size-2'])
            result = Mann_Withney_test(table_1_data, table_2_data, alpha / 100)

        else :
            n2 = ""
            print("bok")
            result = wilcoxon_test(table_1_data[0], table_1_data[1], alpha / 100)


        if bool(result[0]) :
            text = r'we\;accept\;H_0'
            desc = r"Since\;" + str(round(result[5], 3)) + r" \in " + str(result[4]) + r",\;then\;"
            
        else :
            text = r'we\;reject\;H_0'
            desc = r"Since\;" + str(round(result[5], 3)) +  r" \notin " + str(result[4]) + r',\;then\;'
            
        data = {
            "n1" : n1,
            "n2" : n2,
            "v1" : result[6],
            "v2" : result[7],
            "test" : test,
            "alpha" : alpha / 100,
            "formula" : result[1],
            "stat_value" : round(result[5], 3),
            "critical_region" : result[4],
            "symbol" : result[2],
            "desc" : desc,
            "text" : text
        }

    
    except Exception as e :
        return e
    
    return jsonify(data)


@app.route('/homogeneity', methods = ['POST'])
def homogeneity() :
    try :
        distributions = {
            'a Normal' : 'norm',
            'an Exponential' : 'expon',
            'a Poisson' : 'poisson'
        }

        recieved = request.json
        form_data = recieved.get('form')
        table_data = recieved.get('table')
        alpha = int(form_data['alpha'])
        table_data = table_data[0]
        table_data = [float(element) for element in table_data]

        test = form_data['test-select']

        if test != 'Chi-Square' :
            data_type = form_data['data-type']
        else :
            data_type = 'classes'

        known = form_data['param']

        if test != 'Normality' :
            dist = form_data['distribution']
        else :
            dist = 'a Normal'

        if data_type == 'classes' :
            initial = float(form_data['initial'])
            k = int(form_data['sample-size'])
            
            if dist != "a Poisson" :
                ran = float(form_data['range'])
            else :
                ran = 0

            size = sum(table_data)

            if known == 'given' :
                mean = float(form_data['sample-mean'])

                if dist != 'a Normal' :
                    p = (mean)
                else :
                    std = float(form_data['std'])
                    p = (mean, std)
            else :
                p = 'k'

            if test == 'Kolmogorov-Sminrov' :
                result = kolmogorov_sminrov_test_grouped_data(table_data, initial, ran, k, alpha / 100, distributions[dist], p)
            elif test == 'Chi-Square' :
                result = chi_square_test(table_data, initial, ran, k, alpha / 100, distributions[dist], p)

        else :
            n = form_data['sample-size']
            size = n
            if known == 'given' :
                mean = float(form_data['sample-mean'])

                if dist != 'a Normal' :
                    p = (mean)
                else :
                    std = float(form_data['std'])
                    p = (mean, std)
            else :
                p = 'k'

            if test == 'Kolmogorov-Sminrov' :
                result = kolmogorov_sminrov_test_raw_data(table_data, n, alpha / 100, distributions[dist], p)


        if bool(result[0]) :
            text = r'we\;accept\;H_0'
            desc = r"Since\;" + str(round(result[5], 3)) + r" \in " + str(result[4]) + r",\;then\;"
            
        else :
            text = r'we\;reject\;H_0'
            desc = r"Since\;" + str(round(result[5], 3)) +  r" \notin " + str(result[4]) + r',\;then\;'
            

        data = {
            "appliquable" : result[7],
            "test" : test,
            "dist" : result[6],
            "n" : size,
            "alpha" : alpha / 100,
            "formula" : result[1],
            "stat_value" : round(result[5], 3),
            "critical_region" : result[4],
            "symbol" : result[2],
            "desc" : desc,
            "text" : text
        }

    
    except Exception as e :
        return e
    
    return jsonify(data)

if __name__ == "__main__" :
    app.run(debug = True, port=5001)