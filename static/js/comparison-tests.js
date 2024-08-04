var parameter_select = document.querySelector('#parameter');
var hypothesis_divs = document.querySelectorAll('.inputs-2');

var null_select = document.querySelector('.hypothesis-select');
var alternative_select = document.querySelector('.alternative-select');

var data_type = document.querySelector('#data-type');
var spreadsheets = document.querySelectorAll('.spreadsheet');
var size_inputs = document.querySelectorAll('.size');


var mean_div = document.querySelector('#mean-div');
var std_div = document.querySelector('#std-div');

var mean_inputs = document.querySelectorAll('.mean-inp');
var std_inputs = document.querySelectorAll('.std-inp');
var std_select = document.querySelector('#SD-select');

const dataForm = document.querySelector('#dataForm');
const solution = document.querySelector('#solution');

const errorLabels = document.querySelectorAll('.error-labels');

parameter_select.addEventListener('change', function() {
    const selectedValue = this.value;

    switch(selectedValue) {
        case 'Mean' :
            add_symbol('μ');
            std_select.disabled = false;
            mean_div.classList.remove('hidden');
            std_div.classList.remove('hidden');
            add_text(' Sample Ean (x̄', mean_div);
            break;
        case 'Variance' :
            add_symbol('σ');
            mean_div.classList.add('hidden');
            std_div.classList.remove('hidden');
            add_text(' Sample Std Dev (σ', std_div);
            std_select.value = 'no';
            std_select.disabled = true;
            break;
        case 'Proportion' :
            add_symbol('p');
            std_select.disabled = true;
            mean_div.classList.remove('hidden');
            std_div.classList.add('hidden');
            add_text(' Estimated Proportion (p', mean_div);
            break;
    }
});

std_select.addEventListener('change', function() {
    var selectedValue = this.value;
    console.log(this);
    switch(selectedValue) {
        case 'yes' :
            add_text(' Population Std Dev (σ', std_div);
            break;
        case 'no' :
            add_text(' Sample Std Dev (σ', std_div);
            break;
        default :
            break;
    }
});

null_select.addEventListener('change', function() {
    let selectedValue = this.value;
    console.log(selectedValue);
    console.log(alternative_select.value);
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

data_type.addEventListener('change', function() {
    var selectedValue = this.value;

    spreadsheets.forEach(spreadsheet => {
        if (selectedValue == 'param'){
            spreadsheet.style.display = 'none';
        }
        else {
            spreadsheet.style.display = 'block';
        }
    });
});


for (let i = 0; i <= 1; i++) {
    size_inputs[i].addEventListener('input', function() {
        spreadsheets[i].innerHTML = '';
        let n = parseInt(this.value);
        var arr = [new Array(n).fill('')];
        var desc = ['First', 'Second'];

        var hot = new Handsontable(spreadsheets[i], {
            data: arr,
            colHeaders: true,
            rowHeaders: false,
            nestedHeaders: [
                [{label: desc[i] + ' Sample', colspan: n}]
            ],
            licenseKey: 'non-commercial-and-evaluation'
        });

        hot.addHook('afterChange', function(chnages, source) {
            if (source == 'edit') {
                const choice = data_type.value;

                if (choice == 'data') {
                    var data = hot.getData();
                    data = data.map(row => row.map(cell => cell ==='' ? 0 : cell));
                }
                else {
                    spreadsheets[i].style.display = 'none';
                }

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
                        document.querySelectorAll('.mean-inp')[i].value = parseFloat(result.mean.toFixed(3));
                        document.querySelectorAll('.std-inp')[i].value = parseFloat(result.std.toFixed(3));
                    }
                    else {
                        console.log('Error');
                    }
                })
            }
        });
    });
}

dataForm.addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('result').innerHTML = '';
    let allFilled = true;

    const inputsAndSelects = document.querySelectorAll('input, select');

    errorLabels.forEach(input => input.classList.remove('error'));

    inputsAndSelects.forEach(input => {
        if (input.value === '' && input.parentElement.classList.contains('hidden')) {
            input.classList.add('error');
            const errorLabel = input.nextElementSibling;

            if (errorLabel && errorLabel.classList,contains('error')) {
                errorLabel.style.display = 'block';
            }

            allFilled = false;
        }
    });

    if (allFilled) {
        const formData = new FormData(dataForm);
        const formBody = new URLSearchParams(formData).toString();

        fetch('/get-params', {
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

document.querySelectorAll('input, select').forEach(element => {
    element.addEventListener('focus', function() {
        this.classList.remove('error');
        const errorLabel = this.nextElementSibling;
        if (errorLabel && errorLabel.classList.contains('error-label')) {
            errorLabel.style.display = 'none';
        }
    });

    element.addEventListener('change', function() {
        this.classList.remove('error');
        const errorLabel = this.nextElementSibling;
        if (errorLabel && errorLabel.classList.contains('error-label')) {
            errorLabel.style.display = 'none';
        }
    });
});

document.querySelector('#scroll').addEventListener("click", function() {
    let container = document.getElementById("container");
    let offset = 30;

    var elementPosition = container.getBoundingClientRect().top + window.scrollY;
    var offsetPosition = elementPosition - offset;

    window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
});

function add_symbol(symbol) {
    for(let i = 0; i <= 1; i++) {
        let j = 1;
        hypothesis_divs[i].querySelectorAll('p').forEach(p => {
            p.innerHTML = symbol + '<sub>' + j++ +'</sub>'
        });
    }
}

function add_text(text, div) {
    let j = 1;
    let texts = ['First', 'Second'];
    div.querySelectorAll('.label').forEach(label => {
        label.innerHTML = texts[j - 1] + text + "<sub>" + j++ + "</sub>)";
    });
}