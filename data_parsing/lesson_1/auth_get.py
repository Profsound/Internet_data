import lesson_one.local as l
import requests as req

# Выполнить запрос методом GET к ресурсам,
# использующим любой тип авторизации через Postman, Python.

# Cоздаем небольшую функцию, которая возвращает
# id пользователя по емаилу

def get_user_by_email(email):
    params = {
               'api_key': l.api_key,
               'find_email': email,
               'method': 'flickr.people.findByEmail',
               'format': 'json'
             }
    req_url = "https://www.flickr.com/services/rest/"
    r = req.get(req_url, params=params)
    return r.text

print(get_user_by_email('anna@gmail.com'))

# Результат должен быть таким:
# jsonFlickrApi({"user":{"id":"90476509@N00","nsid":"90476509@N00",
# "username":{"_content":"annabesada"}},"stat":"ok"})

