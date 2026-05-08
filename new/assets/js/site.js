const root = document.documentElement;
const themeToggle = document.getElementById("themeToggle");
const searchPanel = document.getElementById("searchPanel");
const openSearch = document.getElementById("openSearch");
const closeSearch = document.getElementById("closeSearch");
const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");
const mobileMenu = document.querySelector(".mobile-menu");
const mobileNav = document.getElementById("mobileNav");

const searchItems = [
    { title: "Home", text: "Static docs generator overview", href: "index.html" },
    { title: "About", text: "Project architecture and goals", href: "about.html" },
    { title: "Contact", text: "Email, LinkedIn and contact form", href: "contact.html" },
    { title: "Markdown syntax", text: "Headings, lists, table and inline formatting", href: "post.html#markdown-syntax" },
    { title: "Code blocks", text: "PrismJS syntax highlighting and copy buttons", href: "post.html#code-blocks" },
    { title: "Deploy", text: "Static hosting workflow", href: "post.html#deploy" }
];

if (localStorage.getItem("theme") === "dark") {
    root.dataset.theme = "dark";
}

themeToggle?.addEventListener("click", () => {
    const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = nextTheme === "dark" ? "dark" : "";
    localStorage.setItem("theme", nextTheme);
});

const renderSearch = (query = "") => {
    if (!searchResults) {
        return;
    }

    const normalized = query.trim().toLowerCase();
    const matches = searchItems.filter((item) => {
        return !normalized || `${item.title} ${item.text}`.toLowerCase().includes(normalized);
    });

    searchResults.innerHTML = matches.map((item) => `
        <a class="search-result" href="${item.href}">
            <strong>${item.title}</strong>
            <span>${item.text}</span>
        </a>
    `).join("");
};

const showSearch = () => {
    if (!searchPanel || !searchInput) {
        return;
    }

    searchPanel.setAttribute("aria-hidden", "false");
    renderSearch(searchInput.value);
    searchInput.focus();
};

const hideSearch = () => {
    if (!searchPanel) {
        return;
    }

    searchPanel.setAttribute("aria-hidden", "true");
    openSearch?.focus();
};

openSearch?.addEventListener("click", showSearch);
closeSearch?.addEventListener("click", hideSearch);
searchInput?.addEventListener("input", () => renderSearch(searchInput.value));
searchResults?.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
        searchPanel?.setAttribute("aria-hidden", "true");
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "/" && document.activeElement !== searchInput) {
        event.preventDefault();
        showSearch();
    }

    if (event.key === "Escape" && searchPanel?.getAttribute("aria-hidden") === "false") {
        hideSearch();
    }
});

const copyText = async (text) => {
    if (navigator.clipboard) {
        await navigator.clipboard.writeText(text);
        return;
    }

    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
};

document.querySelectorAll(".post pre[class*='language-']").forEach((block) => {
    if (block.querySelector(".copy-code")) {
        return;
    }

    const button = document.createElement("button");
    button.className = "copy-code";
    button.type = "button";
    button.textContent = "Copy";
    block.appendChild(button);

    button.addEventListener("click", async () => {
        const code = block.querySelector("code")?.textContent || "";
        await copyText(code);
        button.textContent = "Copied";
        setTimeout(() => {
            button.textContent = "Copy";
        }, 900);
    });
});

mobileMenu?.addEventListener("click", () => {
    if (!mobileNav) {
        return;
    }

    const isOpen = mobileNav.dataset.open === "true";
    mobileNav.dataset.open = String(!isOpen);
    mobileMenu.setAttribute("aria-expanded", String(!isOpen));
});

renderSearch();
