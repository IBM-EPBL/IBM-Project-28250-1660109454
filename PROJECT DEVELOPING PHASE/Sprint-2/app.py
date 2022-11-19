from flask import Flask, render_template, request, redirect
from newsapi import NewsApiClient
import os
import psycopg2

# init flask app
app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")
@app.route('/reg', methods=['GET', 'POST'])
def reg():
	print("Before")
	name = request.form['name']
	email = request.form['email']
	password = request.form['pass']
	print(name,email,password)
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute('select * from users')
	users=cur.fetchall()
	for i in users:
		if(email==i[1]):
			return render_template("register.html",msg="Email id Already Registerd.Please Login")
	cur.execute('insert into users (name,email,passwords) values(%s,%s,%s)',(name,email,password))
	conn.commit()
	cur.close()
	conn.close()
	return render_template("index.html",msg="Succesfully Registered Please Login To Continue")
    


if __name__ == "__main__":
	app.run(debug = True)
