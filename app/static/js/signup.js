const form = document.querySelector("form");
const messagesContainer = form.querySelector(".messages");
const usernameElement = form.querySelector("#username");
const passwordElement = form.querySelector("#password");
const passwordConfirmElement = form.querySelector("#password_confirm");
const messages = new Set();

function updateMessages(messagesContainer) {
  if (messages.size == 0) {
    messagesContainer.innerHTML = "";
    return;
  }

  if (messagesContainer.childElementCount != messages.size) {
    messagesContainer.innerHTML = "";
    for (const message of messages) {
      const listElement = document.createElement("li");
      listElement.innerText = message;
      messagesContainer.appendChild(listElement);
    }
  }
}

function clearMessages() {
  messages.clear();
  updateMessages(messagesContainer);
}

function validateForm(username, password, passwordConfirm) {
  usernamePattern = /^[a-zA-Z0-9]+$/;
  if (username === "") {
    messages.add("Username cannot be empty");
  }
  if (username.length < 5) {
    messages.add("Username must be at least 5 characters long");
  }
  if (username.length > 20) {
    messages.add("Username must be at most 20 characters long");
  }
  if (!usernamePattern.test(username)) {
    messages.add("Username can only contain letters and numbers");
  }

  if (password === "") {
    messages.add("Password cannot be empty");
  }
  if (password.length < 5) {
    messages.add("Password must be at least 5 characters long");
  }
  if (password.length > 20) {
    messages.add("Password must be at most 20 characters long");
  }
  if (password !== passwordConfirm) {
    messages.add("Passwords do not match");
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessages();

  const username = usernameElement.value;
  const password = passwordElement.value.trim();
  const passwordConfirm = passwordConfirmElement.value;

  validateForm(username, password, passwordConfirm);

  if (messages.size > 0) {
    updateMessages(messagesContainer);
    return;
  }

  const response = await fetch("/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
      password_confirm: passwordConfirm,
    }),
  });
  const responseJson = await response.json();

  if (response.ok) {
    window.location.href = "/login";
    return;
  } else {
    const message = responseJson.message;
    messages.add(message);
  }
  updateMessages(messagesContainer);
});
