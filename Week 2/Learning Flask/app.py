#Testing and learning how to use flask to create a website
#information from https://www.digitalocean.com/community/tutorials/how-to-create-your-first-web-application-using-flask-and-python-3

from flask import Flask

app = Flask(__name__)
@app.route('/')
def hello():
    return '<h1>Welcome</h1>'