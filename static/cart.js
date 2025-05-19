// this is for updaing the quantity of the cart
    async function updateQuantity(bookId) {
  const input = document.getElementById(`quantity-${bookId}`);
  const quantity = parseInt(input.value);

  if (isNaN(quantity) || quantity < 1) {
    alert('Please enter a valid quantity (1 or more).');
    return;
  }

  try {
    const response = await fetch(`/cart/update/${bookId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quantity: quantity })
    });

    const data = await response.json();

    if (response.ok) {
      // alert(data.message);
      location.reload();  // reload to show updated cart
    } else {
      alert(data.error || 'Failed to update quantity');
    }
  } catch (error) {
    alert('Error updating quantity');
    console.error(error);
  }
}
  
