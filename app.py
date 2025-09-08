from flask import Flask

# Create an instance of the Flask web application
app = Flask(__name__)

# Define a route for the homepage URL ('/')
@app.route('/')
def hello():
	return '<h1>Hello, World! Your Python server is running on Ubuntu.</h1>'

# Define another route for a different page
@app.route('/about')
def about():
	return '<h3>This is the About page.</h3>'
