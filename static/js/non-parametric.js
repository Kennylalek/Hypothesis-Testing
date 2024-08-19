var test_select = document.querySelector('#test-select');
var sample_size_1 = document.querySelector('#sample-size-1');
var sample_size_2 = document.querySelector('#sample-size-2');
var second_div = document.querySelector('#second-div');
var first_label = document.querySelector('#first-label');
var test = document.querySelector('#test');
var H0 = document.querySelector('#H0');
var spreadsheets = document.querySelectorAll('.spreadsheet');

const dataForm = document.querySelector('#dataForm');
const solution = document.querySelector('#solution');

const errorLabels = document.querySelectorAll('.error-labels');

var hot1 = '';
var hot2 = '';

test_select.addEventListener('change', function() {
    spreadsheets[0].innerHTML = '';
    spreadsheets[1].innerHTML = '';
    var selectedValue = this.value;

    if (selectedValue == 'MW') {
        test.innerHTML = 'Mann-Whitney U test';
        second_div.style.display = 'block';
        first_label.innerHTML = 'First Sample Size (n<sub>2</sub>)';
    }
    else if (selectedValue == 'WI') {
        test.innerHTML = 'Wilcoxon signed-rank test';
        second_div.style.display = 'none';
        first_label.innerHTML = 'Sample Size (n)';
    }
});

sample_size_1.addEventListener('input', function() {
    spreadsheets[0].innerHTML = '';
    var n = parseInt(this.value);

    if (n >= 1) {
        spreadsheets[0].innerHTML = '';
        spreadsheets[0].style.display = 'block';

        if (test_select.value == 'MW') {
            var data = [new Array(n).fill('')];

            let wid = n * 100;

            let X = document.getElementById('rows').value;

            hot1 = new Handsontable(spreadsheets[0], {
                data: data,
                rowHeaders: false,
                colHeaders: true,
                width: (wid > 1000) ? '180%' : wid,
                height: 'auto',
                rowHeaderWidth: 'auto',
                licenseKey: 'non-commercial-and-evaluation',
                rowHeights: 30, 
                colWidths: 100,
                nestedHeaders: [
                    [{ label: X, colspan: n }]
                ],
                cells: function (row, col) {
                    var cellProperties = {};
                    cellProperties.className = 'htCenter htMiddle';
                    return cellProperties;
                }
            });
        }
        else {
            if (n >= 7) {
                var data = Array.from({ length: 2 }, () => Array(n).fill(''));

                let wid = n * 100 + 50;

                let X = document.getElementById('rows').value;
                let Y = document.getElementById('cols').value;

                hot1 = new Handsontable(spreadsheets[0], {
                    data: data,
                    rowHeaders: [X, Y],
                    colHeaders: true,
                    width: (wid > 1000) ? '180%' : wid,
                    height: 'auto',
                    rowHeaderWidth: 120,
                    licenseKey: 'non-commercial-and-evaluation',
                    rowHeights: 30, 
                    colWidths: 100,
                    nestedHeaders: [
                        [{ label: 'Samples', colspan: n }]
                    ],
                    cells: function (row, col) {
                        var cellProperties = {};
                        cellProperties.className = 'htCenter htMiddle';
                        return cellProperties;
                    }
                });
            }
        }
    }
    else {
        spreadsheets[0].style.display = 'none';
    }
});

sample_size_2.addEventListener('input', function() {
    spreadsheets[1].innerHTML = '';
    var n = parseInt(this.value);

    if (n >= 1) {
        spreadsheets[1].innerHTML = '';
        spreadsheets[1].style.display = 'block';

        if (test_select.value == 'MW') {
            var data = [new Array(n).fill('')];

            let wid = n * 100;

            let Y = document.getElementById('cols').value;

            hot2 = new Handsontable(spreadsheets[1], {
                data: data,
                rowHeaders: false,
                colHeaders: true,
                width: (wid > 1000) ? '180%' : wid,
                height: 'auto',
                rowHeaderWidth: 'auto',
                licenseKey: 'non-commercial-and-evaluation',
                rowHeights: 30, 
                colWidths: 100,
                nestedHeaders: [
                    [{ label: Y, colspan: n }]
                ],
                cells: function (row, col) {
                    var cellProperties = {};
                    cellProperties.className = 'htCenter htMiddle';
                    return cellProperties;
                }
            });
        }
    }
    else {
        spreadsheets[1].style.display = 'none';
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
        if (input.value === '' && input.parentElement.style.display != 'none' && !input.disabled) {
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

        var tableData_1 = hot1.getData();
        var tableData_2 = '';

        if (test_select.value == 'MW') {
            tableData_2 = hot2.getData();
        }

        console.log(tableData_1);
        console.log(tableData_2);

        const combineData = {
            form: formObject,
            table_1: tableData_1,
            table_2: tableData_2
        };

        fetch('/non-parametric', {
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
            solution.innerHTML = `
                <div>
                    <h3>Solution :</h3>
                </div>
                <div>
                    <div>
                        <h5>\\(${data.test == 'MW' ? 'First\\;sample\\;ranks\\;u_1 = ' : 'Positive\\;ranks\\;w_+ = '} ${data.v1}\\)</h5>
                        <h5>\\(${data.test == 'MW' ? 'Second\\;sample\\;ranks\\;u_2 = ' : 'Negative\\;ranks\\;w_- = '} ${data.v2}\\)</h5>
                        <h5>\\(${data.test == 'MW' ? 'Sample\\;sizes : n_1 = ' + data.n1 + '\\;n_2 = ' + data.n2 : 'Sample\\;size\\;n = ' + data.n1}\\)</h5>
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
            MathJax.typesetPromise();
            let div = solution.children[1];

            div.classList.add('final-solution');
            div.children[0].classList.add('half-div');
            div.children[1].classList.add('half-div');
            solution.scrollIntoView({behavior: "smooth"});
            
        })
        .catch(error => {
            console.error('Error fetching the result:', error);
            document.getElementById('result').innerHTML = 'An error has occurred.';
        });
    }
});
