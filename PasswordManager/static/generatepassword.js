var clipboard = new ClipboardJS('.copy', {
    container: document.getElementById('newPassword')
});

var lowercase = "abcdefghijklmnopqrstuvwxyz",
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    numbers = "0123456789",
    punctuation = "!@#$%^&*()_+~`|}{[]:;?><,./-=",
    lowercaseInput = true,
    uppercaseInput = true,
    punctuationInput = true,
    numbersInput = true,
    lengthInput = document.getElementById("length"),
    passwordField = document.getElementById("password-here"),
    generateButton = document.getElementById("generate"),
    copyButton = document.getElementById("copy"),
    plength,
    userPassword,
    passwordCharSet;

function generate() {
    userPassword = "";
    passwordCharSet = "";
    if (lowercaseInput == true) {
        passwordCharSet += lowercase;
    }
    if (uppercaseInput == true) {
        passwordCharSet += uppercase;
    }
    if (punctuationInput == true) {
        passwordCharSet += punctuation;
    }
    if (numbersInput == true) {
        passwordCharSet += numbers;
    }
    plength = Number(lengthInput.value);

    for (let i = 0; i < plength; i++) {
        userPassword += passwordCharSet.charAt(
            Math.floor(Math.random() * passwordCharSet.length)
        );
    }

    passwordField.innerHTML = userPassword;

    copyButton.setAttribute("data-clipboard-action", "copy");
    copyButton.setAttribute("data-clipboard-text", userPassword);
}

generateButton.addEventListener("click", generate);

clipboard.on('success', function (e) {
    console.info('Action:', e.action);
    console.info('Text:', e.text);
    console.info('Trigger:', e.trigger);
    let alertbox = document.getElementById('alert');
    alertbox.innerHTML = "Copied!";
    alertbox.classList.add('success');
    setTimeout(function () {
        alertbox.classList.remove('success');
    }, 3000);

    e.clearSelection();
});

clipboard.on('error', function (e) {
    console.error('Action:', e.action);
    console.error('Trigger:', e.trigger);
    let alertbox = document.getElementById('alert');
    alertbox.innerHTML = "Try select the text to copy";
    alertbox.classList.add('fail');
    setTimeout(function () {
        alertbox.classList.remove('fail');
    }, 3000);
});