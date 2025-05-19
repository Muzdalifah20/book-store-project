from flask import Flask , request,jsonify ,session, url_for, redirect

from app.bookclass import books
from datetime import timedelta
from app.register import do_register
from app.login import do_login, show_login
from app.utilities import get_html 



app = Flask(__name__)
app.secret_key = "secret"
app.permanent_session_lifetime = timedelta(hours=5)

# index route
@app.route("/")
@app.route("/index")
def index():
    return get_html("index", {})

# user route
@app.route("/user")
def user():
    if not session.get("user_email"):
        return redirect(url_for("login"))
    user_name = session.get("user_name", "")
    return get_html("user",{"user_name":user_name})

# registeration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return do_register()
    else:
        return get_html("register", {"error": ""})
    
# logging in route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_login()
    else:
        return show_login()
    
# logging out route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


# books route 
@app.route("/api/books")
def api_books():
    books_data = [book.to_dict() for book in books]
    return jsonify(books_data)

# the cart section
carts = {}
 
def find_book(book_id):
    try:
        book_id_int = int(book_id)
    except ValueError:
        return None  # invalid book_id

    for book in books:
        if book.book_id == book_id_int:
            return book
    return None


# adding to the cart
@app.route('/cart/add/<book_id>', methods=['POST'])
def add_to_cart(book_id):
    user_email = session.get("user_email")
    if not user_email:
        return redirect(url_for('login'))

    book = find_book(book_id)
    if not book:
        return "Book not found", 404

    if user_email not in carts:
        carts[user_email] = {}

    user_cart = carts[user_email]

    if book_id in user_cart:
        user_cart[book_id]["quantity"] += 1
    else:
        user_cart[book_id] = {
            "title": book.title,
            "price": book.price,
            "quantity": 1
        }
    # return redirect(url_for('cart'))
    return jsonify({"message": "Item added to cart"}), 200

# deleting from the cart
@app.route('/cart/remove/<book_id>', methods=['POST'])
def remove_from_cart(book_id):
    user_email = session.get("user_email")
    if not user_email:
        return redirect(url_for('login'))

    user_cart = carts.get(user_email, {})
    if book_id in user_cart:
        if user_cart[book_id]["quantity"] > 1:
            user_cart[book_id]["quantity"] -= 1
        else:
            del user_cart[book_id]

    return redirect(url_for('cart'))
@app.route('/cart/add/<book_id>', methods=['POST'])
def remove_to_carta(book_id):
    user_email = session.get("user_email")
    if not user_email:
        return redirect(url_for('login'))

    user_cart = carts.get(user_email, {})
    if book_id in user_cart:
        if user_cart[book_id]["quantity"] > 1:
            user_cart[book_id]["quantity"] += 1
        else:
            del user_cart[book_id]

    return redirect(url_for('cart'))
 
# updating the cart
@app.route('/cart/update/<book_id>', methods=['PUT'])
def update_cart_quantity(book_id):
    user_email = session.get("user_email")
    if not user_email:
        return jsonify({"error": "Unauthorized"}), 401

    user_cart = carts.get(user_email, {})
    if book_id not in user_cart:
        return jsonify({"error": "Item not in cart"}), 404

    data = request.get_json()
    quantity = data.get("quantity")

    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({"error": "Quantity must be an integer >= 1"}), 400

    user_cart[book_id]["quantity"] = quantity

    return jsonify({"message": "Quantity updated", "new_quantity": quantity})


@app.route('/cart')
def cart():
    user_email = session.get("user_email")
    if not user_email:
        return redirect(url_for('login'))

    user_cart = carts.get(user_email, {})

    # Build the cart HTML string here
    cart_html = ""
    total = 0
    for book_id, item in user_cart.items():
        item_total = item["price"] * item["quantity"]
        total += item_total
        cart_html += f"""
        <div>
            <h3>{item['title']}</h3>
            <p>Price: ${item['price']}</p>
            <p>Quantity: {item['quantity']}</p>
            <p>Subtotal: ${item_total}</p>
            <form action="/cart/remove/{book_id}" method="POST">
                <button type="submit">Remove one</button>
            </form>

        </div>
        <div>
          <p>
                Quantity: 
                <input type="number" id="quantity-{book_id}" value="{item['quantity']}" min="1" style="width: 50px;">
                <button onclick="updateQuantity('{book_id}')">Update</button>
            </p>
            <p>Subtotal: ${item_total}</p>
        </div>
        <hr>
        <hr>
        """

    cart_html += f"<h3>Total: ${total}</h3>"
    
    cart_html += """
<form action="/cart/clear" method="POST" style="margin-top: 20px;">
    <button type="submit">
        Clear Cart
    </button>
</form>
"""

    return get_html("cart", {
        "user_email": user_email,
        "cart_items": cart_html
    })

# clearing the cart entirely
@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    user_email = session.get("user_email")
    if not user_email:
        return redirect(url_for('login'))

    if user_email in carts:
        carts[user_email] = {}   

    return redirect(url_for('cart'))

#Search book endpoin
@app.route("/api/search")
def search_book():
    query = request.args.get("query","").strip()
    if not query:
        return jsonify([])
    
    match_books = [book.to_dict() for book in books
                   if book.matches_search(query) ]
    return jsonify(match_books)

# about page route
@app.route("/about", methods=["Get"])
def about():
    with open("data/about.txt", "r") as file:
        content = file.read()
    # Split content into paragraphs by double line breaks
    paragraphs = content.split("\n\n")
    # Wrap each paragraph in <p> tags and join
    html_content = "".join(f"<p>{p.strip().replace('\n', '<br>')}</p>" for p in paragraphs)

    return get_html("about", {"about":html_content})


if __name__ == '__main__':
    app.run(debug=True)
