// Select the login form
var loginForm = document.getElementById('loginForm');

// Add a 'submit' event listener
loginForm.addEventListener('submit', function(event) {
    // Get the username and password fields
    var username = document.getElementById('username');
    var password = document.getElementById('password');

    // Check if the username or password fields are empty
    if (!username.value || !password.value) {
        // If they are, show an error message and prevent the form from submitting
        alert('Please enter both a username and password.');
        event.preventDefault();
    }
});
