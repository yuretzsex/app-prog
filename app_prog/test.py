from app_prog.main import app
from app_prog.models import Base, engine, User, Announcement, Local, Public
from flask_jwt_extended import create_access_token
from app_prog.models import Session
import json

session = Session()

context = app.app_context()
context.push()
client = app.test_client()


# post user+
def test_new_user_200():
    user = {"username": "newUser",
            "firstName": "newFirstName",
            "lastName": "newLastName",
            "password": "88888888",
            "email": "newEmail@email.com",
            "phone": 38000000000,
            "city": "City"}
    url = "/user"
    response = client.post(url, data=json.dumps(user), content_type="application/json")
    assert response.status_code == 200


def test_login():
    url = "/login"
    user = {"username": "newUser", "password": "88888888"}
    response = client.get(url, data=json.dumps(user), content_type="application/json")

    assert response.status_code == 200


def test_login_failed():
    url = "/login"
    user = {"username": "", "password": ""}
    response = client.get(url, data=json.dumps(user), content_type="application/json")

    assert response.status_code == 400


# invalid post user input+
def test_new_user_invalid_username():
    user = {"username": "u",
            "firstName": "newFirstName",
            "lastName": "newLastName",
            "password": "12345678",
            "email": "newnewEmail@email.com",
            "phone": 3000000000,
            "city": "City"}
    url = "/user"
    response = client.post(url, data=json.dumps(user), content_type="application/json")
    assert response.status_code == 400


def test_new_user_invalid_firstname():
    user = {"username": "newnewuser",
            "firstName": "u",
            "lastName": "newLastName",
            "password": "12345678",
            "email": "newnewEmail@email.com",
            "phone": 3000000000,
            "city": "City"}
    url = "/user"
    response = client.post(url, data=json.dumps(user), content_type="application/json")
    assert response.status_code == 400


def test_new_user_invalid_lastname():
    user = {"username": "newnewuser",
            "firstName": "newFirstName",
            "lastName": "u",
            "password": "12345678",
            "email": "newnewEmail@email.com",
            "phone": 3000000000,
            "city": "City"}
    url = "/user"
    response = client.post(url, data=json.dumps(user), content_type="application/json")
    assert response.status_code == 400


def test_new_user_invalid_password():
    user = {"username": "newnewuser",
            "firstName": "newFirstName",
            "lastName": "newLastName",
            "password": "1",
            "email": "newnewEmail@email.com",
            "phone": 3000000000,
            "city": "City"}
    url = "/user"
    response = client.post(url, data=json.dumps(user), content_type="application/json")
    assert response.status_code == 400


def test_new_user_invalid_email():
    user = {"username": "newnewuser",
            "firstName": "newFirstName",
            "lastName": "newLastName",
            "password": "12345678",
            "email": "1",
            "phone": 3000000000,
            "city": "City"}
    url = "/user"
    response = client.post(url, data=json.dumps(user), content_type="application/json")
    assert response.status_code == 400


def test_new_user_invalid_number():
    user = {"username": "newnewuser",
            "firstName": "newFirstName",
            "lastName": "newLastName",
            "password": "12345678",
            "email": "newnewEmail@email.com",
            "phone": "s",
            "city": "City"}
    url = "/user"
    response = client.post(url, data=json.dumps(user), content_type="application/json")
    assert response.status_code == 400


def test_new_user_invalid_city():
    user = {"username": "newnewuser",
            "firstName": "newFirstName",
            "lastName": "newLastName",
            "password": "12345678",
            "email": "newnewEmail@email.com",
            "phone": 3000000000,
            "city": "s"}
    url = "/user"
    response = client.post(url, data=json.dumps(user), content_type="application/json")
    assert response.status_code == 400

# existing post user input
def test_new_user_exists_username():
    user = {"username": "newUser",
            "firstName": "newFirstName",
            "lastName": "newLastName",
            "password": "12345678",
            "email": "newEmail@email.com",
            "phone": 38000000000,
            "city": "City"}
    url = "/user"
    response = client.post(url, data=json.dumps(user), content_type="application/json")
    assert response.status_code == 400


def test_new_user_exists_phone():
    user = {"username": "newnewUser",
            "firstName": "newFirstName",
            "lastName": "newLastName",
            "password": "12345678",
            "email": "newEmail@email.com",
            "phone": 38000000000,
            "city": "City"}
    url = "/user"
    response = client.post(url, data=json.dumps(user), content_type="application/json")
    assert response.status_code == 400


def test_new_user_exists_email():
    user = {"username": "newnewUser",
            "firstName": "newFirstName",
            "lastName": "newLastName",
            "password": "12345678",
            "email": "newEmail@email.com",
            "phone": 3000000000,
            "city": "City"}
    url = "/user"
    response = client.post(url, data=json.dumps(user), content_type="application/json")
    assert response.status_code == 400


# put user
def test_update_user():
    access_token = create_access_token("newUser")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    user = {"city": "updatedCity"}
    url = "/user"
    response = client.put(url, data=json.dumps(user), content_type="application/json", headers=headers)

    assert response.status_code == 200


def test_update_user_exists_username():
    access_token = create_access_token("newUser")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    user = {"username": "brawlstars",}
    url = "/user"
    response = client.put(url, data=json.dumps(user), content_type="application/json", headers=headers)

    assert response.status_code == 400


def test_update_user_exists_email():
    access_token = create_access_token("newUser")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    user = {"email": "bestbrawler2008@ukr.net",}
    url = "/user"
    response = client.put(url, data=json.dumps(user), content_type="application/json", headers=headers)

    assert response.status_code == 400


def test_update_user_exists_phone():
    access_token = create_access_token("newUser")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    user = {"phone": "+38028813372"}
    url = "/user"
    response = client.put(url, data=json.dumps(user), content_type="application/json", headers=headers)

    assert response.status_code == 400


# get user
def test_get_user_id():
    userId = 1
    url = f"user/{userId}"
    response = client.get(url)

    assert json.loads(response.data) == {"user":
                {'id': 1,
                 'username': 'brawlstars',
                 'firstName':'Leon' ,
                 'lastName':'Vypav' ,
                 'email':'bestbrawler2008@ukr.net' ,
                 'phone': '+38028813372',
                 'city': 'Netishyn'}
                                }
    assert response.status_code == 200


def test_get_user_id_not_found():
    userId = 99
    url = f"user/{userId}"
    response = client.get(url)

    assert response.status_code == 404


def test_get_user_username():
    username = "newUser"
    url = f"user/username/{username}"
    response = client.get(url)

    assert response.status_code == 200


def test_get_user_username_not_found():
    username = ""
    url = f"user/{username}"
    response = client.get(url)

    assert response.status_code == 404


# login test


def test_login_username_not_found():
    url = "/login"
    user = {"username": "eqwewewqewqew", "password": "12345678"}
    response = client.get(url, data=json.dumps(user), content_type="application/json")

    assert response.status_code == 404


def test_login_password_not_found():
    url = "/login"
    user = {"username": "newUser", "password": "19945678"}
    response = client.get(url, data=json.dumps(user), content_type="application/json")

    assert response.status_code == 404


# post announcement method
def test_create_announcement_local():
    access_token = create_access_token("brawlstars")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = "/announcement"
    response = client.post(url, data=json.dumps(
        {"tittle": "Test Anons",
         "content": "TEST TEST",
         "isLocal": True}),
                           content_type="application/json", headers=headers)

    assert response.status_code == 200
    an = session.query(Announcement).filter_by(tittle='Test Anons')
    for i in an:
        url = f"/announcement/{i.id}"
        response = client.delete(url, headers=headers)
    assert response.status_code == 200


def test_create_announcement_public():
    access_token = create_access_token("brawlstars")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = "/announcement"
    response = client.post(url, data=json.dumps(
        {"tittle": " Public Test Anons",
         "content": "TEST TEST",
         "isLocal": False}),
                           content_type="application/json", headers=headers)
    session.commit()
    assert response.status_code == 200
    url =f"/announcement/{600000}"
    response = client.delete(url,headers=headers)
    assert response.status_code == 404
    an = session.query(Announcement).filter_by(tittle='Public Test Anons')
    for i in an:
        url =f"/announcement/{i.id}"
        response = client.delete(url,headers=headers)
        assert response.status_code == 200


def test_create_announcement_invalid_title():
    access_token = create_access_token("brawlstars")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = "/announcement"
    response = client.post(url, data=json.dumps(
        {"title": "1",
         "content": "TEST TEST"}),
                           content_type="application/json", headers=headers)

    assert response.status_code == 400


def test_create_announcement_invalid_content():
    access_token = create_access_token("brawlstars")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = "/announcement"
    response = client.post(url, data=json.dumps(
        {"title": "Test",
         "content": "1"}),
                           content_type="application/json", headers=headers)

    assert response.status_code == 400


# get methods
def test_get_list():
    url = '/announcement'
    response = client.get(url)
    assert response.status_code == 200


def test_get_local_list():
    access_token = create_access_token("brawlstars")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    url = '/announcement/local'
    response = client.get(url, headers=headers)
    assert response.status_code == 200


def test_get_announcement():
    url = f"/announcement/{2}"
    response = client.get(url)

    assert response.status_code == 200


def test_get_announcement_not_found():
    url = f"/announcement/{1000}"
    response = client.get(url)

    assert response.status_code == 404


def test_get_local_announcement():
    access_token = create_access_token("brawlstars")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = f"/announcement/local/{2}"
    response = client.get(url,headers=headers)
    assert response.status_code == 404


def test_get_local_announcement_not_found():
    access_token = create_access_token("brawlstars")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = f"/announcement/local/{1000}"
    response = client.get(url,headers=headers)
    assert response.status_code == 404


def test_get_local_announcement_not_allowed():
    url = f"/announcement/local/{1}"
    response = client.get(url)
    assert response.status_code == 401


def test_update_announcement():
    access_token = create_access_token("brawlstars")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = f"/announcement/{2}"
    response = client.put(url, data=json.dumps({"tittle": "test test"}), content_type="application/json", headers=headers)

    assert response.status_code == 200


def test_update_announcement_not_allowed():
    url = f"/announcement/{1}"
    response = client.put(url, data=json.dumps({"tittle": "a new one"}), content_type="application/json")

    assert response.status_code == 401


def test_delete_user():
    url = "/user"
    access_token = create_access_token("newUser")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.delete(url, headers=headers)

    assert response.status_code == 200


def test_delete_user_not_found():
    url = "user"
    access_token = create_access_token("notfound")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.delete(url, headers=headers)

    assert response.status_code == 404

