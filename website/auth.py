from flask import Blueprint, render_template, flash, redirect
from .forms import SignUpForm, LoginForm, PasswordChangeForm
from flask_login import login_user, login_required, logout_user
from .models import Customer
from . import db
from flask import request


auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            new_customer = Customer()
            new_customer.email = email
            new_customer.username = username
            new_customer.password = password1

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account Created Succesully, You can now login')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account Not Created!, Email already exists')

            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''



    return render_template("sign_up.html", form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                return redirect('/')
            else:
                flash('Invalid Email or Password')
        else:
            flash('Account does not exist please sign up')

    return render_template("login.html", form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):
    customer = Customer.query.get(customer_id)  
    return render_template("profile.html", customer=customer)

@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):

    form = PasswordChangeForm() 

    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        customer = Customer.query.get(customer_id)
        

        if customer.verify_password(current_password):
            if new_password == confirm_new_password:
                customer.password = new_password
                db.session.commit()
                flash('Password Changed Successfully')
                return redirect(f'/profile/{customer_id}')
            else:
                flash('New Passwords do not match')
        else:
            flash('Current Password is Incorrect')
        

    return render_template('change_password.html', form=form)