window.addEventListener('scroll', function() {
    var targetElement = document.querySelector('.header_nav');
    var scrollPosition = window.scrollY;

    if (scrollPosition >= targetElement.offsetHeight) {
        targetElement.classList.add('bg-white');
        targetElement.classList.add('sticky-top');
        targetElement.classList.add('shadow-sm');
    } else {
        targetElement.classList.remove('bg-white');
        targetElement.classList.remove('sticky-top');
        targetElement.classList.remove('shadow-sm');
    }
});