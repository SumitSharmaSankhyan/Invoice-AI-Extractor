// =======================================
// Invoice AI Extractor
// script.js
// =======================================

let selectedFiles = [];

// Elements
const pdfInput = document.getElementById("pdfInput");
const chooseBtn = document.getElementById("chooseBtn");
const extractBtn = document.getElementById("extractBtn");
const downloadBtn = document.getElementById("downloadBtn");
const resetBtn = document.getElementById("resetBtn");

const fileList = document.getElementById("fileList");
const tableBody = document.getElementById("tableBody");
const loader = document.getElementById("loader");

// =======================================
// Choose Files
// =======================================

chooseBtn.onclick = () => {
    pdfInput.click();
};

// =======================================
// Files Selected
// =======================================

pdfInput.onchange = function () {

    selectedFiles = Array.from(pdfInput.files);

    showFiles();

};

// =======================================
// Show Files
// =======================================

function showFiles() {

    fileList.innerHTML = "";

    if (selectedFiles.length === 0) {

        fileList.innerHTML = "No PDF selected.";

        extractBtn.disabled = true;

        return;

    }

    extractBtn.disabled = false;

    selectedFiles.forEach(file => {

        let div = document.createElement("div");

        div.className = "file-item";

        let size = (file.size / 1024 / 1024).toFixed(2);

        div.innerHTML = `
            <strong>📄 ${file.name}</strong>
            <br>
            Size : ${size} MB
        `;

        fileList.appendChild(div);

    });

}

// =======================================
// Extract Data
// =======================================

extractBtn.onclick = async function () {

    if (selectedFiles.length === 0) {

        alert("Please choose PDF files.");

        return;

    }

    loader.style.display = "block";

    extractBtn.disabled = true;

    downloadBtn.disabled = true;

    tableBody.innerHTML = "";

    let formData = new FormData();

    selectedFiles.forEach(file => {

        formData.append("files", file);

    });

    try {

        const response = await fetch("/extract", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        loader.style.display = "none";

        extractBtn.disabled = false;

        downloadBtn.disabled = false;

        showTable(data);

    }

    catch (err) {

        loader.style.display = "none";

        extractBtn.disabled = false;

        alert("Extraction failed.");

        console.log(err);

    }

};

// =======================================
// Show Result Table
// =======================================

function showTable(data) {

    tableBody.innerHTML = "";

    if (data.length === 0) {

        tableBody.innerHTML = `

        <tr>

        <td colspan="9">

        No Data Found

        </td>

        </tr>

        `;

        return;

    }

    data.forEach(item => {

        let row = document.createElement("tr");

        row.innerHTML = `

        <td contenteditable="true">${item.po || ""}</td>

        <td contenteditable="true">${item.invoice_no || ""}</td>

        <td contenteditable="true">${item.invoice_date || ""}</td>

        <td contenteditable="true">${item.base_amount || ""}</td>

        <td contenteditable="true">${item.igst || ""}</td>

        <td contenteditable="true">${item.cgst || ""}</td>

        <td contenteditable="true">${item.sgst || ""}</td>

        <td contenteditable="true">${item.other || ""}</td>

        <td contenteditable="true">${item.total || ""}</td>

        `;

        tableBody.appendChild(row);

    });

}

// =======================================
// Download Excel
// =======================================

downloadBtn.onclick = function () {

    window.location.href = "/download";

};

// =======================================
// Start Over
// =======================================

resetBtn.onclick = async function () {

    selectedFiles = [];

    pdfInput.value = "";

    fileList.innerHTML = "No PDF selected.";

    loader.style.display = "none";

    extractBtn.disabled = true;

    downloadBtn.disabled = true;

    tableBody.innerHTML = `

    <tr>

        <td colspan="9">

        No Data Available

        </td>

    </tr>

    `;

    try {

        await fetch("/reset", {

            method: "POST"

        });

    }

    catch (err) {

        console.log(err);

    }

};

// =======================================
// Prevent Browser Opening PDF
// =======================================

document.addEventListener("dragover", function(e){

    e.preventDefault();

});

document.addEventListener("drop", function(e){

    e.preventDefault();

});
