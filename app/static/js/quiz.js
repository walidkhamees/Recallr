const cardsContainer = document.querySelector(".card-container");
const timeRemaining = document.querySelector("h2 span");
const allQuizInput = document.querySelectorAll(".quiz-input");
let currentQuestion = 0;

if (cardsContainer.childElementCount === 0) {
  window.location.href = `/deck/${deckId}/result/${quizId}`;
}

const quizId = Number(cardsContainer.getAttribute("data-quiz-id"));
const deckId = cardsContainer.getAttribute("data-deck-id");
const quizStart = Number(cardsContainer.getAttribute("data-quiz-start"));
const quizEnd = Number(cardsContainer.getAttribute("data-quiz-end"));

if (cardsContainer.childElementCount === 0) {
  window.location.href = `/deck/${deckId}/result/${quizId}`;
}

async function handleAnswer(e) {
  e.preventDefault();
  const answer = e.target.querySelector("input").value;
  const quizId = Number(cardsContainer.getAttribute("data-quiz-id"));
  const cardId = e.target.parentElement.getAttribute("data-card-id");

  const answerRequest = {
    quiz_id: quizId,
    card_id: cardId,
    answer: answer,
  };

  const request = await fetch(`/deck/${deckId}/quiz`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(answerRequest),
  });

  if (!request.ok) {
    alert("Something went wrong");
  } else {
    e.target.parentElement.classList.add("turn-transparent");

    setTimeout(() => {
      cardsContainer.removeChild(e.target.parentElement);
      currentQuestion += 1;
      if (allQuizInput.length > currentQuestion) {
        allQuizInput[currentQuestion].focus();
      }

      if (cardsContainer.childElementCount === 0) {
        window.location.href = `/deck/${deckId}/result/${quizId}`;
      }
    }, 200);
  }
}

let now = Math.floor(Date.now() / 1000);
let time = quizEnd - now;

if (now > quizEnd) {
  alert("Quiz is over");
}

const interval = setInterval(() => {
  now = Math.floor(Date.now() / 1000);
  time = quizEnd - now;

  let minutes = Math.floor(time / 60);
  let seconds = time % 60;

  timeRemaining.innerText = `${minutes}:${seconds < 10 ? "0" + seconds : seconds}`;

  if (time === 0) {
    timeRemaining.innerText = "Time's up!";
    clearInterval(interval);

    setTimeout(() => {
      window.location.href = `/deck/${deckId}/result/${quizId}`;
    }, 1000);
  }
}, 1000);

const forms = document.querySelectorAll("form");

forms.forEach((form) => {
  input = form.querySelector("input");
  input.value = "";
  form.addEventListener("submit", handleAnswer);
});
