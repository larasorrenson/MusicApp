
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, SelectField, DateField, TimeField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed
from flask import request
from .models import Concert
from wtforms import ValidationError
from . import db
import re


ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}


class ConcertForm(FlaskForm):
  EventName = StringField('Event Name', validators=[InputRequired()])
  # adding two validators, one to ensure input is entered and other to check if the 
  # description meets the length requirements
  EventDesc = TextAreaField('Description', validators = [InputRequired()])
  EventImage = FileField('Concert Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  EventDate = DateField('Date', validators=[InputRequired()])
  EventTime = TimeField('Time', validators=[InputRequired()])
  EventLocation = StringField('Location', validators=[InputRequired()])
  EventInfo = StringField('Additional Information', validators=[InputRequired()])
  EventPrice = StringField('Price', validators=[InputRequired()])
  EventTicketCount = StringField('Number of Tickets', validators=[InputRequired()])
  submit = SubmitField("Create")


class UpdateConcertForm(FlaskForm):
  EventName = StringField('Event Name', validators=[InputRequired()])
  EventDesc = TextAreaField('Description', validators = [InputRequired()])
  EventImage = FileField('Concert Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  EventDate = StringField('Date', validators=[InputRequired()])
  EventTime = StringField('Time', validators=[InputRequired()])
  EventLocation = StringField('Location', validators=[InputRequired()])
  EventInfo = StringField('Additional Information', validators=[InputRequired()])
  EventPrice = StringField('Price', validators=[InputRequired()])
  EventTicketCount = StringField('Number of Tickets', validators=[InputRequired()])
  submit = SubmitField("Update")


# creates the login information
class LoginForm(FlaskForm):
     user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
     password=PasswordField("Password", validators=[InputRequired('Enter user password')])
     submit = SubmitField("Login")

# this is the registration form
class RegisterForm(FlaskForm):
     user_name=StringField("User Name", validators=[InputRequired()])
     email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
     phone_num=StringField("Phone Number", validators=[InputRequired()])
     #linking two fields - password should be equal to data entered in confirm
     password=PasswordField("Password", validators=[InputRequired(),
                   EqualTo('confirm', message="Passwords should match")])
     confirm = PasswordField("Confirm Password")

     #submit button
     submit = SubmitField("Register")

class BookingForm(FlaskForm):
  TicketQuantity = IntegerField('Number of Tickets', validators=[InputRequired()])
  submit = SubmitField("Purchase")

  def validate_TicketQuantity(self, field):
      # Assuming you have a relationship between Booking and Concert models
      url = request.base_url
      event_id = int(re.search("ings/(.*?)/",url).group(1))


      print(event_id)
      query = db.select(Concert.EventStatus).where(Concert.id==event_id)
      status = db.session.execute(query).scalar()

      print(status)
      
      if status != 'open':
          raise ValidationError('Tickets can only be sold for events with "open" status')

class UpdateBookingForm(FlaskForm):
    TicketQuantity = IntegerField('Number of Tickets', validators=[InputRequired()])
    submit = SubmitField("Update")

    
class CommentForm(FlaskForm):
  CommentContent = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')