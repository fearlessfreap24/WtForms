from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Length, Email, NumberRange
import pymongo

class User():
    fname = ''
    lname = ''
    email = ''
    password = ''
    username = ''
    age = 0

    def json(User):
        user = {
            'fname': User.fname,
            'lname': User.lname,
            'email': User.email,
            'password': User.password,
            'username': User.username,
            'age': User.age
        }

        return user


class NewUser(FlaskForm):
    fname = StringField("First Name", validators=[InputRequired(), Length(min=2)])
    lname = StringField("Last Name", validators=[InputRequired(), Length(min=2)])
    email = StringField("Email Address", validators=[InputRequired(), Email('An email address is required')])
    password1 = PasswordField("Password", validators=[InputRequired(), Length(min=5, max=20, message="Must be between 5 and 20 characters")])
    password2 = PasswordField("Verify Password", validators=[InputRequired(), Length(min=5, max=20, message="Must be between 5 and 20 characters")])
    username = StringField("Username", validators=[InputRequired(), Length(min=8, max=20)])
    age = IntegerField("Age", validators=[InputRequired(), NumberRange(min=10, max=100)])


if __name__ == "__main__":
    MONGOURI = f'mongodb://192.168.1.199:27017'
    mongo = pymongo.MongoClient(MONGOURI)
    db = mongo.pymongotest
    finduser = db.users.find_one({'fname':'Dylan'})

    newuser = User()
    newuser.fname = 'Dylan'
    newuser.lname = 'Perez'
    newuser.email = 'dylan@perez.com'
    newuser.password = 'testestest'
    newuser.username = 'dylan.perez'
    newuser.age = 46

    # print(newuser.json())

    # print(mongo.list_collection_names())

    # if finduser == None:
    #     mongo.pymongotest.users.insert_one(newuser.json())
    #     print('inserted newuser')
    # else:
    #     print(finduser)

    # db.users.update_one({'fname':'Dylan'}, {"$set": {'username':newuser.username}})

    finduser = db.users.find_one({'username':'dylan.perez'})

    for i in finduser:
        print(f"{i}: {finduser[i]}")
