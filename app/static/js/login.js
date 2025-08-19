form = document.querySelector("form");
usernameElement = form.querySelector("#username");
passwordElement = form.querySelector("#password");
messagesContainer = form.querySelector(".messages");

messages = new Set();

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

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessages();

  const username = usernameElement.value;
  const password = passwordElement.value;

  if (username === "" || password === "") {
    messages.add("Please fill in all fields");
    updateMessages(messagesContainer);
  }

  const response = await fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });
  const responseJson = await response.json();

  if (response.ok) {
    window.location.href = "/deck";
    return;
  } else {
    const message = responseJson.message;
    messages.add(message);
  }
  updateMessages(messagesContainer);
});
