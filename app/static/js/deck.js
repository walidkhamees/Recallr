function convertStringToBoolean(booleanString) {
  switch (booleanString.toLowerCase()) {
    case "true":
      return true;
    case "false":
      return false;
    default:
      return false;
  }
}

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

function handleFlipCard(e) {
  const card = e.currentTarget;
  const flipped = convertStringToBoolean(card.getAttribute("data-flipped"));
  if (flipped) {
    card.setAttribute("data-flipped", "false");
    card.querySelector(".answer").style.display = "none";
    card.querySelector(".question").style.display = "flex";
  } else {
    card.setAttribute("data-flipped", "true");
    card.querySelector(".answer").style.display = "flex";
    card.querySelector(".question").style.display = "none";
  }
}

function handleUpdateCard(e) {
  const card = e.currentTarget.parentElement.parentElement;
  const cardId = card.getAttribute("data-card-id");
  const question = card.getAttribute("data-card-question");
  const answer = card.getAttribute("data-card-answer");

  const questionInput = updateCardForm.querySelector("#question-update-input");
  const answerInput = updateCardForm.querySelector("#answer-update-input");

  questionInput.placeholder = question;
  questionInput.value = question;

  answerInput.placeholder = answer;
  answerInput.value = answer;

  currentCard = {
    card_id: cardId,
    question,
    answer,
  };

  updateCardModal.style.display = "flex";
}

async function handleDeleteCardBtn(e) {
  const currentPath = window.location.href;
  const card = e.target.parentElement.parentElement.parentElement;
  const cardId = card.getAttribute("data-card-id");
  if (!cardId) {
    return;
  }

  const response = await fetch(`${currentPath}/card/${cardId}`, {
    method: "DELETE",
  });

  if (response.ok) {
    card.remove();
  }
}

let currentCard = {};
let messages = new Set();

// Buttons
const cards = document.querySelectorAll(".card");
const deleteCardBtns = document.querySelectorAll(".card-btn.delete-card");
const updateCardBtns = document.querySelectorAll(".card-btn.edit-card");

updateCardBtns.forEach((editCardBtn) => {
  editCardBtn.addEventListener("click", handleUpdateCard);
});

deleteCardBtns.forEach((deleteCardBtn) => {
  deleteCardBtn.addEventListener("click", handleDeleteCardBtn);
});

cards.forEach((card) => {
  card.addEventListener("click", handleFlipCard);
});

// create card form
const openNewCardModalBtn = document.querySelector("#open-new-card-modal");
const createCardModal = document.querySelector("#create-card-modal");
const createCardForm = document.querySelector("#create-card-form");
const closeCreateCardBtn = document.querySelector("#close-create-card-btn");
const createCardQuestionInput = document.querySelector("#question-input");
const createCardAnswerInput = document.querySelector("#answer-input");
const createCardMessages = document.querySelector("#create-card-messages");
const createCardSubmitBtn = document.querySelector("#submit-create-deck-btn");

createCardQuestionInput.addEventListener("input", (e) => {

  createCardQuestionInput.value = e.currentTarget.value;
  const emptyMessage = "Question cannot be empty";
  if (e.currentTarget.value === "") {
    messages.add(emptyMessage);
  } else {
    messages.delete(emptyMessage);
  }

  if (messages.size == 0) {
    createCardSubmitBtn.disabled = false;
  } else {
    createCardSubmitBtn.disabled = true;
  }

  updateMessages(createCardMessages);
});

createCardAnswerInput.addEventListener("input", (e) => {
  createCardAnswerInput.value = e.currentTarget.value;
  const emptyMessage = "Answer cannot be empty";
  if (e.currentTarget.value === "") {
    messages.add(emptyMessage);
  } else {
    messages.delete(emptyMessage);
  }

  if (messages.size == 0) {
    createCardSubmitBtn.disabled = false;
  } else {
    createCardSubmitBtn.disabled = true;
  }

  updateMessages(createCardMessages);
});

openNewCardModalBtn.addEventListener("click", () => {
  createCardModal.style.display = "flex";
  createCardQuestionInput.value = "";
  createCardAnswerInput.value = "";

  messages.clear();
  messages.add("Question cannot be empty");
  messages.add("Answer cannot be empty");

  updateMessages(createCardMessages);
});

// delete all modal form
const openDeleteAllModalBtn = document.querySelector("#open-delete-all-modal");
const deleteAllModal = document.querySelector("#delete-all-modal");
const deleteAllForm = document.querySelector("#delete-all-form");
const closeDeleteAllBtn = document.querySelector("#close-delete-all-btn");

openDeleteAllModalBtn.addEventListener("click", () => {
  deleteAllModal.style.display = "flex";
});

closeDeleteAllBtn.addEventListener("click", () => {
  deleteAllModal.style.display = "none";
});

// Update Card
const updateCardModal = document.querySelector("#update-card-modal");
const updateCardForm = document.querySelector("#update-card-form");
const closeUpdateCardBtn = document.querySelector("#close-update-card-btn");
const updateCardQuestionInput = document.querySelector(
  "#question-update-input",
);
const updateCardAnswerInput = document.querySelector("#answer-update-input");
const updateCardMessages = document.querySelector("#update-card-messages");
const updateCardSubmitBtn = document.querySelector("#submit-update-deck-btn");

closeUpdateCardBtn.addEventListener("click", () => {
  updateCardModal.style.display = "none";
  messages.clear();
  updateMessages(updateCardMessages);
});

updateCardQuestionInput.addEventListener("input", (e) => {
  const emptyMessage = "Question cannot be empty";
  if (e.currentTarget.value === "") {
    messages.add(emptyMessage);
  } else {
    messages.delete(emptyMessage);
  }

  if (messages.size == 0) {
    updateCardSubmitBtn.disabled = false;
  } else {
    updateCardSubmitBtn.disabled = true;
  }

  updateMessages(updateCardMessages);
});

updateCardAnswerInput.addEventListener("input", (e) => {
  const emptyMessage = "Answer cannot be empty";
  if (e.currentTarget.value === "") {
    messages.add(emptyMessage);
  } else {
    messages.delete(emptyMessage);
  }

  if (messages.size == 0) {
    updateCardSubmitBtn.disabled = false;
  } else {
    updateCardSubmitBtn.disabled = true;
  }

  updateMessages(updateCardMessages);
});

updateCardForm.addEventListener("submit", async (e) => {
  if (messages.size != 0) {
    return;
  }

  e.preventDefault(); // prevent submitting the form
  const currentPath = window.location.href;

  currentCard.question = updateCardQuestionInput.value;
  currentCard.answer = updateCardAnswerInput.value;

  const response = await fetch(`${currentPath}/card`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(currentCard),
  });

  // TODO: No need to reload the page just update the card
  if (response.ok) {
    updateCardModal.style.display = "none";
    window.location.reload();
  }
  updateMessages(updateCardMessages);
});

closeCreateCardBtn.addEventListener("click", () => {
  createCardModal.style.display = "none";
  messages.clear();
});

deleteAllForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const currentPath = window.location.href;

  const response = await fetch(`${currentPath}/card`, {
    method: "DELETE",
  });

  if (response.ok) {
    window.location.reload();
    return;
  }
});
