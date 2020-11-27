import bcrypt
from flask import Flask, render_template, session, url_for, redirect
from LoginForm import LoginForm as lf
from pymongo import MongoClient
from User import User, NewUser
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
flask_bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = os.urandom(20)
MONGOURI = f'mongodb://192.168.1.199:27017'
mongo = MongoClient(MONGOURI)
db = mongo.pymongotest
# collection = users


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', user=session['username'])
    else:
        return redirect(url_for('signup'))


@app.route('/form', methods=['GET', 'POST'])
def form():

    form = lf()

    if form.validate_on_submit():
        pwhash = flask_bcrypt.generate_password_hash(password=form.password.data)
        session['username'] = form.username.data
        return redirect(url_for('index'))
    return render_template('form.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    newuser = NewUser()

    if newuser.validate_on_submit():
        return ''
    
    return render_template(url_for('signup.html'))


if __name__ == "__main__":
    app.run()
