from flask import Flask, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sqlite3 as sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////.\vehicle_entry.db'
db = SQLAlchemy(app)

app.secret_key = 'this is secret'


class Vehicle(db.Model):
    make = db.Column(db.String(20), primary_key=True)
    model = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer())


@app.route('/', methods=['POST', 'GET'])
def login():
    error = None
    con = sql.connect('new_userbase.db')
    c = con.cursor()
    find_username = c.execute("SELECT new_username FROM new_userbase")
    username_fetch = find_username.fetchall()
    find_password = c.execute("SELECT new_password FROM new_userbase")
    password_fetch = find_password.fetchall()
    print(password_fetch)
    if request.method == 'POST':
        if request.form['username'] != username_fetch or request.form['password'] != password_fetch:
            error = 'Wrong user or pass'
        else:
            return render_template('dashboard.html')
    return render_template('login.html', error=error)


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')

@app.route('/new_register', methods=['POST', 'GET'])
def new_register(username=None, password=None):
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        con = sql.connect('new_userbase.db')
        c = con.cursor()
        c.execute('INSERT INTO new_userbase (new_username, new_password) VALUES (?,?)', (new_username, new_password))
        con.commit()
        con.close()
        

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/add_car')
def add_car():
    return render_template('add_car.html')


@app.route('/signup', methods=['POST', 'GET'])
def vehicle_entry(make=None, model=None, year=None, color=None, price=None):
    make = request.form['make']
    model = request.form['model']
    year = request.form['year']
    color = request.form['color']
    price = request.form['price']

    con = sql.connect('vehicle_entry.db')
    c = con.cursor()
    c.execute("INSERT INTO vehicle_entry (make, model, year, color, price) VALUES (?,?,?,?,?)",
              (make, model, year, color, price))
    con.commit()
    con.close()

    print(make, model)
    return (render_template('entry.html', model=model, make=make, year=year, color=color, price=price))


@app.route('/view_cars', methods=['POST', 'GET'])
def view_cars():
    con = sql.connect('vehicle_entry.db')
    c = con.cursor()

    make = c.execute('SELECT make FROM vehicle_entry')
    display_make = make.fetchall()

    model = c.execute("SELECT model FROM vehicle_entry")
    display_model = model.fetchall()
    
    c.close()

    return render_template('view_cars.html', display_model = display_model, display_make = display_make)

if __name__ == '__main__':
    app.run(debug=True)
