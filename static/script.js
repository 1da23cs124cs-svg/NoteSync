const editor = document.getElementById("editor");

let timeout;

// ----------------------------
// AUTO SAVE (MAIN FIX)
// ----------------------------
editor.addEventListener("input", function () {

    clearTimeout(timeout);

    timeout = setTimeout(() => {

        fetch(window.location.pathname.replace("/note/", "/save/"), {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "content=" + encodeURIComponent(editor.innerHTML)
        });

    }, 700);
});

// ----------------------------
// FORMAT FUNCTIONS
// ----------------------------
function format(command, btn) {
    document.execCommand(command, false, null);

    // Toggle active class
    btn.classList.toggle("active");
}

document.getElementById("fontSelect")?.addEventListener("change", function () {
    document.execCommand("fontName", false, this.value);
});

document.getElementById("fontSize")?.addEventListener("change", function () {
    document.execCommand("fontSize", false, this.value);
});

// ----------------------------
// EXTRA FEATURES
// ----------------------------
// Get editor

// ----------------------------
// HEADING
// ----------------------------
function addHeading() {
    document.execCommand("formatBlock", false, "h1");
}

// ----------------------------
// OPEN FILE PICKER
// ----------------------------
function openImagePicker() {
    document.getElementById("imageInput").click();
}

// ----------------------------
// HANDLE IMAGE UPLOAD
// ----------------------------
document.getElementById("imageInput").addEventListener("change", function () {

    const file = this.files[0];
    if (!file) return;

    const reader = new FileReader();

    reader.onload = function (e) {

        const imgHTML = `
            <img src="${e.target.result}" 
                 style="max-width:50%; display:block; margin:10px 0;">
        `;

        document.execCommand("insertHTML", false, imgHTML);

        // 🔥 IMPORTANT: trigger auto-save
        editor.dispatchEvent(new Event("input"));
    };

    reader.readAsDataURL(file);
});

function addTable() {
    let rows = prompt("Rows:", 2);
    let cols = prompt("Columns:", 2);

    rows = parseInt(rows);
    cols = parseInt(cols);

    if (rows > 0 && cols > 0) {

        let table = "<table border='1' style='border-collapse:collapse; width:100%; margin-top:10px;'>";

        for (let i = 0; i < rows; i++) {
            tableHTML += "<tr>";
            for (let j = 0; j < cols; j++) {
                tableHTML += "<td style='padding:5px; color:gray;' contenteditable='true'>Cell</td>";
            }
            tableHTML += "</tr>";
        }

        table += "</table>";

        document.execCommand("insertHTML", false, table);
    }
}

function addTimestamp() {

    const now = new Date();
    const timeString = now.toLocaleString();

    const timestampHTML = `
        <span contenteditable="false" 
              style="color:#888; font-size:12px; margin-left:10px; background:#222; padding:2px 5px; border-radius:4px;">
            [${timeString}]
        </span>
    `;

    document.execCommand("insertHTML", false, timestampHTML);
}
