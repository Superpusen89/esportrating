# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


from flask.ext.wtf import Form
from wtforms import validators, ValidationError
from wtforms.fields import TextField, TextAreaField, SubmitField, IntegerField
 
 
class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

class AddTeamForm(Form):
    teamName = TextField("Team name", [validators.Required("Please enter a team name.")])
    team_id = IntegerField("Team id", [validators.Required("Please enter a team id.")])
    submit = SubmitField("Send")
    
class AddPlayerForm(Form):
    username = TextField("Username", [validators.Required("Please enter a username.")])
    user_id = IntegerField("User id", [validators.Required("Please enter a user id.")])
    team_id = IntegerField("Team id", [validators.Required("Please enter a team id.")])
    submit = SubmitField("Send")