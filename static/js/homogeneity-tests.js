var test_select = document.getElementById('test-select');
var distribution = document.getElementById('distribution');

var test = document.getElementById('test');
var distribution_name = document.getElementById('distribution-name');

var dimensions = document.getElementById('dimensions');
var data_type = document.querySelector('#data-type');
var size_label = document.getElementById('size-label');
var size_input = document.getElementById('sample-size');

var param = document.getElementById('param');
var parameters = document.getElementById('parameters');
var std = document.querySelector('.standard-deviation');

var spreadsheet = document.getElementById('spreadsheet');
const dataForm = document.querySelector('#dataForm');
const solution = document.querySelector('#solution');

const errorLabels = document.querySelectorAll('.error-labels');

var hot = '';


test_select.addEventListener('change', function () {
    var selectedValue = this.value;

    switch (selectedValue) {
        case 'Chi-Square' :
            test.innerHTML = 'Chi-Square Test for Homogeneity';
            distribution.disabled = false;
            data_type.value = 'classes';
            data_type.disabled = true;
            dimensions.style.display = 'flex';
            size_label.innerHTML = 'Number of Classes (k)';
            break;
        case 'Kolmogorov-Sminrov' :
            test.innerHTML = 'Kolmogorov-Sminrov Test';
            distribution.disabled = false;
            data_type.disabled = false;
            break;
        case 'Normality' :
            test.innerHTML = 'Normality Test';
            distribution.value = 'a Normal';
            distribution.disabled = true;
            data_type.disabled = false;
            distribution_name.innerHTML = 'a Normal';
            break;
        default :
            break;
    }
});

distribution.addEventListener('change', function() {
    var selectedValue = this.value;
    distribution_name.innerHTML = selectedValue;

    if (selectedValue == 'a Poisson') {
        std.style.display = 'none';
    }
    else {
        std.style.display = 'block';
    }
});

data_type.addEventListener('change', function() {
    var selectedValue = this.value;

    if (selectedValue == 'classes') {
        dimensions.style.display = 'flex';
        size_label.innerHTML = 'Number of Classes (k)';
    }
    else {
        dimensions.style.display = 'none';
        size_label.innerHTML = 'Sample Size (n)';
    }
});

param.addEventListener('change', function() {
    var selectedValue = this.value;

    if (selectedValue == 'given') {
        parameters.style.display = 'flex';
    }
    else {
        parameters.style.display = 'none';
    }
});

size_input.addEventListener('input', function() {
    var val = data_type.value;

    if (val == 'raw') {
        var selectedValue = parseInt(this.value);

        if (selectedValue > 0) {
            spreadsheet.innerHTML = '';
            spreadsheet.style.display = 'block';
            data = [new Array(selectedValue).fill('')];

            let wid = selectedValue * 100 + 50;

            hot = new Handsontable(spreadsheet, {
            data: data,
            rowHeaders: false,
            colHeaders: true,
            width: (wid > 1000) ? '180%' : wid,
            height: 'auto',
            rowHeaderWidth: 160,
            licenseKey: 'non-commercial-and-evaluation',
            rowHeights: 30, 
            colWidths: 120,
            nestedHeaders: [
                [{ label: 'Sample', colspan: selectedValue }]
            ],
            cells: function (row, col) {
                var cellProperties = {};
                cellProperties.className = 'htCenter htMiddle';
                return cellProperties;
            }
            });
        }
        else {
            spreadsheet.innerHTML = '';
        }
    }
    else {
        generate_table();
    }
});

dataForm.addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('result').innerHTML = '';
    let allFilled = true;

    const errorLabels = document.querySelectorAll('.error-label');
    const inputsAndSelects = document.querySelectorAll('input, select');
    
    errorLabels.forEach(label => label.style.display = 'none');
    inputsAndSelects.forEach(input => input.classList.remove('error'));

    inputsAndSelects.forEach(input => {
        if (input.value === '' && input.parentElement.parentElement.style.display != 'none' && !input.disabled) {
            input.classList.add('error');
            const errorLabel = input.nextElementSibling;
            if (errorLabel && errorLabel.classList.contains('error-label')) {
                errorLabel.style.display = 'block';
            }
            allFilled = false;
        }
    });

    if (allFilled) {
        const formData = new FormData(dataForm);
        const formObject = {};
        formData.forEach((value, key) => formObject[key] = value);

        var tableData = hot.getData();

        const combineData = {
            form: formObject,
            table: tableData
        };

        fetch('/homogeneity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(combineData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.alpha);
            
            solution.style.display = 'block';
            let appliquable = data.appliquable;

            if (appliquable == 'yes') {

            

                solution.innerHTML = `
                    <div>
                        <h3>Solution :</h3>
                    </div>
                    <div>
                        <div>
                            <h5>\\(Test\\;used : ${data.test}\\)</h5>
                            <h5>\\(Distribution : ${data.dist} \\)</h5>
                            <h5>\\(Sample\\;size\\;n =  ${data.n}\\)</h5>
                            <h5>\\(Significance\\;level\\; \\alpha = ${data.alpha}\\)</h5>
                        </div>
                        <div>
                            <h5>\\(Statistic : ${data.formula}\\)</h5>
                            <h5>\\(Statistic\\;value : ${data.stat_value}\\)</h5>
                            <h5>\\(Critical\\;value : ${data.symbol}\\)</h5>
                            <h5>\\(Critical\\;region : ${data.critical_region}\\)</h5>
                        </div>
                    </div>
                    <div>
                        <p>
                            \\(${data.desc}${data.text}\\)
                        </p>
                    </div>
                `;

                let div = solution.children[1];

                div.classList.add('final-solution');
                div.children[0].classList.add('half-div');
                div.children[1].classList.add('half-div');
            }
            else {
                solution.innerHTML = `
                    <div>
                        <h5>The sample does not satisfy the conditions for the test to be applied</h5>
                        <h5>\\( \\forall i,j, C_{ij} > 5 \\)</div>
                    </div>
                `;
            }
            MathJax.typesetPromise();
            
            solution.scrollIntoView({behavior: "smooth"});
            
        })
        .catch(error => {
            console.error('Error fetching the result:', error);
            document.getElementById('result').innerHTML = 'An error has occurred.';
        });
    }
});

document.querySelector('#initial').addEventListener('input', generate_table);
document.querySelector('#range').addEventListener('input', generate_table);

function generate_table() {
    var initial_value = parseFloat(document.querySelector('#initial').value);
    var range = parseFloat(document.querySelector('#range').value);
    var k = parseInt(size_input.value);

    if (range > 0 && k > 0) {
        spreadsheet.innerHTML = '';
        spreadsheet.style.display = 'block';
        let wid = k * 100 + 50;

        var headers = [];

        if (distribution.value == 'a Poisson') {
            for (let i = initial_value; i <= k + initial_value; i++) {
                headers.push(i);
            }
        }
        else {
            for (let i = 0; i < k; i++) {
                let start = Math.round((initial_value + i * range) * 100) / 100;
                let end = Math.round((initial_value + (i + 1) * range) * 100) / 100;
                headers.push(`[${start}, ${end}[`);
            }
        }
    
        var data = [new Array(k).fill('')];
        
        hot = new Handsontable(spreadsheet, {
            data: data,
            rowHeaders: ['Freq'],
            colHeaders: headers,
            width: (wid > 1000) ? '150%' : wid,
            height: 'auto',
            rowHeights: 30,
            colWidths: 100,
            licenseKey: 'non-commercial-and-evaluation',
            cells: function (row, col) {
                var cellProperties = {};
                cellProperties.className = 'htCenter htMiddle';
                return cellProperties;
            }
        });
    }
    else {
        spreadsheet.style.display = 'none';
    }
}
