from flask import Flask, render_template, redirect, request, jsonify
from utility import *
import numpy as np

app = Flask(__name__)

@app.route('/')
def index() :
    return render_template('index.html')

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


@app.route('/get-result', methods = ['POST'])
def get_result() :
    text = None
    if request.method == 'POST' :
        try :
            parameter = request.form['parameter']
            n = int(request.form['sample-size'])
            hypothesis = int(request.form['hypothesis'])
            test_value = float(request.form['test-value'])
            alpha = int(request.form['alpha'])

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
                result = variance_comformity_test(std, test_value, n, alpha / 100, hypothesis)
            
            elif parameter == 'Proportion' :
                proportion = float(request.form['sample-mean'])
                result = proportion_comformity_test(proportion, test_value, n, alpha / 100, hypothesis)
            

            if result[0] :
                text = r'we\;can\;not\;reject\;H_0'
                desc = r"Since\;" + str(round(result[2], 3)) + r" \in " + result[5] + r',\;then\;'
            else :
                text = r'we\;reject\;H_0'
                desc = r"Since\;" + str(round(result[2], 3)) + r" \notin " + result[5] + r',\;then\;'
            
            data = {
                "parameter" : parameter,
                "test_type" : result[1],
                "test_value" : test_value,
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
            return e
        
    return jsonify(data)


@app.route('/get-table-data', methods = ['POST'])
def table() :
    data = request.json.get('data')
    print(data)

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



@app.route('/get-params', methods = ['POST'])
def get_params() :
    if request.method == 'POST' :
        try :
            parameter = request.form['parameter']
            n_1 = int(request.form['sample-size-1'])
            n_2 = int(request.form['sample-size-2'])
            test_type = int(request.form['hypothesis'])
            alpha = int(request.form['alpha'])
            
            if parameter == 'Mean' :
                mean_1 = float(request.form['sample-mean-1'])
                mean_2 = float(request.form['sample-mean-2'])

                std_1 = float(request.form['std-1'])
                std_2 = float(request.form['std-2'])

                known = request.form['known']

                if known == 'yes' :
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

            if result[0] :
                text = r'we\;can\;not\;reject\;H_0'
                desc = r"Since\;" + str(round(result[2], 3)) + r" \in " + result[5] + r',\;then\;'
            else :
                text = r'we\;reject\;H_0'
                desc = r"Since\;" + str(round(result[2], 3)) + r" \notin " + str(result[5]) + r',\;then\;'
            
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
            
    return jsonify(data)


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
            result = qualitative_variables_test(table_data, alpha / 100, rows, cols)
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
        print("hellooooo")
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
                print("noooooo")
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
        print("hellooooo")
        form_data = recieved.get('form')
        table_1_data = recieved.get('table_1')
        table_2_data = recieved.get('table_2')
        test = form_data['test']
        print("heeeeree")
        print(table_1_data, table_2_data)

        if test == 'MW' :
            table_1_data = table_1_data[0]
            table_2_data = table_2_data[0]
            print("boboboob")
            table_1_data = [float(element) for element in table_1_data]
            print("problem here")
            table_2_data = [float(element) for element in table_2_data]
            print("hehehehe")
        else :
            table_1_data = [[float(element) for element in row] for row in table_1_data]

        alpha = int(form_data['alpha'])
        n1 = int(form_data['sample-size-1'])
        print(n1)

        print(table_1_data, table_2_data)

        if test == 'MW' :
            n2 = int(form_data['sample-size-2'])
            result = Mann_Withney_test(table_1_data, table_2_data, alpha / 100)
            print("noooooo")

        else :
            n2 = ""
            result = wilcoxon_test(table_1_data[0], table_1_data[1], n1, alpha / 100)


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
        print("hellooooo")
        form_data = recieved.get('form')
        table_data = recieved.get('table')
        alpha = int(form_data['alpha'])
        print(table_data)
        table_data = table_data[0]
        table_data = [float(element) for element in table_data]
        
        print("kjkjkj")

        test = form_data['test-select']
        print("heeeeree")
        print(table_data)
        print(test)

        if test != 'chi2' :
            data_type = form_data['data-type']
        else :
            data_type = 'classes'

        known = form_data['param']

        if test != 'normality' :
            dist = form_data['distribution']
        else :
            dist = 'a Normal'

        if data_type == 'classes' :
            initial = float(form_data['initial'])
            k = int(form_data['sample-size'])
            print('we good')
            
            if dist != "a Poisson" :
                ran = float(form_data['range'])
            else :
                ran = 0
                print('here too')

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
                print("lol")

            if test == 'samir' :
                print('maybe here')
                result = kolmogorov_sminrov_test_grouped_data(table_data, initial, ran, k, alpha / 100, distributions[dist], p)
                print("kkfhskjhd")
            elif test == 'chi2' :
                print("here we go")
                print(table_data, initial, ran, k, alpha / 100, distributions[dist], p)
                result = chi_square_test(table_data, initial, ran, k, alpha / 100, distributions[dist], p)
                print("saaad")

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

            if test == 'samir' :
                result = kolmogorov_sminrov_test_raw_data(table_data, n, alpha / 100, distributions[dist], p)


        if bool(result[0]) :
            text = r'we\;accept\;H_0'
            desc = r"Since\;" + str(round(result[5], 3)) + r" \in " + str(result[4]) + r",\;then\;"
            
        else :
            text = r'we\;reject\;H_0'
            desc = r"Since\;" + str(round(result[5], 3)) +  r" \notin " + str(result[4]) + r',\;then\;'
            

        data = {
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