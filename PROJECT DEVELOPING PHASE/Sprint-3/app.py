from flask import Flask, render_template, request, redirect
from newsapi import NewsApiClient
import os
import psycopg2

# init flask app
app = Flask(__name__)




def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user='postgres',
                            password='tamil')
    return conn

# helper function
def get_sources_and_domains():
	all_sources = newsapi.get_sources()['sources']
	sources = []
	domains = []
	for e in all_sources:
		id = e['id']
		domain = e['url'].replace("http://", "")
		domain = domain.replace("https://", "")
		domain = domain.replace("www.", "")
		slash = domain.find('/')
		if slash != -1:
			domain = domain[:slash]
		sources.append(id)
		domains.append(domain)
	sources = ", ".join(sources)
	domains = ", ".join(domains)
	return sources, domains

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/check',methods=['GET','POST'])
def check():
	email=request.form['email']
	password=request.form['password']
	conn=get_db_connection()
	cur=conn.cursor()
	cur.execute('select * from users')
	users=cur.fetchall()
	flag=False
	for i in users:
		if(i[1]==email and i[2]==password):
			flag=True
	if(flag):
		return redirect("/home")
	else:
		return render_template("index.html",msg="email id/Password incorrect")

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
