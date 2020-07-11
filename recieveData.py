from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

# still need to give a command to render these in the html page
class HostForm(FlaskForm):
    name = StringField(
        "Name (1 to 20 characters)", validators=[DataRequired(), Length(min=1, max=20)])

    confirmHost = SubmitField('Host a Game')


class JoinForm(FlaskForm):
    name = StringField(
        "Name (1 to 20 characters)", validators=[DataRequired(), Length(min=1, max=20)])

    # need to figure out how to find the game with the specific code
    joincode = PasswordField("Join Code")

    joingame = SubmitField('Join Game')


