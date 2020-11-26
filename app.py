from flask import Flask, render_template, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from LoginForm import LoginForm as lf
from pymongo import MongoClient
from User import User

app = Flask(__name__)
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
        return form()


@app.route('/form', methods=['GET', 'POST'])
def form():

    form = lf()

    if form.validate_on_submit():
        return "Form has been submitted for user " + form.username.data
    return render_template('form.html', form=form)


if __name__ == "__main__":
    app.run()
