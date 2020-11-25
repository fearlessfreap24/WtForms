from flask import Flask, render_template
from LoginForm import LoginForm as lf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisamajorsecret'


@app.route('/form', methods=['GET', 'POST'])
def form():

    form = lf()

    if form.validate_on_submit():
        return "Form has been submitted for user " + form.username.data
    return render_template('form.html', form=form)


if __name__ == "__main__":
    app.run()
