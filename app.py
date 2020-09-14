from flask import Flask, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
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

con = sql.connect('./vehicle_entry.db')
con.execute('CREATE TABLE IF NOT EXISTS userbase(username TEXT PRIMARY KEY, password TEXT)')


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['new_username'] != 'root' or request.form['new_password'] != 'toor':
            error = 'Wrong user or pass'
        else:
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        
        con = sql.connect('vehicle_entry.db')
        c = con.cursor()

        c.execute('INSERT INTO userbase (new_username, new_password) VALUES (?,?)', (new_username, new_password))

        con.commit()
        con.close()
        
        return redirect(url_for('dashboard', new_username = new_username, new_password =new_password))
    else:
        return render_template('register.html')
        
    return render_template('register.html')

@app.route('/dashboard', methods=['GET','POST'])
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
    c.execute("SELECT * FROM vehicle_entry")
    display = c.fetchall()

    return render_template('view_cars.html', display=display)


if __name__ == '__main__':
    app.run(debug=True)
