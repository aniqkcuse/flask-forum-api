import dotenv
import os
import requests

dotenv.load_dotenv()

class Test_comment():
    data_user = {"username":"testing1", "password":"password_testing", "email":"testing@mail.com"}
    user = requests.post("http://localhost:5000/api/v1/user/", json=data_user).json()
    header = {"Authorization": f"Bearer {user['access_token']}"}

    topic_data = {"name":"topic1"}
    topic = requests.post("http://localhost:5000/api/v1/topic/", json=topic_data, headers=header)

    discussion_data = {"topic":"topic1", "title":"title1", "description":"description1"}
    discussion = requests.post("http://localhost:5000/api/v1/discussion/", json=discussion_data, headers=header).json()
    print(discussion)
    discussion_id = discussion["discussion"]["id"]

    url_base = "http://localhost:5000/api/v1/comment/"
    comment_data = {"content":"content1","forum_id":discussion_id}
    comment = requests.post(url_base, json=comment_data, headers=header).json()
    comment_id = comment["comment"]["id"]

    def test_create_comment(self):
        comment = requests.post(url=self.url_base, json=self.comment_data, headers=self.header).json()
        assert comment["msg"] == "Comment created"

    def test_get_all_comment(self):
        comment = requests.get(url=self.url_base, headers=self.header)
        assert comment.status_code == 200

    def test_get_one_comment(self):
        comment = requests.get(url=f"{self.url_base}{self.comment_id}", headers=self.header).json()
        assert comment["content"] == self.comment_data["content"]

    def test_update_comment(self):
        comment_data_updated = {"content":"content1_updated", "forum_id":self.discussion_id}
        comment = requests.put(url=f"{self.url_base}{self.comment_id}", json=comment_data_updated, headers=self.header).json()
        assert comment["msg"] == "Comment update"

    def test_delete_comment(self):
        comment = requests.delete(url=f"{self.url_base}{self.comment_id}", headers=self.header).json()
        assert comment["msg"] == "Comment deleted"
