from flask import Flask, redirect, request, render_template, url_for
import json

app = Flask(__name__)


def load_posts():
    with open('posts.json', 'r') as file:
        return json.load(file)


def update_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


blog_posts = load_posts()


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        new_post = {
            'id': len(blog_posts) + 1,
            'author': author,
            'title': title,
            'content': content
        }

        blog_posts.append(new_post)
        update_posts(blog_posts)  # Update the JSON file

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run()
