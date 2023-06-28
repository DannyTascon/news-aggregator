// get the elements
const navbarToggle = document.querySelector('.navbar-toggle');
const navbarCollapse = document.querySelector('.navbar-collapse');

// toggle navbarCollapse when navbarToggle is clicked
navbarToggle.addEventListener('click', () => {
  navbarCollapse.classList.toggle('show');
});

// hide navbarCollapse when window is resized
window.addEventListener('resize', () => {
  if (window.innerWidth > 768) {
    navbarCollapse.classList.remove('show');
  }
});
