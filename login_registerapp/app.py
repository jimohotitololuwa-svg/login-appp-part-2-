from flask import Flask, render_template, request
import requests
import sqlite3

app = Flask(__name__)

#connect to a database
def get_db():
    return sqlite3.connect("users.db")

# create a table if it doesnt exist
def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT ,
            email TEXT ,
            password TEXT
        );
    """ )

    db.commit()
    db.close()

create_table()

@app.route("/")
def index():
    return render_template("Login.html")

@app.route("/register")
def register():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM Users WHERE Name=?")
        account = cursor.fetchone()
        if account:
            msg = "Account already exists"
        else:
            cursor.execute("INSERT INTO Users (username, email, password) VALUES (?, ?, ?)", (username, email, password))

        db.commit()
        msg = "Registration successful!"

    db.close()


    return render_template("register.html", msg=msg)


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

app.run(debug=True)