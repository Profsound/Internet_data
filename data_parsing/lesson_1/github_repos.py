import requests as req

# Поcмотреть документацию к API Гитхаба.
# Разобраться и вывести список всех репозиториев для конкретного пользователя.

# Простое решение:
# В командной строке можно набрать команду и получить репозитории пользователя
# curl -i https://api.github.com/users/davisking/repos

# Но лучше создать небольшую функцию, которая возвращает
# список названий репозиториев по имени пользователя
def get_repositories(username):
    req_url = "https://api.github.com/users/%s/repos" %username
    r = req.get(req_url)
    data = r.json()
    return [x['full_name'] for x in data]

print(get_repositories('davisking'))
print(get_repositories('e-fominov'))


