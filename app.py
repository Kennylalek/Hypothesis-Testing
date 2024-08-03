from flask import Flask, render_template, redirect, request, jsonify
from utility import *

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
                print('done here !!!')
                result = proportion_comformity_test(proportion, test_value, n, alpha / 100, hypothesis)
            

            if result[0] :
                text = f'we\;can\;not\;reject\;H_0'
                desc = f"Since\;{round(result[2], 3)} \\in " + result[5] + ',\;then\;'
            else :
                text = 'we\;reject\;H_0'
                desc = f"Since\;{round(result[2], 3)} \\notin " + result[5] + ',\;then\;'
            
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

            print(data)

        except Exception as e :
            return e
        
    return jsonify(data)

       

if __name__ == "__main__" :
    app.run(debug = True, port=5001)