 function incrementCartCount() {
  const countElem = document.getElementById('cart-count');
  let count = parseInt(countElem.textContent) || 0;
  count += 1;
  countElem.textContent = count;
  countElem.style.display = 'inline-block';
}

 
function attachAddToCartListeners() {
  document.querySelectorAll('.add-to-cart-btn').forEach(button => {
    button.addEventListener('click', async (event) => {
      event.preventDefault();
      const bookId = button.getAttribute('data-book-id');

      try {
        const response = await fetch(`/cart/add/${bookId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          // Just increment the cart count silently
          incrementCartCount();
        } else {
          // Optionally handle failure silently or log error
          console.error('Failed to add item to cart.');
        }
      } catch (error) {
        console.error('Error adding to cart:', error);
      }
    });
  });
}


async function loadBooks() {
  const container = document.getElementById('books-container');
  try {
    const res = await fetch('/api/books');
    const books = await res.json();
    container.innerHTML = '';
    books.forEach(book => {
      const div = document.createElement('div');
      div.className = 'book-card';
      div.innerHTML = `
        <h3>${book.title}</h3>
        <p>Price: $${book.price}</p>
        <img src="${book.cover_image}" alt="${book.title}">
          <button class="add-to-cart-btn" data-book-id="${book.book_id}">Add to Cart</button>


        
      `;
      container.appendChild(div);
    });

    attachAddToCartListeners(); // Attach listeners after buttons are created
  } catch {
    container.textContent = 'Failed to load books.';
  }
}

loadBooks();

  // document.getElementById('logout-form').addEventListener('submit', function() {
  //   localStorage.removeItem('user_name');
  // });