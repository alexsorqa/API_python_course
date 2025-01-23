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