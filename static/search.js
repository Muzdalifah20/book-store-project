(()=>{
    const search_button = document.getElementById("search_button")
    search_button.addEventListener('click', async ()=>{
      const query = document.getElementById("search_input").value.trim()
      if (!query){
        alert ("Please enter a book to search");
        return;
      }

    const response = await fetch(`/api/search?query=${encodeURIComponent(query)}`);
    const result = await response.json()

    const result_container = document.getElementById("search_result");
    result_container.innerHTML = '';

    if (result.length === 0){
      result_container.textContent = "Sorry, No book found";
      return;
    }

    result.forEach(book =>{
        const card = document.createElement('div');
          card.className = 'book-card';
          card.innerHTML = `
            <h3>${book.title}</h3>
            <p><em>by ${book.author}</em></p>`
          result_container.appendChild(card);

        });
    });
})();