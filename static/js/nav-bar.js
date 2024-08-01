document.addEventListener('scroll', function() {
    var navbar = document.getElementById('navbar');
    if (window.scrollY > 0) {
        navbar.classList.add('navbar-scrolled');
      navbar.classList.remove('navbar-default');
    } else {
      navbar.classList.add('navbar-default');
      navbar.classList.remove('navbar-scrolled');
    }
  });