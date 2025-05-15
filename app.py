from flask import Flask , request,jsonify
from utilities import get_html , usersdb
import json
from bookclass import books

app = Flask(__name__)

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

    users = usersdb()
    users.append(new_user)
    with open("usersdb.json", "w") as file:
        json.dump(users, file, indent=4)

    return get_html("register", "")

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
                return get_html("index")
            else:
                return get_html("login","Password is not correct")
    return get_html("login", "User name is not correct")
 

def show_login():
    return get_html("login")

@app.route("/")
def index():
    return get_html("index")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_login()
    else:
        return show_login()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return do_register()
    else:
        return get_html("register")
    
@app.route("/api/books")
def api_books():
    books_data = [book.to_dict() for book in books]
    return jsonify(books_data)

@app.route("/cart")
def cart():
    return get_html("cart")

