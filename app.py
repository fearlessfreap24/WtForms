from flask import Flask, render_template
from LoginForm import LoginForm as lf
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisamajorsecret'
dbuser = 'FLAKSADMIN'
dbuserpw = ''
MONGOURI = f'mongodb+srv://dylan:{dbuserpw}@cluster0.qqxpe.mongodb.net/<dbname>?retryWrites=true&w=majority'
mongo = MongoClient(MONGOURI)


@app.route('/form', methods=['GET', 'POST'])
def form():

    form = lf()

    if form.validate_on_submit():
        return "Form has been submitted for user " + form.username.data
    return render_template('form.html', form=form)


if __name__ == "__main__":
    app.run()
