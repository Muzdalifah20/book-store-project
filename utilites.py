import json

def get_html(html_page, error=None):
    with open("templates/"+html_page + ".html","r") as html_file:
        content = html_file.read()
    
    if error:
         content = content.replace("{{error}}", error)
    else:
         content = content.replace("{{error}}", "")

    return content

# def get_html(html_page, **kwargs):
#     with open(f"templates/{html_page}.html", "r", encoding="utf-8") as html_file:
#         content = html_file.read()

#     for key, value in kwargs.items():
#         placeholder = f"{{{{{key}}}}}"  # e.g., {{error}}
#         content = content.replace(placeholder, str(value) if value else "")

#     return content

def usersdb():
    #  case the file is empty
    try:
          with open("usersdb.json","r") as file:
               users = json.load(file)
    except(FileNotFoundError):
          users = []
    return users