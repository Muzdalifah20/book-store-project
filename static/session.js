




fetch('/api/books')
  .then(res => res.json())
  .then(books => {
    const container = document.querySelector('.books-container');
    books.forEach(book => {
      // const img = document.createElement("img");
      // img.src = book.cover_image;
      const card = document.createElement('div');
      card.className = 'book-card';
      card.innerHTML = `
        <img src="${book.cover_image}" alt="${book.title}" />
        <h3>${book.title}</h3>
        <p>$${book.price.toFixed(2)}</p>
        <button data-id="${book.id}">Add to Cart</button>
      `;
      container.appendChild(card);
    });

    container.querySelectorAll('button').forEach(button => {
      button.addEventListener('click', () => {
        const bookId = button.getAttribute('data-id');
        fetch('/api/cart/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ book_id: parseInt(bookId) })
        })
        .then(res => res.json())
        .then(data => {
          alert(data.message);
          loadCart();  // function to refresh cart display
        });
      });
    });
  });

  function loadCart() {
    fetch('/api/cart')
      .then(res => res.json())
      .then(cartItems => {
        const cartContainer = document.querySelector('.cart-container');
        cartContainer.innerHTML = '';
        cartItems.forEach(item => {
          const div = document.createElement('div');
          div.className = 'cart-item';
          div.innerHTML = `
            <span>${item.title} (x${item.quantity})</span>
            <button data-id="${item.id}">Delete</button>
          `;
          cartContainer.appendChild(div);
        });
  
        cartContainer.querySelectorAll('button').forEach(button => {
          button.addEventListener('click', () => {
            const bookId = button.getAttribute('data-id');
            fetch('/api/cart/remove', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ book_id: parseInt(bookId) })
            })
            .then(res => res.json())
            .then(data => {
              alert(data.message);
              loadCart();
            });
          });
        });
      });
  }
  
  // Call loadCart() on page load to initialize cart display
  window.onload = loadCart;
  