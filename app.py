# make comparing logic for album mesh
# generate random albums (from list of albums)
# very basic buttons
# 

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

top_spotify_albums = [ "Un Verano Sin Ti - Bad Bunny", "÷ (Divide) - Ed Sheeran", "Starboy - The Weeknd",
                      "Hollywood's Bleeding - Post Malone", "Sour - Olivia Rodrigo", "After Hours - The Weekend",
                      "Dua Lipa - Dua Lipa", "Future Nostalgia - Dua Lipa", "Beerbongs & Bentleys - Post Malone",
                      "When We All Fall Asleep, Where Do We Go? - Billie Eilish" ]
top_spotify_albums_reversed = top_spotify_albums[::-1]
a = 0
b = 0
count_list = [0] * len(top_spotify_albums)

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


@app.route('/album_mesh', methods = ['GET', 'POST'])
def album_mesh():
    if a or b >= len(top_spotify_albums):
        return redirect('/album_mesh/results')
    else:
        return render_template('logic.html', a = a, b = b, song_a = top_spotify_albums[a], song_b = top_spotify_albums_reversed[b])

@app.route('/album_mesh/results', methods = ['POST'])
def album_mesh_results(count_list):
    top_songs_sorted = {}
    for i in range(0,len(top_spotify_albums)):
        top_songs_sorted[top_spotify_albums[i]] = count_list[i]
    top_songs_sorted = dict(sorted(top_songs_sorted.items(), key=lambda item: item[1], reverse=True))
    return render_template('results.html', top_spotify_albums, top_songs_sorted)

@app.route('/album_mesh/song_1/<int:a>', methods = ['GET', 'POST'])
def album_mesh_song_1(a = a, b =b , count_list = count_list):
    count_list[a] += 1
    b += 1
    return redirect('/album_mesh')

@app.route('/album_mesh/song_2/<int:b>', methods = ['GET', 'POST'])
def album_mesh_song_2(a = a, b =b , count_list = count_list):
    count_list[-(b+1)] += 1
    a += 1
    return redirect('/album_mesh')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        posts_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author = posts_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
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

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

if __name__ == "__main__":
    app.run(debug=True)