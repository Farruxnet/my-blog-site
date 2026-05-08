const copyButtonLabel = "Nusxa";
const copiedButtonLabel = "Bajarildi";
const codeBlocks = document.querySelectorAll(".post-content pre");

const copyText = async (text) => {
    if (navigator.clipboard) {
        await navigator.clipboard.writeText(text);
        return;
    }

    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.setAttribute("readonly", "");
    textArea.style.position = "fixed";
    textArea.style.opacity = "0";
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("copy");
    textArea.remove();
};

codeBlocks.forEach((block) => {
    const code = block.querySelector("code");

    if (!code || block.querySelector(".copy-code-button")) {
        return;
    }

    const button = document.createElement("button");
    button.type = "button";
    button.className = "copy-code-button";
    button.textContent = copyButtonLabel;
    button.setAttribute("aria-label", "Kodni nusxalash");
    block.appendChild(button);

    button.addEventListener("click", async () => {
        await copyText(code.textContent);
        button.textContent = copiedButtonLabel;

        setTimeout(() => {
            button.textContent = copyButtonLabel;
        }, 700);
    });
});
