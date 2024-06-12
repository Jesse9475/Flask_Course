from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is the content of post 1. SIGMA',
        'author': 'Jesse'
    },
    {
        'title': 'Post 2',
        'content': 'This is the content of post 2. RiZZLER'
    }
]

@app.route('/posts')
def posts():
    return render_template('posts.html', posts = all_posts)

@app.route('/home')
@app.route('/home/<id>')
def hello(id=None):
    return "Hello, " + str(id)


@app.route('/onlyget', methods = ['POST', 'GET'])
def get_req():
    return 'You can only get this webpage.'

@app.route('/name/<username>')
def get_username(username = ''):
    return render_template('index.html', username = username)


if __name__ == "__main__":
    app.run(debug=True)

