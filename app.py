from flask import Flask, render_template
import json

app = Flask(__name__)


def load_posts():
    with open('posts.json', 'r') as file:
        return json.load(file)


def update_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run()
