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