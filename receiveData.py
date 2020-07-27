from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class JoinForm(FlaskForm):
    name = StringField(
        "Name (1 to 20 characters)", validators=[DataRequired(), Length(min=1, max=20)])


    joingame = SubmitField('Join Game')
