// Function to validate Full Name (Alphabets only)
function validateFullName() {
    const fullNameInput = document.getElementById("full-name");
    const fullNameValue = fullNameInput.value;
    const isValid = /^[A-Za-z\s]+$/.test(fullNameValue);
    // Display an error message or apply styling based on `isValid`
}

// Function to validate Username (No special characters)
function validateUsername() {
    const usernameInput = document.getElementById("username");
    const usernameValue = usernameInput.value;
    const isValid = /^[A-Za-z0-9]+$/.test(usernameValue);
    // Display an error message or apply styling based on `isValid`
}

// Function to validate Phone Number (10 digits)
function validatePhoneNumber() {
    const phoneInput = document.getElementById("phone");
    const phoneValue = phoneInput.value;
    const isValid = /^\d{10}$/.test(phoneValue);
    // Display an error message or apply styling based on `isValid`
}

// Function to validate Email
function validateEmail() {
    const emailInput = document.getElementById("email");
    const emailValue = emailInput.value;
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValue);
    // Display an error message or apply styling based on `isValid`
}

// Function to validate Password (At least one capital letter, one small letter, one special character, minimum 6 characters)
function validatePassword() {
    const passwordInput = document.getElementById("password");
    const passwordValue = passwordInput.value;
    const isValid = /^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])(?=.{6,})/.test(passwordValue);
    // Display an error message or apply styling based on `isValid`
}

// Function to validate Confirm Password (Match with Password)
function validateConfirmPassword() {
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm-password");
    const passwordValue = passwordInput.value;
    const confirmPasswordValue = confirmPasswordInput.value;
    const isValid = passwordValue === confirmPasswordValue;
    // Display an error message or apply styling based on `isValid`
}

// Event listeners for real-time validation
document.getElementById("full-name").addEventListener("input", validateFullName);
document.getElementById("username").addEventListener("input", validateUsername);
document.getElementById("phone").addEventListener("input", validatePhoneNumber);
document.getElementById("email").addEventListener("input", validateEmail);
document.getElementById("password").addEventListener("input", validatePassword);
document.getElementById("confirm-password").addEventListener("input", validateConfirmPassword);
