from flask import Flask, session, jsonify, request, render_template
from bookclass import books  # Assuming this imports your books list
from utilites import get_html, usersdb 
import json
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# def get_book(book_id):
#     for book in books:
#         if book['id'] == book_id:
#             return book
#     return None

# @app.route('/api/books')
# def api_books():
#     return jsonify(books)

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
                # assign the user name inside a text file
                user_name = user.get("first_name")
                with open("welcome.txt", "w" ) as file:
                    file.write(user_name)
                # read the text file 
                with open("welcome.txt","r") as file:
                    user_name = file.read()
                
                # actual_value = f"<h1>Welcome {user_name} </h1>"
                books_dicts = [book.__dict__ for book in books]
                index_page = render_template("index.html", books=books_dicts, user_name=user_name)
                return index_page
                # return index_page.replace("$$welcome$$", actual_value)
            else:
                return "Password is not correct"
    return "User name is not correct"
 

def show_login():
    return render_template("login.html")
# @app.route('/login')
# def login():
#     return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_login()
    else:
        return show_login()


@app.route('/')
def home():
   books_dicts = [book.__dict__ for book in books]  # Convert Book objects to dicts
   return render_template('index.html', books=books_dicts)
   # List of Book objects

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
        return render_template("register.html", error=error_message), 400

    users = usersdb()
    users.append(new_user)
    with open("usersdb.json", "w") as file:
        json.dump(users, file, indent=4)

    return render_template("register.html", success="Successfully registered!")

@app.route('/register', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        return do_register()
    else:
        return render_template("register.html")

def get_book(book_id):
    for book in books:
        if book.book_id == book_id:
            return book.__dict__  # Return dict
    return None

@app.route('/api/books')
def api_books():
    books_dicts = [book.__dict__ for book in books]
    return jsonify(books_dicts)

@app.route('/api/cart')
def api_cart():
    cart = session.get('cart', {})
    cart_items = []
    for book_id, qty in cart.items():
        if book_id is None or book_id == 'None' or book_id == '':
            continue  # skip invalid keys
        try:
            book_id_int = int(book_id)
        except ValueError:
            continue  # skip invalid keys
        book = get_book(book_id_int)
        if book:
            item = book.copy()
            item['quantity'] = qty
            cart_items.append(item)
    return jsonify(cart_items)


@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    book_id = str(data.get('book_id'))
    if book_id is None:
        return jsonify({"error": "Invalid book_id"}), 400
    book_id_str = str(book_id)
    cart = session.get('cart', {})
    cart[book_id] = cart.get(book_id_str, 0) + 1
    session['cart'] = cart
    return jsonify({"message": "Added", "cart": cart})

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.json
    book_id = str(data.get('book_id'))
    cart = session.get('cart', {})
    cart.pop(book_id, None)
    session['cart'] = cart
    return jsonify({"message": "Removed", "cart": cart})

if __name__ == '__main__':
    app.run(debug=True)
