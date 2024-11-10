from typing import Optional

import openai
from flask import Flask, render_template, request, redirect, url_for, session
import json

from openai import OpenAI
from dotenv import load_dotenv
import os

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

load_dotenv()

api_key = os.getenv("SECRET_1")
openai.api_key = api_key


def getUserName():
    all_users = UserMethods.get_all_users()
    userName = ""
    for user in all_users:
        if user['email'] == session['email']:
            userName += f"{user['name']} {user['lastname']}"
    return userName


def legalAIResponse(prompt):
    client = OpenAI()

    completion = client.chat.completions.create(

        model="gpt-4o-mini",
        messages=[

            {"role": "system", "content": "You are a helpful legal assistant."},
            {"role": "user", "content": prompt}

        ]
    )
    return completion.choices[0].message.content

@app.route('/')
def home():
    if 'email' in session:
        return render_template('home.html', username=session['email'], userName=getUserName())
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        pwd = request.form.get('password')
        email, password = UserMethods.get_user_credentials(username)
        #verify password
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
        bar_num = request.form.get('license_id')
        school = request.form.get('law_school')
        firm = request.form.get('law_firm')
        conc = "None"
        if bar_num == "" and school == "" and firm == "":
            new_person = user(first, last, email, pwd, location, conc, "no", bar_num, school, firm)
            new_person.insert_doc()

        else:
            new_person = user(first, last, email, pwd, location, conc, "yes", bar_num, school, firm)
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
    if 'email' in session:  # Need to be logged in to access claims page
        messages = []

        if request.method == 'POST':
            new_post = request.form.get('concern')
            if new_post:

                UP.upload_claim(session['email'], new_post)
                return redirect(url_for('claims'))  # Refresh page to show the new post

        elif request.method == 'GET':
            # Retrieve all posts for the logged-in user
            all_users = UserMethods.get_all_users()
            for user in all_users:
                for post in user["posts"]:
                    # Each post includes the main message and comments
                    messages.append({
                        "data": post["data"],
                        "comments": post.get("comments", [])
                    })

        return render_template('claims.html', messages=messages if messages else [], userName=getUserName())
    else:
        return render_template('login.html')

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if 'email' in session:
        message_data = request.form.get('message_data')  # The content of the message to identify it
        comment = request.form.get('comment')
        commenter_email = session['email']  # The email of the logged-in user
        original_poster = ""
        all_users = UserMethods.get_all_users()
        for user in all_users:
            for post in user["posts"]:
                if post['data'] == message_data:
                    original_poster = user['email']
        # Add the comment to the specified post
        UP.comment_on_post(original_poster, message_data, comment, commenter_email)

        return redirect(url_for('claims'))
    else:
        return redirect(url_for('login'))

response = ""
@app.route('/aichat', methods=['GET', 'POST'])
def aichat():
    if 'email' in session: #need to be logged in to access legal AI advice

        if request.method == 'POST':
            prompt = request.form.get('prompt')  # The content of the prompt
            global response
            response = legalAIResponse(prompt)
            return redirect(url_for('aichat'))  # Refresh page to show the new post

        print(response)
        return render_template('aichat.html', userName=getUserName(), response=response)
    else:
        return redirect(url_for('login'))


@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'email' in session: #need to be logged in to access account settings
        userName = getUserName()
        if request.method == 'POST':
            email: Optional[str] = request.form.get('email')
            user_to_update = {"email" : f"{session['email']}"}
            update_email = { '$set' :{ 'email' : f'{email}' }}
            result = user_collection.update_one(user_to_update, update_email)


            user_to_update = {"email": f"{email}"}
            pwd = request.form.get('password')
            update_pwd = {'$set':{'password': f'{pwd}'}}
            result = user_collection.update_one(user_to_update, update_pwd)

            first = request.form.get('first')
            update_first = {'$set': {'name': f'{first}'}}
            result = user_collection.update_one(user_to_update, update_first)


            last = request.form.get('last')
            update_last = {'$set': {'lastname': f'{last}'}}
            result = user_collection.update_one(user_to_update, update_last)

            location = request.form.get('location')
            update_loc = {'$set': {'location': f'{location}'}}
            result = user_collection.update_one(user_to_update, update_loc)
            session.pop('email', None)
            return redirect(url_for('login'))




        return render_template('account.html', userName=userName)
    else:
        return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)
