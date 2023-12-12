import dotenv
import requests
import os

dotenv.load_dotenv()

class Test_discussion():
    data_user = {"username":"testing1", "password":"password_testing", "email":"testing@mail.com"}
    user = requests.post("http://localhost:5000/api/v1/user/", json=data_user).json()
    header = {"Authorization": f"Bearer {user['access_token']}"}

    topic_data = {"name":"topic1"}
    requests.post("http://localhost:5000/api/v1/topic/", json=topic_data, headers=header)

    url_base = "http://localhost:5000/api/v1/discussion/"
    discussion_data = {"topic":"topic1", "title":"title1", "description":"description1"}
    discussion_id = requests.post(url_base, json=discussion_data, headers=header).json()["discussion"]["id"]

    def test_create_discussion(self):
        discussion = requests.post(url=self.url_base, json=self.discussion_data, headers=self.header).json()
        assert discussion["msg"] == "Discussion created"

    def test_get_all_discussion(self):
        discussion = requests.get(url=self.url_base, headers=self.header)
        assert discussion.status_code == 200

    def test_get_one_discussion(self):
        discussion = requests.get(url=f"{self.url_base}{self.discussion_id}", headers=self.header).json()
        assert discussion["title"] == self.discussion_data["title"]

    def test_update_discussion(self):
        discussion_data_update = {"topic":"topic1", "title":"title1_updated", "description":"description1_updated"}
        discussion = requests.put(url=f"{self.url_base}{self.discussion_id}", json=discussion_data_update, headers=self.header).json()
        assert discussion["msg"] == "Discussion updated"

    def test_delete_discussion(self):
        discussion = requests.delete(url=f"{self.url_base}{self.discussion_id}", headers=self.header).json()
        assert discussion["msg"] == "Discussion deleted"


