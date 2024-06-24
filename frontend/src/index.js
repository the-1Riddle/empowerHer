import "./style/style.scss";


/*const appDiv = document.getElementById("app");
appDiv.innerHTML = `<h1>${message}</h1>`;*/

const messageInput = document.getElementById('message');
const inputValue = messageInput.value;
console.log(inputValue); // Display the value in the console

    const signupButton = document.getElementById('signup-button');
    const signinButton = document.getElementById('signin-button');
    const registrationForm = document.getElementById('registration-form');
    const signinForm = document.getElementById('signin-form');

    signupButton.addEventListener('click', () => {
        registrationForm.style.display = 'block';
        signinForm.style.display = 'none';
    });

    signinButton.addEventListener('click', () => {
        signinForm.style.display = 'block';
        registrationForm.style.display = 'none';
    });
/*handle form submission
    const registrationForm = document.getElementById('registration-form');
    const signinForm = document.getElementById('signin-form');

    registrationForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission
        // Get form data and send it to your database
        // Example: You can use fetch() or an AJAX request
        // ...
    });

    signinForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission
        // Get form data and send it to your database
        // Example: You can use fetch() or an AJAX request
        // ...
    });
*/
//handle prompt
    const showPromptButton = document.getElementById('show-prompt');
    const messagePrompt = document.getElementById('message-container');

    showPromptButton.addEventListener('click', () => {
        messagePrompt.style.display = 'block'; // Show the prompt
    });

