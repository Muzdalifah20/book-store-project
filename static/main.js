 //loading the book in the user page 
    async function loadBooks() {
      try {
        const response = await fetch('/api/books');
       
        const books = await response.json();

        const container = document.getElementById('books-container');
        container.innerHTML = ''; // Clear container

        books.forEach(book => {
          const card = document.createElement('div');
          card.className = 'book-card';
          card.innerHTML = `
            <img src="${book.cover_image}" alt="${book.title}" />
            <h3>${book.title}</h3>
            <p><em>by ${book.author}</em></p>
             
            <p>Price: $${book.price.toFixed(2)}</p>
            <form action="/login" method="get" id="add_cart">
            <button type="submit">Add to Cart</button>
            </form>
          `;
          container.appendChild(card);
        });
      } catch (err) {
        console.error(err);
        document.getElementById('books-container').textContent = 'Error loading books.';
      }
    }

     
    loadBooks();




   
