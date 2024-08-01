let parameter_select = document.querySelector('#parameter');
let parameters = document.querySelectorAll('.param');

let null_select = document.querySelector('#hypothesis-select');
let alternative_select = document.querySelector('#alternative-select');

let null_input = document.querySelector('#null-input')
let alternative_input = document.querySelector('#alternative-input')

let SD_select = document.querySelector('#SD-select');
let SD_label = document.querySelector('#SD-label');
let mean_label = document.querySelector('#mean-label');

let mean_div = document.querySelector('.mean');
let SD_div = document.querySelector('.standard-deviation');

let params_div = document.querySelector('#params');

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

$(document).ready(function(){
    $('form').on('submit', function(event){
        event.preventDefault(); // Prevent the default form submission

        $.ajax({
            url: '/conformity-tests',
            method: 'POST',
            data: $(this).serialize(),
            success: function(){}
        });
    });
});