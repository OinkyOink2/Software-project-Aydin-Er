const dz = document.getElementById('dropzone');
const fileInput = document.getElementById('file');
dz.addEventListener('click', ()=> fileInput.click());
['dragenter','dragover'].forEach(evt => dz.addEventListener(evt, e => { 
  e.preventDefault(); e.stopPropagation(); dz.classList.add('dragover'); 
}));
['dragleave','drop'].forEach(evt => dz.addEventListener(evt, e => { 
  e.preventDefault(); e.stopPropagation(); dz.classList.remove('dragover'); 
}));
dz.addEventListener('drop', e => { 
  if (e.dataTransfer.files.length) { 
    fileInput.files = e.dataTransfer.files; 
    dz.classList.remove('dragover'); 
    dz.closest('form').submit(); 
  } 
});

const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const asciiBox = document.getElementById('asciiBox');

if (copyBtn) { 
  copyBtn.addEventListener('click', async ()=> { 
    asciiBox.select(); 
    document.execCommand('copy'); 
    copyBtn.textContent = 'Copied!'; 
    setTimeout(()=> copyBtn.textContent='Copy ASCII', 1200); 
  }); 
}

if (downloadBtn) { 
  downloadBtn.addEventListener('click', ()=> {
    const blob = new Blob([asciiBox.value], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; 
    a.download = 'ascii-art.txt'; 
    a.click();
    URL.revokeObjectURL(url);
  }); 
}