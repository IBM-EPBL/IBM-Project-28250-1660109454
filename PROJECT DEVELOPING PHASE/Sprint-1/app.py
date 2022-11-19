from flask import Flask, render_template, request, redirect
from newsapi import NewsApiClient
import os
import psycopg2

# init flask app
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
	app.run(debug = True)
