import requests
import dotenv
import os

dotenv.load_dotenv()

class Test_topic():
    data_user = {"username":"testing1", "password":"password_testing", "email":"testing@mail.com"}
    user = requests.post("http://localhost:5000/api/v1/user/", json=data_user).json()
    header = {"Authorization": f"Bearer {user['access_token']}"}

    topic_data = {"name":"topic1"}
    url_base = "http://localhost:5000/api/v1/topic/"
    topic = requests.post(url_base, json=topic_data, headers=header).json()
    topic_id = topic["topic"]["id"]

    def test_create_topic(self):
        topic = requests.post(url=self.url_base, json=self.topic_data, headers=self.header).json()
        assert topic["msg"] == "Topic created"

    def test_get_all_topic(self):
        topic = requests.get(url=self.url_base, headers=self.header)
        assert topic.status_code == 200

    def test_get_one_topic(self):
        topic = requests.get(url=f"{self.url_base}{self.topic_id}", headers=self.header).json()
        assert topic["name"] == self.topic_data["name"]

    def test_update_topic(self):
        topic_data_update = {"name":"topic1_update"}
        topic = requests.put(url=f"{self.url_base}{self.topic_id}", json=topic_data_update, headers=self.header).json()
        assert topic["msg"] == "Topic updated"

    def test_delete_topic(self):
        topic = requests.delete(url=f"{self.url_base}{self.topic_id}", headers=self.header).json()
        assert topic["msg"] == "Topic deleted"

