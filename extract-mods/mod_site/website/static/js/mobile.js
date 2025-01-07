// Select the menu button and the nav links container
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

// Toggle 'show' class on nav links when menu button is clicked
menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('show');
});
