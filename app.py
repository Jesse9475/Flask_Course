from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home/<int:id>')
def hello(id):
    return "Hello, " + str(id)


@app.route('/onlyget', methods = ['POST', 'GET'])
def get_req():
    return 'You can only get this webpage.'

if __name__ == "__main__":
    app.run(debug=True)

