# Переводчик слов
# Используется для перевода "условий погоды" в команде /weather

import requests

API_KEY_TRANSL = '33569effd4msh09c2fdf1deea561p1ed1e2jsn3d2fd4806d5e'


def translation(phrase):
    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"

    querystring = {"langpair": "en|ru", "q": phrase, "mt": "1", "onlyprivate": "0", "de": "a@b.c"}

    headers = {
        'x-rapidapi-key': API_KEY_TRANSL,
        'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        rez = data['responseData']['translatedText']
        return rez
    else:
        return phrase
