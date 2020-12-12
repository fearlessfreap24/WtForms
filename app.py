from flask import Flask, render_template, session, url_for, redirect, request
from LoginForm import LoginForm as lf
from pymongo import MongoClient
from User import User, NewUser
# from flask_bcrypt import Bcrypt
import bcrypt
import os
from dotenv import load_dotenv
from flask_session import Session

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20)
app.config['SESSION_TYPE'] = "mongodb"
# flask_bcrypt = Bcrypt(app)
DBUSER = os.getenv("DBUSER")
DBPWD = os.getenv("DBPWD")
client = MongoClient('192.168.1.199',
                    username=DBUSER,
                    password= DBPWD,
                    authSource='pymongotest')
db = client.pymongotest
# collection = users
app.config['SESSION_MONGODB'] = client
app.config['SESSION_MONGODB_DB'] = 'pymongotest'
app.config['SESSION_MONGODB_COLLECT'] = 'sessions'
Session(app)


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
        
        finduser = db.users.find_one({"username": form.username.data })
        if finduser == None:
            return "No user found"
        elif bcrypt.checkpw(form.password.data.encode(), finduser["password"]):
            session['username'] = form.username.data
            return redirect(url_for('index'))
        else:
            return "Passwords do not match"

    return render_template('form.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    newuser = NewUser()

    if newuser.validate_on_submit():
        if newuser.password1.data == newuser.password2.data:
            pw = bcrypt.hashpw(newuser.password1.data.encode(), bcrypt.gensalt())
        else:
            error = 'Passwords do not match'
            return render_template('signup.html', form=newuser, error=error)

        fname = newuser.fname.data
        lname = newuser.lname.data
        email = newuser.email.data
        uname = newuser.username.data
        age = int(newuser.age.data)

        finduser = db.users.find_one({"$or": [{"email": email}, {"username": uname}]})
        print(finduser)
        if finduser == None:
            adduser = User(fname, lname, email, pw, uname, age).json()
            dbadd = db.users.insert_one(adduser)
            if dbadd:
                error = f"User {fname} {lname} has been added"
                return render_template('signup.html', form=newuser, error=error)
        else:
            error = 'User already exists'
            return render_template('signup.html', form=newuser, error=error)

        # return ''
    
    return render_template('signup.html', form=newuser)


if __name__ == "__main__":
    app.run(debug=True)
