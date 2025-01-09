import requests

#1 В этом случае выводится код 200 или сообщение о том что дан неправильный метод
link = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(link, link.text, sep='______')

#2 В этом случае выводится код 400 и/или отсутствует сообщение
link2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={'method': 'HEAD'})
print(link2, link2.text, sep='______')

#3 В этом случае выводится код 200 и/или сообщение {"success":"!"}
link3 = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={'method': 'PUT'})
print(link3, link3.text, sep='______')

#4
methods = ['GET', 'POST', 'PUT', 'DELETE']
total = {}

for key in methods:
    if key == 'GET':
        temp = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={'method': 'GET'})
        total.setdefault(key, []).extend(['GET:', temp.text])
    else:
        temp = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", data={'method': {key}})
        total.setdefault(key, []).extend(['GET:', temp.text])

for k in methods:
    if k == 'GET':
        temp = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", params={'method': 'GET'})
        total.setdefault(k, []).extend(['POST:', temp.text])
    else:
        temp = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", params={'method': {k}})
        total.setdefault(k, []).extend(['POST:', temp.text])

for elem in methods:
    if elem == 'GET':
        temp = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", params={'method': 'GET'})
        total.setdefault(elem, []).extend(['PUT:', temp.text])
    else:
        temp = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", params={'method': {k}})
        total.setdefault(elem, []).extend(['PUT:', temp.text])

for el in methods:
    if el == 'GET':
        temp = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", params={'method': 'GET'})
        total.setdefault(el, []).extend(['DELETE:', temp.text])
    else:
        temp = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", params={'method': {k}})
        total.setdefault(el, []).extend(['DELETE:', temp.text])

print('\n'.join(f"{k}: {v}" for k, v in total.items()))

