import requests


def test_phrase_generator():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f"The phrase should be less then 15 characters long, but have {len(phrase)} instead."


def test_cookie():
    link = requests.get('https://playground.learnqa.ru/api/homework_cookie')
    cookie = link.cookies
    for name, value in cookie.items():
        print(f"Cookie: {name} = {value}")
        assert name == "HomeWork", "Unexpected cookie name."
        assert value == "hw_value", "Unexpected cookie value."


def test_headers():
    link = requests.get('https://playground.learnqa.ru/api/homework_header')
    headers = link.headers
    print(headers)
    assert len(headers.keys()) == 9 and len(headers.values()) == 9, f"None or not all headers are presented in API call"