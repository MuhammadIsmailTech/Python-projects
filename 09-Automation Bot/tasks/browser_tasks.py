import webbrowser
import urllib.parse

def google_search(query):
    q = urllib.parse.quote(query)
    webbrowser.open(f"https://www.google.com/search?q={q}")
    print("Searching:", query)

def open_website(url):
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    print("Opening website:", url)
