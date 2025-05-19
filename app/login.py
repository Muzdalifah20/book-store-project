from flask import request, session, url_for, redirect
from .utilities import usersdb , get_html

# hashing
def hashing(password):
    hashed = 0
    for char in password:
        hashed += ord(char)
    return str(hashed)

@app.after_request
def add_security_headers(response):
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response
# # do the login
def do_login():
    email = request.form.get("email", "").strip().lower()
    password = hashing(request.form.get("password","").strip())
   
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
        if email == user.get("email"):
           
            if password == user.get("password"):
                email = user.get("email")
                    # adding session 
                session.permanent = True
                session["user_email"] = email
                
                session["user_name"] = user.get("first_name", "").capitalize()
                return redirect(url_for("user"))
            else:
              
                return get_html("login",{ "error":"Password is not correct"})
    return get_html("login", { "error":"User name is not correct"})
 

def show_login():
    return get_html("login", {"error": ""})
