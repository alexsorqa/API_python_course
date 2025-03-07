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


def test_user_agent():
    user_agents = ['Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                   'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
                   'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
                   'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
                   ]
    total = {}
    for data in user_agents:
        link = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check", headers={"User-Agent": data})
        result = link.json()
        #print(result)
        for key, value in result.items():
            if value == 'Unknown':
                total.setdefault(data, [])
                if key not in total[data]:
                    total[data].append(key)
    assert not total, f"Some user agent parameters have 'Unknown' data. Please double check the result {total}"