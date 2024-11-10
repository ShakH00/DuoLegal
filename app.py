from flask import Flask, render_template, request, redirect, url_for, session
import json

from bson import json_util
from pymongo import MongoClient

import UserMethods
from UserMethods import user
import UploadMethods as UP
client = MongoClient("mongodb+srv://saqibmaz:Mongodb%40Modulo48@cluster0.beh24.mongodb.net/?retryWrites=true&w=majority", ssl = True)
db = client['sadsDB']
user_collection = db['users']

app = Flask('__name__', template_folder='index')
app.secret_key = 'boi!#@$f23%^$^5u98pb7v9bu(*&*($^)(989540svirfuyvityr'



@app.route('/')
def home():
    if 'email' in session:
        return render_template('home.html', username=session['email'])
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        pwd = request.form.get('password')
        email, password = UserMethods.get_user_credentials(username)
        #Simulated login check (replace with actual database verification)
        if user.verify_password(password, pwd):  # Simulate successful login
            session['email'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid email or password!')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        first = request.form.get('first')
        last = request.form.get('last')
        location = request.form.get('location')
        conc = "None"
        new_person = user(first, last, email, pwd, location, conc)
        new_person.insert_doc()
        # Simulate user registration
        session['email'] = email  # Log the user in after registration
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

#password reset
@app.route('/password-reset')
def passwordreset():
    if request.method == 'POST':
        email = request.form.get('email')
        return redirect(url_for('login'))
    return render_template('password-reset.html')

@app.route('/claims', methods=['GET', 'POST'])
def claims():
    if 'email' in session: #need to be logged in to access claims page
        messages = []
        if request.method == 'POST':
            newPost = request.form.get('concern')
            if newPost:
                messages.append(newPost)
                UP.upload_claim(session['email'], newPost)
                return redirect(url_for('claims')) #refresh page so that it updates, adding the new post
        elif request.method == 'GET':
            m = UserMethods.get_all_users()
            for user in m:
                for post in user["posts"]:
                    messages.append(post["data"])
        return render_template('claims.html', messages=messages if messages else "")
    else:
        return render_template('login.html')

@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'email' in session: #need to be logged in to access account settings
        if request.method == 'POST':
            email = request.form.get('email')
            pwd = request.form.get('password')
            first = request.form.get('first')
            last = request.form.get('last')
            location = request.form.get('location')
            lawyer = request.form.get("lawyer")
            bar_num = request.form.get("bar")

        return render_template('account.html')
    else:
        return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)
