import os

from flask import Flask, render_template, request, url_for
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_restful import abort
from werkzeug.utils import redirect

from data import db_session
from data.geo_map import get_map
from data.ways import Ways
from data.user import User
from forms.ways import WaysForm
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    ways = db_sess.query(Ways).all()
    #  return redirect('/galery')
    return render_template("index.html", ways=ways)


@app.route('/marshrut')
def marshrut():
    db_sess = db_session.create_session()
    ways = db_sess.query(Ways).all()
    #  return redirect('/galery')
    return render_template("marshrut.html", ways=ways)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Req',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            town=form.town.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        with open(f'static/img/avatars/{user.id}.jpg', 'wb') as f:
            f.write(request.files['photo'].read())

        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/ways',  methods=['GET', 'POST'])
@login_required
def add_ways():
    form = WaysForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ways = Ways()
        ways.way = form.way.data
        ways.work_size = form.work_size.data
        ways.leader = form.leader.data
        ways.start_date = form.start_date.data
        ways.end_date = form.end_date.data
        ways.is_finished = form.is_finished.data
        ways.categor = form.categor
        ways.iname = form.iname
        ways.url = get_map(ways.iname)
        current_user.ways.append(ways)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('ways.html', title='Добавить маршрут', form=form)


@app.route('/ways/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ways(id):
    form = WaysForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        ways = db_sess.query(Ways).filter(Ways.id == id, Ways.user == current_user).first()
        if ways:
            form.way.data = ways.way
            form.work_size.data = ways.work_size
            form.leader.data = ways.leader
            form.start_date.data = ways.start_date
            form.end_date.data = ways.end_date
            form.is_finished.data = ways.is_finished
            form.categor.data = ways.categor
            form.iname.data = ways.iname
            form.url.data = ways.url
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ways = db_sess.query(Ways).filter(Ways.id == id, Ways.user == current_user).first()
        if ways:
            ways.way = form.way.data
            ways.work_size = form.work_size.data
            ways.leader = form.leader.data
            ways.start_date = form.start_date.data
            ways.end_date = form.end_date.data
            ways.is_finished = form.is_finished.data
            ways.categor = form.categor.data
            ways.iname = form.iname.data

            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('ways.html', title='Редактирование работы', form=form)


@app.route('/ways_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def ways_delete(id):
    db_sess = db_session.create_session()
    ways = db_sess.query(Ways).filter(Ways.id == id, Ways.user == current_user).first()
    if ways:
        db_sess.delete(ways)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/galery', methods=['POST', 'GET'])
def galery():
    title = 'Аватарки'
    pictures = os.listdir('static/img')
    if request.method == 'GET':
        return render_template('galery.html', pictures=pictures, title=title, lnp=len(pictures))
    elif request.method == 'POST':
        f = request.files['file']
        with open(f'static/img/{len(pictures) + 1}.jpg', 'wb') as file:
            file.write(f.read())
        return redirect('/galery')


def main():
    db_session.global_init("db/turizm.db")
    app.run()


if __name__ == '__main__':
    main()