from flask import Flask

app = Flask(__name__)

@app.get("/api/v1/discussion/", method=["GET","POST"])
def get_discussion():
    return "<h1>Hello world</h1>"
