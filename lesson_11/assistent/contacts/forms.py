from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ContactForm(FlaskForm):
    name = TextAreaField("Enter name contact", validators=[DataRequired(), Length(min=2, max=140)])
    phone = TextAreaField("Enter phone contact", validators=[DataRequired(), Length(min=2, max=140)])
    birthday = TextAreaField("Enter birthday", validators=[DataRequired(), Length(min=2, max=140)])
    address = TextAreaField("Enter address", validators=[DataRequired(), Length(min=2, max=140)])
    email = TextAreaField("Enter email", validators=[DataRequired(), Length(min=2, max=140)])
    submit = SubmitField('Submit')
