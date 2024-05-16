from urllib.parse import quote
import webbrowser

def multisearch(name_list):
    for name in name_list:
        if name == "":
            print("blank name")
            continue
        else:
            print(name)
            url = f"https://dak.gg/er/players/{quote(name)}"
            webbrowser.open(url)
