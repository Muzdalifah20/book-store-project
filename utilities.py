import json

def get_html(html_page, error_message = ""):
    with open("templates/" +html_page + ".html", "r", encoding="utf-8") as html_file:
        content =  html_file.read()
        content = content.replace("$$error$$", error_message)
        return content
    
def usersdb():
    try:
        with open("usersdb.json","r")as file:
            users = json.load(file)
    except(FileNotFoundError):
        users = []
    return users