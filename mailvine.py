from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

# from flask_mysqldb import MySQL

app = Flask(__name__)

# Secret Key to protect data. Protection against cookie data tampering.
app.config['SECRET_KEY'] = '2a44893ff4337692349481e9a9e77e75'


# Index
@app.route('/')
def index():
    return render_template('index.html')


# Login
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


# User Registration/Sign up
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created successfully. Congrats {form.firstName.data}!", 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
