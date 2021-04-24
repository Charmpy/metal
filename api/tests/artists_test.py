from requests import get, post, delete


# print(get('http://localhost:5000/api/artists').json())
#
print(post('http://localhost:5000/api/artists',
           json={
               'name': 'Metallica'

           }
           ).json())

print(post('http://localhost:5000/api/artists',
           json={
               'name': 'Black Sabath'

           }
           ).json())

print(get('http://localhost:5000/api/artists').json())
#
# print(delete('http://localhost:5000/api/artists/2').json())
#
# print(get('http://localhost:5000/api/artists').json())