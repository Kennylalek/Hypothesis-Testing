let parameter_select = document.querySelector('#parameter');
let parameters = document.querySelectorAll('.param');

let null_select = document.querySelector('#hypothesis-select');
let alternative_select = document.querySelector('#alternative-select');

let null_input = document.querySelector('#null-input')
let alternative_input = document.querySelector('#alternative-input')

let data_type = document.querySelector("#data-type");
let spreadsheet = document.querySelector("#spreadsheet");

let SD_select = document.querySelector('#SD-select');
let SD_label = document.querySelector('#SD-label');
let mean_label = document.querySelector('#mean-label');

let mean_div = document.querySelector('.mean');
let SD_div = document.querySelector('.standard-deviation');

let params_div = document.querySelector('#params');

data_type.addEventListener('change', function() {
    var selectedValue = this.value;

    if (selectedValue == 'param'){
        spreadsheet.innerHTML = '';
        spreadsheet.style.display = 'none';
    }
    else {
        let n = parseInt(document.getElementById('sample-size').value);
        console.log(n);
        console.log(typeof(n));
        const arr = [new Array(n).fill('')];

        var hot = new Handsontable(spreadsheet, {
            data: arr,
            colHeaders: true,
            rowHeaders: false,
            nestedHeaders: [
                {label: 'data', colspan: n}
            ],
            licenseKey: 'non-commercial-and-evaluation'
        });
        spreadsheet.style.display = 'block';
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
    const dataForm = document.getElementById('dataForm');
    const solution = document.getElementById('solution');

    dataForm.addEventListener('submit', function(event) {
        event.preventDefault();
        let allFilled = true;
        const errorLabels = document.querySelectorAll('.error-label');
        const inputsAndSelects = document.querySelectorAll('input, select');
        
        errorLabels.forEach(label => label.style.display = 'none');
        inputsAndSelects.forEach(input => input.classList.remove('error'));

        inputsAndSelects.forEach(input => {
            if (input.value === '' && !input.parentElement.classList.contains('hidden')) {
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
                document.getElementById('result').innerText = 'An error has occurred.';
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
});

document.querySelector('#scroll').addEventListener("click", function() {
    let container = document.getElementById("container");
    let offset = 30;

    var elementPosition = container.getBoundingClientRect().top + window.scrollY;
    var offsetPosition = elementPosition - offset;

    window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
});

/*
$(document).ready(function(){
    $('#dataForm').submit(function(event){
        event.preventDefault();
        let allFilled = true;
        $('.error-label').hide();
        $('input, select').removeClass('error');

        $('input, select').each(function() {
            if ($(this).val() == '') {
                $(this).addClass('error');
                $(this).next('.error-label').show();
                allFilled = false;
            }
        });

        if (allFilled) {
            $('#solution').show();
            $.post("/get-result", $(this).serialize())
            .done(function(data){
                $("#solution").html(`
                    <div>
                        <h2>Solution :</h2>
                    </div>
                    <div>
                        <h5>Parameter : ${data.parameter}</h5>
                        <h5>Test type : ${data.test_type}</h5>
                        <h5>Test value : ${data.test_value}</h5>
                        <h5>Significance level α = ${data.alpha}</h5>
                    </div>
                    <div>
                        <h5>Statistic : ${data.formula}</h5>
                        <h5>Statistic value : ${data.stat_value}</h5>
                        <h5>Critical value : ${data.critical_value}</h5>
                    </div>
                `);
            })
            .fail(function() {
                $("#result").html("An error has occurred.");
            });
            MathJax.typeset();
        } 
    });

    $('input, select').on('focus change', function() {
        $(this).removeClass('error');
        $(this).next('.error-label').hide();
    })
});
*/
