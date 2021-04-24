from requests import get, post, delete, put


print(get('http://localhost:5000/api/add_customer').json())

print(post('http://localhost:5000/api/add_customer',  # Корректный запрос на добавление
           json={
               'surname': 'Popov',
               'name': 'Alex',
               'email': 'alex@mail.ru',
               'hashed_password': '000000'
           }).json())

print(get('http://localhost:5000/api/add_customer').json())
print(get('http://localhost:5000/api/customers/1').json())