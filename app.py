from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
from datetime import datetime

app = Flask(__name__)
app.secret_key = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////.\vehicle_entry.db'
db = SQLAlchemy(app)

# MAKES TABLE
class Vehicle(db.Model):
    make = db.Column(db.String(20), primary_key=True)
    model = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer())

class View_Past_Punches(db.Model):
    emp_id = db.Column(db.Integer(), primary_key=True, nullable=True)
    date = db.Column(db.String(40), nullable=False)

#con = sql.connect('./vehicle_entry.db')
#con.execute('CREATE TABLE IF NOT EXISTS view_past_punches(emp_id INTEGER PRIMARY KEY, date TEXT)')
#con = sql.connect('./vehicle_entry.db')
#con.execute('CREATE TABLE IF NOT EXISTS vehicle_entry(make TEXT PRIMARY KEY, model TEXT, year INTEGER, color TEXT, price INTEGER)')



@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/clock_in', methods=['POST'])
def clock_in(emp_id=None, date=None):
    emp_id = request.form['emp_ID']
    #Check emp_id db for correct id
    
    d = datetime.now()

    con = sql.connect('vehicle_entry.db')
    c = con.cursor()
    # The ID needs to be UNIQUE, off for testing
    c.execute("INSERT INTO view_past_punches (emp_id, date) VALUES (?, ?)", (emp_id, d,))
    con.commit()
    con.close()
    flash('You are clocked in at')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('home.html')


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
    return (render_template('entry.html', make=make, model=model, year=year, color=color, price=price))

@app.route('/view_cars', methods=['POST','GET'])
def view_cars():
    con = sql.connect('vehicle_entry.db')
    c = con.cursor()
    c.execute("SELECT * FROM vehicle_entry")
    display = c.fetchall()
    return render_template('view_cars.html', display=display)


if __name__ == '__main__':
    app.run(debug=True)

