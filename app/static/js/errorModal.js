const errorModal = document.querySelector(".error-modal");
const errors = document.querySelectorAll(".error-modal li");

if (errors.length > 0) {
  errorModal.style.display = "flex";
}

const closeBtn = document.querySelector(".error-modal button");

closeBtn.addEventListener("click", () => {
    errorModal.style.display = "none";
});




