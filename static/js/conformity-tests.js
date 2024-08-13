let parameter_select = document.querySelector('#parameter');
let parameters = document.querySelectorAll('.param');
let params_div = document.querySelector('#params');

let null_select = document.querySelector('#hypothesis-select');
let alternative_select = document.querySelector('#alternative-select');

let null_input = document.querySelector('#null-input')
let alternative_input = document.querySelector('#alternative-input')

let data_type = document.querySelector("#data-type");
let spreadsheet = document.querySelector("#spreadsheet");

let size = document.getElementById('sample-size');
let SD_select = document.querySelector('#SD-select');

let mean_label = document.querySelector('#mean-label');
let SD_label = document.querySelector('#SD-label');

let mean_div = document.querySelector('.mean');
let SD_div = document.querySelector('.standard-deviation');

let mean_inp = document.getElementById('sample_mean');
let std_inp = document.getElementById('SD');


data_type.addEventListener('change', function() {
    var selectedValue = this.value;

    if (selectedValue == 'param'){
        spreadsheet.style.display = 'none';
        /*
        mean_inp.disabled = false;
        std_inp.disabled = false;
        */
    }
    else {
        spreadsheet.style.display = 'block';
        /*
        mean_inp.disabled = true;
        std_inp.disabled = true;
        */
    }
});

parameter_select.addEventListener('change', function() {
    var selectedValue = parameter_select.value;

    switch(selectedValue) {
        case "Mean" :
            parameters[0].innerHTML = 'μ';
            parameters[1].innerHTML = 'μ';

            SD_select.disabled = false;

            mean_div.classList.remove('hidden');
            SD_div.classList.remove('hidden');
            mean_label.innerHTML = 'Sample Mean (x̄)';

            params_div.classList.remove('flex-end');
            break;
        case "Variance" :
            parameters[0].innerHTML = 'σ';
            parameters[1].innerHTML = 'σ';

            SD_select.value = 'no';
            SD_select.disabled = true;
            SD_label.innerHTML = 'Sample Standard Deviation (S)';

            mean_div.classList.add('hidden');
            SD_div.classList.remove('hidden');

            params_div.classList.add('flex-end');
            break;
        case "Proportion" :
            parameters[0].innerHTML = 'p';
            parameters[1].innerHTML = 'p';

            SD_select.disabled = true;
            SD_div.classList.add('hidden');
            mean_div.classList.remove('hidden');
            params_div.classList.remove('flex-end');
            mean_label.innerHTML = 'Estimated Proportion (p)';
            break;
        default :
            break;
    }
});

null_select.addEventListener('change', function() {
    var selectedValue = this.value;

    switch (selectedValue) {
        case '0' :
            alternative_select.value = 'ne';
            break;
        case '1' :
            alternative_select.value = 'gt';
            break;
        case '2' :
            alternative_select.value = 'lt';
            break;
    }
});

null_input.addEventListener('input', function() {
    alternative_input.value = null_input.value;
});

SD_select.addEventListener('change', function() {
    var selectedValue = this.value;

    switch (selectedValue) {
        case 'yes' :
            SD_label.innerHTML = 'Population Standard Deviation (σ)';
            break;
        case 'no' :
            SD_label.innerHTML = 'Sample Standard Deviation (S)';
            break;
        default :
            break;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    size.addEventListener('input', function() {
        spreadsheet.innerHTML = '';
        let n = parseInt(size.value);
        var arr = [new Array(n).fill('')];
        
        var H = new Handsontable(spreadsheet, {
            data: arr,
            colHeaders: true,
            rowHeaders: false,
            nestedHeaders: [
                [{label: 'Your Sample', colspan: n}]
            ],
            licenseKey: 'non-commercial-and-evaluation',
            cells: function (row, col) {
                var cellProperties = {};
                cellProperties.className = 'htCenter htMiddle';
                return cellProperties;
            }
        });

        H.addHook('afterChange', function(changes, source) {
            if (source == 'edit') {
                const choice = data_type.value;

                if (choice == 'data') {
                    var data = H.getData();
                    data = data.map(row => row.map(cell => cell === '' ? 0 : cell));
                    /*
                    const isFilled = data.every(row => row.every(cell => cell !== ''));

                    if (!isFilled) 
                        alert("All cells must be filled");
                    */
                    const tableData = {
                        data: data.flat()
                    };
                    
                    fetch('/get-table-data', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(tableData)
                    })
                    .then(response => {
                        return response.json();
                    })
                    .then(result => {
                        if (result.success) {
                            mean_inp.value = parseFloat(result.mean.toFixed(3));
                            std_inp.value = parseFloat(result.std.toFixed(3));
                        }
                        else {
                            console.log("Probleme here");
                        }
                    })
                }
            }
        });
    });

    const dataForm = document.getElementById('dataForm');
    const solution = document.getElementById('solution');

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
            const formBody = new URLSearchParams(formData).toString();

            fetch('/get-result', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formBody
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                solution.style.display = 'block';
                let formula = `\\( ${data.formula} \\)`;
                let region = `\\( ${data.critical_region} \\)`;
                let symbol = `\\( ${data.symbol} \\)`;
                let desc = `\\( ${data.desc} \\)`;
                let text = `\\( ${data.text} \\)`;
                solution.innerHTML = `
                    <div>
                        <h3>Solution :</h3>
                    </div>
                    <div>
                        <div>
                            <h5>Parameter : ${data.parameter}</h5>
                            <h5>Test type : ${data.test_type}</h5>
                            <h5>Test value : ${data.test_value}</h5>
                            <h5>Significance level α = ${data.alpha}</h5>
                        </div>
                        <div>
                            <h5>Statistic : ${formula}</h5>
                            <h5>Statistic value : ${data.stat_value}</h5>
                            <h5>Critical value : ${symbol}</h5>
                            <h5>Critical region : ${region}</h5>
                        </div>
                    </div>
                    <div>
                        <p>
                            ${desc}${text}
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
});
