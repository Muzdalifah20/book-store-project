from flask import request ,session, url_for, redirect
import json
from .utilities import usersdb ,get_html
 

# hashing
def hashing(password):
    hashed = 0
    for char in password:
        hashed += ord(char)
    return str(hashed)
# validate user input
def validate_user_input(new_user):
    for key, value in new_user.items():
        if not value:
            return True, f"Please enter your {key}"
    users = usersdb()
    for user in users:
        if new_user["email"] == user["email"]:
            return True, "This email already exists"
    return False, ""

# do register
def do_register():
    first_name = request.form.get("first_name", "").strip().lower()
    last_name = request.form.get("last_name", "").strip().lower()
    email = request.form.get("email", "").strip().lower()
    password = hashing(request.form.get("password", ""))

    
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

    user_name_greeting = new_user.get("first_name").capitalize()
    session.permanent = True
    session["user_name"] = user_name_greeting
    

    # save the new_user information in jason file
    users = usersdb()
    users.append(new_user)
    with open("usersdb.json", "w") as file:
        json.dump(users, file, indent=4)

    return redirect(url_for("login"))
