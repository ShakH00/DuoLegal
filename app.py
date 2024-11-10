from flask import Flask, render_template, request, redirect, url_for, session
import json

from bson import json_util

import UserMethods
from UserMethods import user
import UploadMethods as UP


app = Flask('__name__', template_folder='index')
app.secret_key = 'boi!#@$f23%^$^5u98pb7v9bu(*&*($^)(989540svirfuyvityr'



@app.route('/')
def home():
    if 'email' in session:
        print("in session")
        return render_template('home.html', username=session['email'])
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        pwd = request.form.get('password')

        # Simulated login check (replace with actual database verification)
        if username and pwd:  # Simulate successful login
            session['email'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid email or password!')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('email')
        pwd = request.form.get('password')
        first = request.form.get('first')
        last = request.form.get('last')
        location = request.form.get('location')
        # Simulate user registration
        session['email'] = username  # Log the user in after registration
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
