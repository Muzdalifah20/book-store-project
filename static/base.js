 
    // Function to load external HTML into a container
    async function loadHTML(url, containerId) {
      const response = await fetch(url);
      const text = await response.text();
      let container =document.getElementById(containerId) 
      if (container) {
    container.innerHTML = text;
  } else {
    console.warn(`Element with id "${containerId}" not found.`);
  }
    }

    // Load header and footer
//    document.addEventListener('DOMContentLoaded', () => {
  loadHTML('/static/html/header.html', 'header-placeholder');
  loadHTML('/static/html/footer.html', 'footer-placeholder');
// });

 