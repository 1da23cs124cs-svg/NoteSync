const textarea = document.getElementById("editor");

let timeout = null;

textarea.addEventListener("keyup", function () {
    clearTimeout(timeout);

    timeout = setTimeout(() => {
        fetch(window.location.pathname.replace("/note/", "/save/"), {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "content=" + encodeURIComponent(textarea.value)
        });
    }, 700);
});