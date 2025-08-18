logoutBtn = document.querySelector("#logout");

if (logoutBtn) {

    logoutBtn.addEventListener("click", async () => {
        const response = await fetch("/logout", {
            method: "GET",
        });
        if (response.ok) {
            localStorage.clear();
            window.location.href = "/";
        }
    });

}
