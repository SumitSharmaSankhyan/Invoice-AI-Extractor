// =============================
// Invoice Extractor
// =============================

let selectedFiles = [];

// =============================
// HTML Elements
// =============================

const pdfInput = document.getElementById("pdfInput");
const chooseBtn = document.getElementById("chooseBtn");
const extractBtn = document.getElementById("extractBtn");
const downloadBtn = document.getElementById("downloadBtn");
const resetBtn = document.getElementById("resetBtn");

const fileList = document.getElementById("fileList");
const tableBody = document.getElementById("tableBody");
const loader = document.getElementById("loader");

// =============================
// Choose Files
// =============================

chooseBtn.addEventListener("click", () => {
    pdfInput.click();
});

// =============================
// File Selected
// =============================

pdfInput.addEventListener("change", () => {

    selectedFiles = Array.from(pdfInput.files);

    showFiles();

    if (selectedFiles.length > 0) {
        extractBtn.disabled = false;
    }

});

// =============================
// Show Selected Files
// =============================

function showFiles() {

    fileList.innerHTML = "";

    if (selectedFiles.length === 0) {

        fileList.innerHTML = "No PDF Selected";

        extractBtn.disabled = true;

        return;

    }

    selectedFiles.forEach(file => {

        let div = document.createElement("div");

        div.className = "file-item";

        div.innerHTML =
            "📄 " +
            file.name +
            " (" +
            (file.size / 1024 / 1024).toFixed(2) +
            " MB)";

        fileList.appendChild(div);

    });

}

// =============================
// Extract Button
// =============================

extractBtn.addEventListener("click", async () => {

    if (selectedFiles.length === 0) {

        alert("Please choose PDF files.");

        return;

    }

    loader.style.display = "block";

    extractBtn.disabled = true;

    const formData = new FormData();

    selectedFiles.forEach(file => {

        formData.append("files", file);

    });

    try {

        const response = await fetch("/extract", {

            method: "POST",

            body: formData

        });

        const result = await response.json();

        loader.style.display = "none";

        extractBtn.disabled = false;

        showTable(result);

        downloadBtn.disabled = false;

    }

    catch (error) {

        loader.style.display = "none";

        extractBtn.disabled = false;

        alert("Unable to extract invoice data.");

        console.log(error);

    }

});

// =============================
// Show Table
// =============================

function showTable(data) {

    tableBody.innerHTML = "";

    if (!data || data.length === 0) {

        tableBody.innerHTML =

        `<tr>

            <td colspan="9">

                No Data Found

            </td>

        </tr>`;

        return;

    }

    data.forEach(item => {

        tableBody.innerHTML +=

        `<tr>

            <td contenteditable="true">${item.po}</td>

            <td contenteditable="true">${item.invoice}</td>

            <td contenteditable="true">${item.date}</td>

            <td contenteditable="true">${item.base}</td>

            <td contenteditable="true">${item.igst}</td>

            <td contenteditable="true">${item.cgst}</td>

            <td contenteditable="true">${item.sgst}</td>

            <td contenteditable="true">${item.other}</td>

            <td contenteditable="true">${item.total}</td>

        </tr>`;

    });

}

// =============================
// Download Excel
// =============================

downloadBtn.addEventListener("click", () => {

    window.location.href = "/download";

});

// =============================
// Start Over
// =============================

resetBtn.addEventListener("click", () => {

    selectedFiles = [];

    pdfInput.value = "";

    fileList.innerHTML = "No PDF Selected";

    tableBody.innerHTML =

    `<tr>

        <td colspan="9">

            No Data Available

        </td>

    </tr>`;

    extractBtn.disabled = true;

    downloadBtn.disabled = true;

    loader.style.display = "none";

});

// =============================
// Drag & Drop (Optional)
// =============================

document.addEventListener("dragover", function(e){

    e.preventDefault();

});

document.addEventListener("drop", function(e){

    e.preventDefault();

});
