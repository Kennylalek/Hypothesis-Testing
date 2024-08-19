var character_type = document.querySelector('#character');
var test_type = document.querySelector('#test-type');
var dimensions_div = document.querySelector('#dimensions');
var sample_size_div = document.querySelector('.indp-mean');
var sample_size_input = document.querySelector('#sample-size');
var test = document.querySelector('#test');
var H0 = document.querySelector('#H0');
var spreadsheet = document.querySelector('#spreadsheet');

const dataForm = document.querySelector('#dataForm');
const solution = document.querySelector('#solution');

const errorLabels = document.querySelectorAll('.error-labels');

var hot = '';

character_type.addEventListener('change', function() {
    spreadsheet.innerHTML = '';
    var selectedValue = this.value;

    if (selectedValue == 'qualitative') {
        test_type.disabled = true;
        sample_size_input.disabled = true;
        dimensions_div.style.display = 'flex';
        test.innerHTML = 'Categorical Variables Test';
        H0.innerHTML = 'H<sub>0</sub>  : The two characters are independent';
        document.getElementById('rows-label').innerHTML = 'Number of Rows';
        document.getElementById('cols-label').innerHTML = 'Number of Columns';
    }
    else if (selectedValue == 'quantitative') {
        test_type.disabled = false;
        document.getElementById('rows-label').innerHTML = 'First Character Name';
        document.getElementById('cols-label').innerHTML = 'Second Character Name';

        sample_size_input.disabled = false;
        sample_size_input.value = '';

        if (test_type.value == 'parametric') {
            test.innerHTML = 'Null Correlation Test';
        }
        else {
            test.innerHTML = 'Spearman Test';
        }
    }
});

test_type.addEventListener('change', function() {
    if (character_type.value == 'quantitative') {
        var selectedValue = this.value;

        if (selectedValue == 'parametric') {
            test.innerHTML = 'Null Correlation Test';
        }
        else {
            test.innerHTML = 'Spearman Test';
        }
    }
});

sample_size_input.addEventListener('input', function() {
    if (character_type.value == 'quantitative') {
        spreadsheet.innerHTML = '';
        var n = parseInt(this.value);

        if (n >= 1) {
            spreadsheet.innerHTML = '';
            spreadsheet.style.display = 'block';

            var data = Array.from({ length: 2 }, () => Array(n).fill(''));

            let wid = n * 100 + 50;

            let X = document.getElementById('rows').value;
            let Y = document.getElementById('cols').value;

            hot = new Handsontable(spreadsheet, {
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
                    [{ label: 'Sample', colspan: n }]
                ],
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

        const combineData = {
            form: formObject,
            table: tableData
        };

        fetch('/independence', {
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
            let char = data.character;
            let appliquable = data.appliquable;

            if (appliquable == 'yes') {
                solution.innerHTML = `
                    <div>
                        <h3>Solution :</h3>
                    </div>
                    <div>
                        <div>
                            <h5>\\(${char == 'qualitative' ? 'Rows' : 'First\\;Character'} : ${data.rows} \\)</h5>
                            <h5>\\(${char == 'qualitative' ? 'Columns' : 'Second\\;Character'} : ${data.cols}\\)</h5>
                            <h5>\\(Degrees\\;of\\;Freedom : ${data.dof}\\)</h5>
                            <h5>\\(Significance\\;level\\;\\alpha = ${data.alpha}\\)</h5>
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

document.getElementById('rows').addEventListener('input', generate_table);
document.getElementById('cols').addEventListener('input', generate_table);

function generate_table() {
    var rows = parseInt(document.querySelector('#rows').value);
    var columns = parseInt(document.querySelector('#cols').value);

    if (rows > 0 && columns > 0) {
        spreadsheet.innerHTML = '';
        spreadsheet.style.display = 'block';
        let wid = columns * 100 + 50;
    
        var data = Array.from({ length: rows }, () => Array(columns).fill(''));
        
        hot = new Handsontable(spreadsheet, {
            data: data,
            rowHeaders: true,
            colHeaders: true,
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

