from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    comments = [
        {
            'author': {'username': 'B1-C1'},
            'body': 'Provisioned'
        },
        {
            'author': {'username': 'A1-C1'},
            'body': 'Needs Reclaim'
        }
    ]
    return render_template('index.html', title='Home', comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

    # racks = [
    #     {  
    #         'id': {
    #             'name': 'A1-C1',
    #             'location': 'Plano',
    #             'phase': 'A',
    #             'row': '1',
    #             'cabinet': '1'
    #         },
    #         'usage': {
    #             'a': 5.5,
    #             'b': 7
    #         },
    #         'service': {
    #             'a': 30,
    #             'b': 30
    #         }
    #     },
    #     {
    #         'location': {
    #             'phase': 'B',
    #             'row': '9',
    #             'cabinet': '1'
    #         },
    #         'usage': {
    #             'a': 3,
    #             'b': 6
    #         },
    #         'service': {
    #             'a': 30,
    #             'b': 30
    #         }
    #     }
    # ]
    # return render_template('index.html', title='Home', user=user, racks=racks)
    
    # pdu = [
    #     {
    #         'name': ''
            
    #     }
    # ]