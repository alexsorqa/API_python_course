import time
import requests

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
data = response.json()
print(data)

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": "QMxoTMyojNwASOw0SMw0SNyAjM"})
print(response.text)

time.sleep(16)

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": "QMxoTMyojNwASOw0SMw0SNyAjM"})
print(response.json())

