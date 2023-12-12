import requests

class Test_user():
    data_user = {"username":"testing1", "password":"password_testing", "email":"testing@mail.com"}
    url_base = "http://localhost:5000/api/v1/user/"
    user = requests.post(url_base, json=data_user).json()
    header = {"Authorization": f"Bearer {user['access_token']}"}
    user_id = user['user']['id']

    def test_creation_user(self):
        user = requests.post(url=self.url_base, json=self.data_user).json()
        assert user["msg"] == "User created"

    def test_get_general_user(self):
        list_user = requests.get(url=self.url_base, headers=self.header)
        assert list_user.status_code == 200

    def test_get_one_user(self):
        user = requests.get(url=f"{self.url_base}{self.user_id}/", headers=self.header).json()
        assert self.data_user["username"] == user["username"]

    def test_update_user(self):
        new_data_user = {"username":"testing1_updated", "password":"password1_updated", "email":"testing2@mail.com"}
        user = requests.put(url=f"{self.url_base}{self.user_id}/", json=new_data_user, headers=self.header).json()
        print(user)
        assert user["msg"] == "User updated"

    def test_delete_user(self):
        user = requests.delete(url=f"{self.url_base}{self.user_id}/", headers=self.header).json()
        assert user["msg"] == "User deleted"
