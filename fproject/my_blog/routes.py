from flask import render_template, url_for, flash, redirect, request
from my_blog import app, db
from flask_login import current_user, login_user
from my_blog.forms import RegistrationForm, LoginForm
from my_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import os

db.init_app(app)

# Создание таблиц
with app.app_context():
    db.create_all()

# Функция для инициализации базы данных


def init_db():
    if not os.path.exists('initialized.flag'):
        with app.app_context():
            # Создание таблиц
            db.create_all()
            # Создание пользователя
            user1 = User(username='admin',
                         email='adminl@demo.com', password='111')
            db.session.add(user1)
            db.session.commit()
            # Создание флага
            with open('initialized.flag', 'w') as f:
                f.write('initialized')


# Вызов функции для инициализации базы данных
init_db()
posts = [
    {
        'author': 'Туленков Михаил',
        'title': 'Шифр-1: Цезаря',
        'content': 'Первая работа по шифрованию',
        'date_posted': '6 Октября, 2024'
    },
    {
        'author': 'Туленков Михаил',
        'title': 'Шифр-1: ',
        'content': 'Вторая работа по шифрованию',
        'date_posted': 'ноябрь 1, 2024'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title='О странице')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Учетная запись создана для {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:  # Сравнение паролей напрямую
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(
                'Вход неуспешный. Пожалуйста, проверьте имя пользователя и пароль', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
