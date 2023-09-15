from flask import Flask, redirect, request, render_template, url_for
import json

app = Flask(__name__)


def load_posts():
    with open('posts.json', 'r') as file:
        return json.load(file)


def update_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


def fetch_post_by_id(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


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


@app.route('/delete/<int:post_id>')
def delete(post_id):
    global blog_posts  # Access the global variable

    # Find the blog post with the given id and remove it from the list
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Update the JSON file
    update_posts(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Update the post in the JSON file
        post['author'] = author
        post['title'] = title
        post['content'] = content

        update_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:id>', methods=['POST'])
def like(id):
    post = fetch_post_by_id(id)
    if post is None:
        return "Post not found", 404

    post['likes'] += 1
    update_posts(blog_posts)

    return redirect(url_for('index'))


@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run()
