// script.js
document.addEventListener('DOMContentLoaded', function() {
  // Simulate fetching files from database
  const files = [
    { name: 'File 1.txt', link: '#' },
    { name: 'File 2.pdf', link: '#' },
    { name: 'File 3.docx', link: '#' },
    // Add more files here...
  ];

  // Function to display files in the scrollable div
  function displayFiles(fileListElement, files) {
    fileListElement.innerHTML = '';
    files.forEach(file => {
      const fileElement = document.createElement('div');
      fileElement.classList.add('file-list');
      fileElement.innerHTML = `<a href="${file.link}">${file.name}</a>`;
      fileListElement.appendChild(fileElement);
    });
  }

  // Display files in both scrollable divs
  displayFiles(document.getElementById('fileList'), files);
  displayFiles(document.getElementById('fileList2'), files);

  // Handle file upload (for demonstration purposes only)
  document.getElementById('fileInput').addEventListener('change', function(e) {
    const selectedFiles = e.target.files;
    console.log('Selected Files:', selectedFiles);
    // Here you would send the files to the server using AJAX or fetch API
  });

  document.getElementById('fileInput2').addEventListener('change', function(e) {
    const selectedFiles = e.target.files;
    console.log('Selected Files:', selectedFiles);
    // Here you would send the files to the server using AJAX or fetch API
  });
});
function selectFile(element) {
    // Remove selected class from all elements
    const fileList = document.getElementById('fileList');
    const fileElements = fileList.children;
    for (let i = 0; i < fileElements.length; i++) {
      fileElements[i].classList.remove('selected');
    }
    
    // Add selected class to the clicked element
    element.classList.add('selected');
  }

