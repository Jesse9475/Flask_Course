from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model): # Model for the database
    id = db.Column(db.Integer, primary_key = True) # Different Data Type, Primary Key means must be different from other id's
    title = db.Column(db.String(100), nullable = False) #character limit, cannot be blank
    content = db.Column(db.Text, nullable = False) # No limit, cannot be blank
    author = db.Column(db.String(20), nullable = False, default = 'N/A') # 20 char limit, but theres a default if not put in
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) #DateTime data type is just the time, default is the UTC (Universal Coordinated Time)
    
    def __repr__(self): #will print whenever a new blog post is created (the constructor)
        return 'Blog post ' + str(self.id)
    
    

@app.route('/')
def index():
    return render_template('index.html')

all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is the content of post 1. RRRR',
        'author': 'Jesse'
    },
    {
        'title': 'Post 2',
        'content': 'This is the content of post 2. PPPP'
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

