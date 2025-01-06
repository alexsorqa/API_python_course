import requests

link = requests.get("https://playground.learnqa.ru/api/long_redirect")
url_history = [elem.url for elem in link.history]
print(f"Total redirections: {len(url_history)} and final url is: {url_history[-1]}")