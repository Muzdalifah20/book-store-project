from flask import Flask , request,jsonify ,session, url_for, redirect
from utilities import get_html , usersdb
import json
from bookclass import books
from datetime import timedelta


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
carts = {
    "user_email":{
        "books":{
            "book1":{ "title":"hi", "price": 10, "quantity": 2},
            "book1":{ "title":"ha", "price": 30, "quantity": 3}
        }
    }
}

@app.route("/api/cart/<user_email>", methods=["GET"])
def get_cart(user_email):
    cart = carts.get(user_email, {"books":{}})
    return cart

@app.route("api/cart/<user_email>", methods=['POST'])
def add_cart(user_email):
    cart_data =  request.get_json()
    book_id = cart_data.get("book_id")
    title = cart_data.get("title")
    price = cart_data.get("price")
    quantity = cart_data.get("quantity")

    # create a new cart for the user whose email is not in the carts, else give cart deteails
    if user_email not in carts:
        carts["user_email"] = {"books":{}}
    
    # show cart books
    books = carts["user_email"]["books"]

    if book_id in books:
        books[book_id]["quantity"] += quantity
    else:
        books[book_id] = {"title":title, "price":price,"quantity":quantity}

    return jsonify(carts["user_email"])

@app.route("/api/cart/<user_email>/<book_id>", methods=['DELETE'])
def remove_book(user_email, book_id):
    if user_email in carts and book_id in carts[user_email]["books"]:
        carts[user_email]["books"].pop(book_id)
        return jsonify(carts["user_email"])
    return jsonify({"error":"this book is not found"}), 404

@app.route("/api/cart/<user_email>/clear", methods=['POST'])
def clear_cart(user_email):
    if user_email in carts:
        carts[user_email]["books"] = {}
    return jsonify({"message": "Your cart is cleared!"})

@app.route("/cart")
def cart():
    return get_html("cart")

