const chooseBtn=document.getElementById("chooseBtn");

const pdfInput=document.getElementById("pdfInput");

const fileList=document.getElementById("fileList");

const uploadBtn=document.getElementById("uploadBtn");

const status=document.getElementById("status");

const dropZone=document.getElementById("dropZone");

let selectedFiles=[];


chooseBtn.onclick=()=>{

pdfInput.click();

};


pdfInput.onchange=()=>{

selectedFiles=[...pdfInput.files];

displayFiles();

};


dropZone.addEventListener("dragover",(e)=>{

e.preventDefault();

dropZone.style.background="#dff4ff";

});


dropZone.addEventListener("dragleave",()=>{

dropZone.style.background="white";

});


dropZone.addEventListener("drop",(e)=>{

e.preventDefault();

dropZone.style.background="white";

selectedFiles=[...e.dataTransfer.files];

displayFiles();

});


function displayFiles(){

fileList.innerHTML="";

selectedFiles.forEach(file=>{

fileList.innerHTML+=`

<div class="file-item">

📄 ${file.name}

</div>

`;

});

}


uploadBtn.onclick=()=>{

if(selectedFiles.length==0){

alert("Select PDF files");

return;

}

const formData=new FormData();

selectedFiles.forEach(file=>{

formData.append("files",file);

});

status.innerHTML="Uploading...";

fetch("/upload",{

method:"POST",

body:formData

})

.then(res=>res.json())

.then(data=>{

status.innerHTML="✅ Uploaded Successfully";

console.log(data);

})

.catch(()=>{

status.innerHTML="Upload Failed";

});

};
