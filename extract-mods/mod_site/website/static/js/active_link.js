// JavaScript to highlight the active link in the menu

// Get the current page's URL path
const currentPage = window.location.pathname;

// Select all navigation links
const navLinks = document.querySelectorAll('.navbar a');

// Loop through each link and check if it matches the current page
navLinks.forEach(link => {
    // Check if the link's href matches the current page
    if (link.getAttribute('href') === currentPage) {
        link.classList.add('active'); // Add active class if it matches
    }
});
