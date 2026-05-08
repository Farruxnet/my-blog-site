const copyButtonLabel = "Nusxa";
const codeBlocks = document.querySelectorAll("pre");

codeBlocks.forEach((block) => {
    if (!navigator.clipboard) {
        return;
    }

    const button = document.createElement("button");
    button.innerText = copyButtonLabel;
    block.appendChild(button);

    button.addEventListener("click", async () => {
        const code = block.querySelector("code");

        if (!code) {
            return;
        }

        await navigator.clipboard.writeText(code.innerText);
        button.innerText = "Bajarildi";

        setTimeout(() => {
            button.innerText = copyButtonLabel;
        }, 700);
    });
});
