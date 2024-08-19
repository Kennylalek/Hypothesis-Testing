var parameter = document.querySelector('#parameter');
var test_type = document.querySelector('#test-type');
var sample_size_div = document.querySelector('.indp-mean');
var sample_size_input = document.querySelector('#sample-size');
var sample_count_input = document.querySelector('#sample-count');
var test = document.querySelector('#test');
var H0 = document.querySelector('#H0');
var spreadsheet = document.querySelector('#spreadsheet');

const dataForm = document.querySelector('#dataForm');
const solution = document.querySelector('#solution-multiple');

const errorLabels = document.querySelectorAll('.error-labels');

var hot = '';

parameter.addEventListener('change', function() {
    var selectedValue = this.value;

    if (selectedValue == 'mean') {
        test_type.disabled = false;

        if (test_type.value == 'parametric') {
            test.innerHTML = 'Analysis of Variance (ANOVA)';
        }
        else {
            test.innerHTML = 'Kruskal-Wallis Test';
        }
        H0.innerHTML = `H<sub>0</sub>  : The samples' means are equal`;
    }
    else if (selectedValue == 'variance') {
        test_type.disabled = true;
        test.innerHTML = 'Bartlett Test';
        H0.innerHTML = `H<sub>0</sub>  : The samples' variances are equal`;
    }
});

test_type.addEventListener('change', function() {
    if (parameter.value == 'mean') {
        var selectedValue = this.value;

        if (selectedValue == 'parametric') {
            test.innerHTML = 'Analysis of Variance (ANOVA)';
        }
        else {
            test.innerHTML = 'Kruskal-Wallis Test';
        }
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
        if (input.value === '' && !input.parentElement.classList.contains('hidden') && !input.disabled) {
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
        tableData = tableData[0].map((_, colIndex) => tableData.map(row => row[colIndex]));

        tableData = tableData.filter(row => row.some(cell => cell !== null && cell !== ''));

        // Optionally, remove empty cells within each row
        tableData = tableData.map(row => row.filter(cell => cell !== null && cell !== ''));

        console.log(tableData);

        const combineData = {
            form: formObject,
            table: tableData
        };

        fetch('/multiple-samples', {
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
            solution.style.display = 'block';

            let test = data.t;
            console.log(test);

            if (test == 'ANOVA') {
                solution.innerHTML = `
                    <table>
                        <caption>ANOVA Table</caption>
                        <thead>
                            <tr>
                                <th>Source of Variation</th>
                                <th>Sum of Squares (SS)</th>
                                <th>Degrees of Freedom (df)</th>
                                <th>Mean Square</th>
                                <th>F-value</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Between Groups</td>
                                <td>\\( nS_F^2 = ${data.SF} \\)</td>
                                <td>\\(k - 1 = ${data.k - 1} \\)</td>
                                <td>\\(${(data.SF / (data.k - 1)).toFixed(3)} \\) </td>
                                <td rowspan="3">\\( ${data.formula} = ${data.stat_value}\\)</td>
                            </tr>
                            <tr>
                                <td>Within Groups</td>
                                <td>\\( nS_R^2 = ${data.SR} \\)</td>
                                <td>\\(n - k = ${data.n - data.k} \\)</td>
                                <td>\\(${(data.SR / (data.n - data.k)).toFixed(3)}\\) </td>
                            </tr>
                            <tr>
                                <td>Total</td>
                                <td>\\(nS^2 = ${data.S} \\)</td>
                                <td>\\(n - 1 = ${data.n - 1}\\)</td>
                                <td></td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>\\(Critical\\;value : ${data.symbol} \\)</h5>
                    <div>
                        <p>
                            \\(${data.desc}${data.text}\\)
                        </p>
                    </div>
                `;
            }
            else {
                solution.innerHTML = `
                    <div>
                        <h3>Solution :</h3>
                        <h5>\\(Statistic : ${data.formula} \\)</h5>
                        ${test == 'Bartlett' ? `<h5>\\(With :  ${data.lambda} \\)</h5>` : ''}
                    </div>
                    <div>
                        <div>
                            <h5>\\(Total\\;Size\\;n = ${data.n}\\)</h5>
                            <h5>\\(Number\\;of\\;Samples\\;k = ${data.k}\\)</h5>
                            <h5>\\(Significance\\;level\\;\\alpha = ${data.alpha}\\)</h5>
                        </div>
                        <div>
                            
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
            
            MathJax.typesetPromise();
            solution.scrollIntoView({behavior: "smooth"});
            
        })
        .catch(error => {
            console.error('Error fetching the result:', error);
            document.getElementById('result').innerHTML = 'An error has occurred.';
        });
    }
});

sample_count_input.addEventListener('input', generate_table);
sample_size_input.addEventListener('input', generate_table);

function generate_table() {
    var rows = parseInt(sample_size_input.value);
    var columns = parseInt(sample_count_input.value);

    if (rows > 0 && columns > 0) {
        spreadsheet.innerHTML = '';
        spreadsheet.style.display = 'block';
        let wid = columns * 100 + 50;
    
        var data = Array.from({ length: rows }, () => Array(columns).fill(''));

        const headers = Array.from({ length: columns }, (_, i) => `Sample ${i + 1}`);
        
        hot = new Handsontable(spreadsheet, {
            data: data,
            rowHeaders: true,
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

