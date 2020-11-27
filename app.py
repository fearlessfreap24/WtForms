import bcrypt
from flask import Flask, render_template, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from LoginForm import LoginForm as lf
from pymongo import MongoClient
from User import User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
flask_bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisamajorsecret'
MONGOURI = f'mongodb://192.168.1.199:27017'
mongo = MongoClient(MONGOURI)
db = mongo.pymongotest
# collection = users


@app.route('/')
def index():
    if 'username' in session:
        return f"You are logged in as {session['username']}"
    else:
        return redirect(url_for('form'))


@app.route('/form', methods=['GET', 'POST'])
def form():

    form = lf()

    if form.validate_on_submit():
        pwhash = flask_bcrypt.generate_password_hash(password=form.password.data)
        session['username'] = form.username.data
        return redirect(url_for('index'))
    return render_template('form.html', form=form)


if __name__ == "__main__":
    app.run()
