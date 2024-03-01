from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, TEST you HURENSÖHNE! This is a change to test pre-commit'

@app.route('/about')
def about():
    return 'About'


if __name__ == '__main__':
    app.run(debug=True)