from flask import Flask, render_template, redirect, request
from utility import *

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index() :
    return render_template('index.html')

@app.route('/tests', methods = ['GET'])
def tests() :
    return render_template('tests.html')

@app.route('/conformity-tests', methods = ['GET', 'POST'])
def conformity_tests() :

    text = None
    if request.method == 'POST' :
        try :
            parameter = request.form['parameter']
            n = int(request.form['sample-size'])
            hypothesis = int(request.form['hypothesis'])
            test_value = float(request.form['test-value'])
            alpha = int(request.form['alpha'])

            print('done here!!!')

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
                result = variance_comformity_test(std, test_value, n, alpha, hypothesis)
            
            elif parameter == 'Proportion' :
                proportion = float(request.form['sample-mean'])
                result = proportion_comformity_test(proportion, test_value, n, alpha, hypothesis)
            
            if result :
                text = 'We can not reject H0'
            else :
                text = 'We reject H0'

        except Exception as e :
            return e
        
    return render_template('conformity-tests.html', result = text)

       

if __name__ == "__main__" :
    app.run(debug = True, port=5001)