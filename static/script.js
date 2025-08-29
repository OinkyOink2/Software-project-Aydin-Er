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
