from flask import Flask , request,jsonify ,session, url_for, redirect
from utilities import get_html , usersdb
import json
from bookclass import books 
from datetime import timedelta
# from carts import carts

app = Flask(__name__)
app.secret_key = "secret"
app.permanent_session_lifetime = timedelta(hours=5)

# Registeration part
def validate_user_input(new_user):
    for key, value in new_user.items():
        if not value:
            return True, f"Please enter your {key}"
    users = usersdb()
    for user in users:
        if new_user["email"] == user["email"]:
            return True, "This email already exists"
    return False, ""

 
def do_register():
    first_name = request.form.get("first_name", "").strip().lower()
    last_name = request.form.get("last_name", "").strip().lower()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    new_user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    }

    error_found, error_message = validate_user_input(new_user)
    if error_found:
        return get_html("register", error_message), 400
    # save the user name to a file to use it in the user page
    user_name = new_user.get("first_name")
    with open("user-name.txt", "a") as file:
        file.write(user_name)

    # save the new_user information in jason file
    users = usersdb()
    users.append(new_user)
    with open("usersdb.json", "w") as file:
        json.dump(users, file, indent=4)

    return redirect(url_for("login"))

# do the login
def do_login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password","").strip()
    user_log = {
        "email": email,
        "password": password
    }
    # checking for empty fields
    for key,value in user_log.items():
        if not value:
            return f"please enter your {key}"
    # get json file from usersdb()
    users = usersdb()
    for user in users:
        if user_log.get("email") == user.get("email"):
            # print(f"Comparing passwords: input='{password}' stored='{user.get('password')}'")
            if user_log.get("password") == user.get("password"):
                email = user.get("email")
                # adding session 
                session.permanent = True
                session["user_email"] = email
                return redirect(url_for("user"))
            else:
                if "user_email" in session:
                    redirect(url_for("/user"))
                return get_html("login","Password is not correct")
    return get_html("login", "User name is not correct")
 

def show_login():
    return get_html("login")

@app.route("/")
def index():
    return get_html("index")

@app.route("/user")
def user():
    if not session.get("user_email"):
        return redirect(url_for("login"))
    return get_html("user")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return do_register()
    else:
        return get_html("register")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_login()
    else:
        return show_login()
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


    
@app.route("/api/books")
def api_books():
    books_data = [book.to_dict() for book in books]
    return jsonify(books_data)

# the cart section

carts = {}

# # Dummy books data (replace with your real books)
# books_list = [
#     {"book_id": "1", "title": "Book One", "price": 10},
#     {"book_id": "2", "title": "Book Two", "price": 15},
# ]

# def find_book(book_id_int):
def find_book(book_id):
    try:
        book_id_int = int(book_id)
    except ValueError:
        return None  # invalid book_id

    for book in books:
        if book.book_id == book_id_int:
            return book
    return None



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
        <hr>
        """

    cart_html += f"<h3>Total: ${total}</h3>"

    # Pass the generated HTML to your get_html function to inject into template
    return get_html("cart", user_email=user_email, cart_html=cart_html)

 


#Search book endpoin
@app.route("/api/search")
def search_book():
    query = request.args.get("query","").strip()
    if not query:
        return jsonify([])
    
    match_books = [book.to_dict() for book in books
                   if book.matches_search(query) ]
    return jsonify(match_books)



if __name__ == '__main__':
    app.run(debug=True)
