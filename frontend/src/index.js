import "./style/style.scss";
document.getElementById('services').addEventListener('change', function() {
    var selectedValue = this.value;
    if (selectedValue !== '') {
      window.location.href = selectedValue;
    }
  });

/*const appDiv = document.getElementById("app");
appDiv.innerHTML = `<h1>${message}</h1>`;*/

const messageInput = document.getElementsByClassName('message');
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

//handle prompt
    const messages = []; //array to store messages
    document.getElementById('submit-message').addEventListener('click', function () {
        const messageInput = document.getElementById('message-input');
        const messageText = messageInput.value.trim();
      
        if (messageText) {
          messages.push(messageText);
          // Clear the input fielssd
          messageInput.value = '';
        }

        const messageBoard = document.getElementById('message-board');
        const newMessage = document.createElement('div');
        newMessage.className = 'message';
        newMessage.textContent = messageText; // Display the user's message
        messageBoard.appendChild(newMessage);
      });
     
  //dropdown
document.getElementById('services').addEventListener('change', function() {
    var selectedValue = this.value;
    if (selectedValue !== '') {
      window.location.href = selectedValue;
    }
  });
//health checks

   
