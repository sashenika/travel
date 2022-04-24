from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class WaysForm(FlaskForm):
    way = StringField('Маршрут', validators=[DataRequired()])
    work_size = IntegerField('Длительность', validators=[DataRequired()])
    leader = StringField('Руководительr', validators=[DataRequired()])
    start_date = StringField('Дата начала')
    end_date = StringField('Дата окончания')
    is_finished = BooleanField("Is finished")
    categor = IntegerField('Категория')
    iname = StringField('Название реки  на английском')
    submit = SubmitField('Добавить')