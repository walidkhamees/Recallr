const messages = new Set();
const speicalCharactersPattern = /\w*[\[\]\<\>\/\?\\:\*\|\s\&\+]+\w*/;

let selectedDeck = {};

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

// create new deck
const createDeckModal = document.querySelector("#create-deck-modal");
const createDeckNameInput = document.querySelector("#input-deck-name");
const createDeckMessages = document.querySelector("#create-deck-messages");
const createDeckSubmitBtn = document.querySelector("#submit-create-deck-btn");

const createDeckBtn = document.querySelector("#new-deck-btn");
const closeBtnCreateDeckModal = document.querySelector(
  "#close-create-deck-btn",
);

// opens the modals
createDeckBtn.addEventListener("click", () => {
  createDeckModal.style.display = "flex";
  document.querySelector("#input-deck-name").value = "";
});

// close the modals
closeBtnCreateDeckModal.addEventListener("click", () => {
  createDeckModal.style.display = "none";
});

createDeckNameInput.addEventListener("input", (e) => {
  const inputValue = e.target.value;

  const emptyDeckNameMessage = "Deck name cannot be empty";
  if (inputValue.length == 0) {
    messages.add(emptyDeckNameMessage);
  } else {
    messages.delete(emptyDeckNameMessage);
  }
  updateMessages(createDeckMessages);

  const specialCharactersMessage =
    "Deck name cannot contain special characters";
  if (speicalCharactersPattern.test(inputValue)) {
    messages.add(specialCharactersMessage);
  } else {
    messages.delete(specialCharactersMessage);
  }

  if (messages.size == 0) {
    createDeckSubmitBtn.disabled = false;
  } else {
    createDeckSubmitBtn.disabled = true;
  }

  updateMessages(createDeckMessages);
});

// delete all decks
const deleteAllForm = document.querySelector("#delete-all-form");
const deleteAllModal = document.querySelector("#delete-all-modal");

const deleteAllBtn = document.querySelector("#delete-all-btn");
// delete all modal buttons
const closeBtnDeleteAllModal = document.querySelector("#close-delete-all-btn");

closeBtnDeleteAllModal.addEventListener("click", () => {
  deleteAllModal.style.display = "none";
});

deleteAllBtn.addEventListener("click", () => {
  deleteAllModal.style.display = "flex";
});

deleteAllForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const response = await fetch("/deck", {
    method: "DELETE",
  });

  if (response.ok) {
    window.location.reload();
    return;
  }
});


// update deck
const updateDeckModal = document.querySelector("#update-deck-modal");
const updateDeckForm = document.querySelector("#update-deck-form");
const updateDeckMessages = document.querySelector("#update-deck-messages");
const updateDeckInputName = document.querySelector("#update-input-deck-name");
const closeBtnUpdateDeckModal = document.querySelector("#close-update-deck-btn");
const updateDeckSubmitBtn = document.querySelector("#submit-update-deck-btn");
const allEditDeckBtns = document.querySelectorAll(".edit");

function handleUpdateDeck(e) {
  const btn = e.currentTarget;
  const deckElement = btn.parentElement.parentElement;
  const selectedDeckId = deckElement.getAttribute("data-deck-id");
  const selectedDeckName = deckElement.getAttribute("data-deck-name");
  selectedDeck = {
    deck_id: selectedDeckId,
    deck_name: selectedDeckName,
  };
  updateDeckInputName.value = selectedDeckName;
  updateDeckModal.placeholder = selectedDeckName;

  updateDeckModal.style.display = "flex";
}

updateDeckInputName.addEventListener("input", (e) => {
  const inputValue = e.target.value.trim();

  const emptyDeckNameMessage = "Deck name cannot be empty";
  if (inputValue.length == 0) {
    messages.add(emptyDeckNameMessage);
  } else {
    messages.delete(emptyDeckNameMessage);
  }
  updateMessages(updateDeckMessages);

  const specialCharactersMessage =
    "Deck name cannot contain special characters";
  if (speicalCharactersPattern.test(inputValue)) {
    messages.add(specialCharactersMessage);
  } else {
    messages.delete(specialCharactersMessage);
  }

  if (messages.size == 0) {
    updateDeckSubmitBtn.disabled = false;
  } else {
    updateDeckSubmitBtn.disabled = true;
  }

  updateMessages(updateDeckMessages);
});

allEditDeckBtns.forEach((btn) => {
  btn.addEventListener("click", handleUpdateDeck);
});

closeBtnUpdateDeckModal.addEventListener("click", () => {
  updateDeckModal.style.display = "none";
  messages.clear();
  selectedDeck = {};
});

updateDeckForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  selectedDeck.deck_name = updateDeckInputName.value;
  const response = await fetch("/deck", {
    method: "PUT",
    body: JSON.stringify(selectedDeck),
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (response.ok) {
    window.location.reload();
    return;
  } else {

    const responseJson = await response.json();
    const message = responseJson.message;

    messages.add(message);
    updateMessages(updateDeckMessages);
    setTimeout(() => {
        messages.delete(message);
        updateMessages(updateDeckMessages);
    }, 1000);

  }
});

const allDeleteDeckBtns = document.querySelectorAll(".delete");

async function handleDeleteDeckBtn(e) {
    const deck = e.target.parentElement.parentElement;
    const deckId = deck.getAttribute("data-deck-id");
    if (!deckId) {
      return;
    }
    const response = await fetch(`/deck/${deckId}`, {
        method: "DELETE",
    });

    if (response.ok) {
        deck.remove();
    }
}


allDeleteDeckBtns.forEach((btn) => {
  btn.addEventListener("click", handleDeleteDeckBtn);
});
