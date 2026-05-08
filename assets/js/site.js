const root = document.documentElement;

if (localStorage.getItem("theme") === "dark") {
    root.classList.add("dark");
}

const menuToggle = document.getElementById("menuToggle");
const siteMenu = document.getElementById("siteMenu");

if (menuToggle && siteMenu) {
    const setMenuState = (isOpen) => {
        siteMenu.classList.toggle("hidden", !isOpen);
        siteMenu.classList.toggle("flex", isOpen);
        menuToggle.setAttribute("aria-expanded", String(isOpen));
    };

    menuToggle.addEventListener("click", () => {
        setMenuState(siteMenu.classList.contains("hidden"));
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth >= 768) {
            setMenuState(false);
        }
    });
}
