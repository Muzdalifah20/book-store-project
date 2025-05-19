import json

# creating html template
def get_html(html_page, placeholders=None):
    if placeholders is None:
        placeholders = {}

    with open(f"templates/{html_page}.html", "r", encoding="utf-8") as html_file:
        content = html_file.read()

        for key, value in placeholders.items():
            content = content.replace(f"$${key}$$", str(value) if value is not None else "")

        return content


# json to save the users data  
def usersdb():
    try:
        with open("data/usersdb.json","r")as file:
            users = json.load(file)
    except(FileNotFoundError):
        users = []
    return users
