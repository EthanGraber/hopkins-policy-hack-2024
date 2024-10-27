const fileInput = document.getElementById('file-input');
const uploadButton = document.getElementById('upload-button');
const messageBox = document.getElementById('message');

// script.js (relevant parts)
const notificationButton = document.getElementById('notification-button');

notificationButton.addEventListener('click', (event) => {
  fetch("/send-test-notification", {
    method: "GET"
  })
  .then(response => response.json())
  .then(data => {
    const timestamp = new Date().toLocaleTimeString();
    messageBox.innerHTML += `${timestamp} ${data.message}<br>`;
  })
  .catch(error => {
    const timestamp = new Date().toLocaleTimeString();
    messageBox.innerHTML += `${timestamp} Error: ${error}<br>`;
  });
});


// Set the message box font to monospace
messageBox.style.fontFamily = 'monospace';

uploadButton.addEventListener('click', (event) => {
  event.preventDefault();
  fileInput.click();
});

fileInput.addEventListener('change', (event) => {
  // Get the selected file
  const file = event.target.files[0];
  const formData = new FormData();
  formData.append("file", file);
  // Send the file to the server
  fetch("/upload", {
    method: "POST",
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // Get the current timestamp
    const timestamp = new Date().toLocaleTimeString();
    
    // Append the message to the #message box on a new line
    messageBox.innerHTML += `${timestamp} ${data.message || data.error}<br>`;
  })
  .catch(error => {
    // Get the current timestamp
    const timestamp = new Date().toLocaleTimeString();
    
    // Append the error message to the #message box on a new line
    messageBox.innerHTML += `${timestamp} Error: ${error}<br>`;
  });

});
