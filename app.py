from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////.\vehicle_entry.db'
db = SQLAlchemy(app)

class Vehicle(db.Model):
    make = db.Column(db.String(20), primary_key=True)
    model = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer())

#con = sql.connect('./vehicle_entry.db')
#con.execute('CREATE TABLE IF NOT EXISTS vehicle_entry(make TEXT PRIMARY KEY, model TEXT, year INTEGER, color TEXT, price INTEGER)')

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
    return (render_template('entry.html', model=model, make=make))

@app.route('/view_cars', methods=['POST','GET'])
def view_cars():
    con = sql.connect('vehicle_entry.db')
    c = con.cursor()
    c.execute("SELECT * FROM vehicle_entry")
    display = c.fetchall()
    return render_template('view_cars.html', display=display)


if __name__ == '__main__':
    app.run(debug=True)
            
