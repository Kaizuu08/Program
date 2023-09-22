#Testing and learning how to use flask to create a website
#information from https://www.digitalocean.com/community/tutorials/how-to-create-your-first-web-application-using-flask-and-python-3
#and https://www.youtube.com/watch?v=GHvj1ivQ7ms&t=180s&ab_channel=CodeVoid for virtual environment

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)