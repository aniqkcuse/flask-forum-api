import dotenv
import os
import requests

dotenv.load_dotenv()

class Test_auth():
    data_user = {"username":"testing1", "password":"password_testing", "email":"testing@mail.com"}
    user = requests.post("http://localhost:5000/api/v1/user/", json=data_user).json()
    header = {"Authorization": f"Bearer {user['access_token']}"}

    url_base = "http://localhost:5000/api/v1/auth/"
    authentication = {"username":"testing1", "password":"password_testing"}

    def test_login(self):
        user = requests.post(url=f"{self.url_base}", json=self.authentication)
        assert user.status_code == 200

    def test_logout(self):
        user = requests.delete(url=f"{self.url_base}", headers=self.header).json()
        assert user["msg"] == "JWT Revoked"
