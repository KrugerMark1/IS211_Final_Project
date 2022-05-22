from flask import Flask, render_template, request, Response, redirect, url_for, session
import re
import json
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'COMPUTERSCIENCE'

# Create the database using the schema
def create_database(conn):
	create_table_post = '''CREATE TABLE post (
		id INTEGER PRIMARY KEY,
		title TEXT,
		published_date DATE,
		author TEXT,
		content TEXT,
		permalink_url TEXT
	);'''

	create_table_user = '''CREATE TABLE user (
		id INTEGER PRIMARY KEY,
		username TEXT,
	    password TEXT
	);'''

	cur = conn.cursor()

	cur.execute(create_table_post)
	cur.execute(create_table_user)

	conn.commit()

# Create a connection to the database
def create_connection(db_file):
	conn = sqlite3.connect(db_file)
	return conn

# Create a user via the provided data
def create_user(data):
	conn = create_connection("sqlite_database.db")

	sql = '''INSERT INTO user
			(id, username, password)
            VALUES
            (?, ?, ?)'''

	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

	conn.close()

# Create a post via the provided data
def create_post_in_database(data):
	conn = create_connection("sqlite_database.db")

	sql = '''INSERT INTO post
			(title, published_date, author, content, permalink_url)
            VALUES
            (?, ?, ?, ?, ?)'''

	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

	conn.close()

# Create and commit to database all default users information.
def create_default_users():
	conn = create_connection("sqlite_database.db")
	create_database(conn)

	conn.close()

	Users = [
		(1, 'admin', 'password'),
		(2, 'johndoe', 'password2'),
		(3, 'janedoe', 'password3'),
		(4, 'marcoskrguer', 'hal0wars4uditor3')
	]

	for user in Users:
		create_user(user)

# Check to see if the database file has the default information. 
def check_database_exists():
	conn = create_connection("sqlite_database.db")

	cur = conn.cursor()

	try: 
		cur.execute('SELECT * FROM user')

		rows = cur.fetchall()

	except:
		rows = []

	if len(rows) == 0:

		return(False)

	return(True)

# Select all posts in the database by reverse chronological order
def select_posts():
	conn = create_connection("sqlite_database.db")
	cur = conn.cursor()
	cur.execute('SELECT * FROM post ORDER BY published_date DESC')
	rows = cur.fetchall()
	conn.close()
	return(rows)

# Select a single post by id
def select_post_by_id(post_id):
	conn = create_connection("sqlite_database.db")
	cur = conn.cursor()
	cur.execute('SELECT * FROM post WHERE id=?', (post_id,))
	rows = cur.fetchall()
	conn.close()
	return(rows[0])

# Select a single post by permalink url
def select_post_by_permalink(permalink_url):
	conn = create_connection("sqlite_database.db")
	cur = conn.cursor()
	cur.execute('SELECT * FROM post WHERE permalink_url=?', (permalink_url,))
	rows = cur.fetchall()
	conn.close()
	return(rows[0])

# UPDATE a post in the database by id
def edit_post_in_database(data):
	conn = create_connection("sqlite_database.db")

	sql = '''UPDATE post
			set title = ?, 
				published_date = ?, 
				author = ?, 
				content = ?, 
				permalink_url = ?
            WHERE id = ?'''

	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

	conn.close()

# DELETE a post in the database by id
def delete_post_in_database(post_id):
	conn = create_connection("sqlite_database.db")

	sql = '''DELETE FROM post WHERE id=?'''

	cur = conn.cursor()
	cur.execute(sql, (post_id,))
	conn.commit()

	conn.close()

# GET - Show the user the homescreen and all posts in reverse chronological order.
@app.route('/', methods=['GET'])
def home():
	posts = select_posts()
	return(render_template('index.html', posts=posts))

# GET - Show the user their dashboard page if they are logged in
@app.route('/dashboard', methods=['GET'])
def dashboard():
	if session.get('auth'):
		messages = request.args.get('messages')
		posts = select_posts()
		return(render_template('dashboard.html', posts=posts, error_messages=messages))
	else:
		return(redirect('/login'))

# GET - Show page that allows user to input all the fields for a post
# POST - Process the data from the page and create that post in the database
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
	if session.get('auth'):
		if request.method == 'GET':
			messages = request.args.get('messages')
			return(render_template('create_post.html', error_messages=messages))

		elif request.method == 'POST':
			args = request.form
			now = datetime.now()
			published_date = now.strftime("%d/%m/%Y %H:%M:%S")

			permalink_url = f'/posts/{args.get("title").replace(" ", "-")}'

			post = (args.get('title'), published_date, args.get('author'), args.get('content'), permalink_url)

			print(post)

			# try:
			create_post_in_database(post)
			# except:
				# return(redirect(url_for('.create_post', messages="Error. Please try again. Check for blank fields or special characters.")))

			return(redirect('/dashboard'))

	else:
		return(redirect('/login'))

# GET - Show page that allows user to input all eidts to all fields in a post
# POST - Process the data from the page to edit any changed information
@app.route('/edit_post/<pid>', methods=['GET', 'POST'])
def edit_post(pid):
	if session.get('auth'):
		if request.method == 'GET':
			messages = request.args.get('messages')
			post = select_post_by_id(pid)
			return(render_template('edit_post.html', post=post, error_messages=messages))

		elif request.method == 'POST':
			args = request.form
			now = datetime.now()
			published_date = now.strftime("%d/%m/%Y %H:%M:%S")

			permalink_url = f'/posts/{args.get("title").replace(" ", "-")}'

			post_edits = (args.get('title'), published_date, args.get('author'), args.get('content'), permalink_url, pid)

			print(post_edits)

			try:
				edit_post_in_database(post_edits)
			except:
				return(redirect(url_for('.edit_post', pid=pid, messages="Error. Please try again. Check for blank fields or special characters.")))

			return(redirect('/dashboard'))

	else:
		return(redirect('/login'))

# POST - delete a post of a certain id
@app.route('/delete_post/<pid>', methods=['POST'])
def delete_post(pid):
	try:
		delete_post_in_database(pid)
	except:
		return(redirect(url_for('.dashboard', messages="Error. Please try again.")))

	return(redirect(url_for('.dashboard', messages="Post succesfully deleted.")))

# GET - Show the display page for a single post
@app.route('/posts/<permalink_url>', methods=['GET'])
def post_permalink_url(permalink_url):
	post = select_post_by_permalink(f'/posts/{permalink_url}')
	return(render_template('post.html', post=post))

# GET - Show page that allows user to input username and password
# POST - Process login and validate credentials. 
@app.route('/login', methods=['GET', 'POST'])
def login():

	if request.method == 'GET':
		messages = request.args.get('messages')
		return(render_template('login.html', error_messages=messages))

	elif request.method == 'POST':

		args = request.form

		login_details = {
		  "username": args.get('username'),
		  "password": args.get('password')
		}

		if login_details.get('username') == 'admin' and login_details.get('password') == 'password':
			session['auth'] = True
			return(redirect('/dashboard'))
		else:
			session['auth'] = False
			return(redirect(url_for('.login', messages="Error. Incorrect Login Credentials.")))

if __name__ == '__main__':
	if check_database_exists() == False:
		create_default_users()
	app.run()