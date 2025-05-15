import json

def get_html(html_page):
    with open("templates/" +html_page + ".html", "r", encoding="utf-8") as html_file:
        content =  html_file.read()
        return content
    
def usersdb():
    try:
        with open("usersdb.json","r")as file:
            users = json.load(file)
    except(FileNotFoundError):
        users = []
    return users