from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku 


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://tuiicrvtgmutnr:258eb88df86dac9010e875b3da9f2ab2fb3fbba2bf066b45694deb78124ca844@ec2-23-21-165-188.compute-1.amazonaws.com:5432/dsiglfh5pnn6k"
heroku = Heroku(app)
db = SQLAlchemy(app)

class Blogs(db.Model): 
	__tablename__ = "blogs"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(60))
	author = db.Column(db.String(45))
	body = db.Column(db.Text())

	def __init__(self, title, author, body):
		self.title = title
		self.author = author
		self.body = body


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/blog_post', methods = ["POST"])
def blog_post():
	if request.content_type == 'application/json':
		post_data = request.get_json()
		title = post_data.get("title")
		author = post_data.get("author")
		body = post_data.get("body")
		reg = Blogs(title, author, body)
		db.session.add(reg)
		db.session.commit()
		return jsonify("Completed Transaction")
	return home()


@app.route('/return_blogs', methods=["GET"])
def return_blogs():
	all_blogs = db.session.query(Blogs.title, Blogs.author, Blogs.body).all()
	return jsonify(all_blogs)

@app.route('/return_blog/<id>', methods=["GET"])
def return_single_blog(id):
	one_blog = db.session.query(Blogs).get(id)
	return jsonify(one_blog)

@app.route('/update_blog/<id>', methods=["PUT"])
def blog_update(id):
	if request.content_type == 'application/json':
		post_data = request.get_json()
		title = post_data.get("title")
		author = post_data.get("author")
		body = post_data.get("body")
		record = db.session.query(Blogs).get(id)	
		record.title = title
		record.author = author
		record.body = body
		db.session.commit()
		return jsonify("Completed Update")
	return home()

@app.route('/delete/<id>', methods=["DELETE"])
def blog_delete(id):
	if request.content_type == 'application/json':
		post_data = request.get_json()
		record = db.session.query(Blogs).get(id)	
		db.session.delete(record)
		db.session.commit()
		return jsonify("Completed Deletion")
	return home()


if __name__ == '__main__':
	app.debug = True
	app.run()