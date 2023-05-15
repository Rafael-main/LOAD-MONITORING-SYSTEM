from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email


class LoginForm(FlaskForm):
    login_username = StringField('Username', validators=[InputRequired()])
    login_password = PasswordField('Password', validators=[InputRequired()])
    login_submit = SubmitField('Sign in')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    signup_submit = SubmitField('Sign Up')

class InputDataForm(FlaskForm):
    deptname = StringField('Department', validators=[InputRequired()])
    roomname = StringField('Room', validators=[InputRequired()])
    item = StringField('Item', validators=[InputRequired()])
    brandnameitem = StringField('Brand Name Item', validators=[InputRequired()])
    loadnums = IntegerField('Load Nums', validators=[InputRequired()])
    ratingsev = DecimalField('RatingsEV', validators=[InputRequired()])
    ratingsia = DecimalField('RatingsIA', validators=[InputRequired()])
    ratingspw = DecimalField('RatingsPW', validators=[InputRequired()])
    actualpw = DecimalField('ActualPW', validators=[InputRequired()])
    usagefactor = DecimalField('Usage Factor', validators=[InputRequired()])
    input_data_submit = SubmitField('Add Record')

class FilterForm(FlaskForm):
    def filterChoice():
        return [
            ('COE-EC', 'COE-EC'),
            ('ME - General Laboratory', 'ME - General Laboratory'),
            ('CERE', 'CERE'),
            ('DMET Fluid science lab', 'DMET Fluid science lab'),
            ('Comlab', 'Comlab'),
            ('FABLAB', 'FABLAB')
        ]
    filterData = SelectField('Filter by Department', choices=filterChoice)
    input_filter_submit = SubmitField('Filter')