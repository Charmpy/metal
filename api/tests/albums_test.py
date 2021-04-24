from requests import get, post, delete, put


print(get('http://localhost:5000/api/albums').json())

print(post('http://localhost:5000/api/albums',  # Корректный запрос на добавление
           json={
               'title': 'black in black',
               'artistid': 10,
           }).json())

