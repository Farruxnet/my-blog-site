const root = document.documentElement;

if (localStorage.getItem("theme") === "dark") {
    root.classList.add("dark");
}

const menuToggle = document.getElementById("menuToggle");
const siteMenu = document.getElementById("siteMenu");

if (menuToggle && siteMenu) {
    menuToggle.addEventListener("click", () => {
        siteMenu.classList.toggle("hidden");
        siteMenu.classList.toggle("flex");
    });
}
