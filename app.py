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
#mongo db stuff
client = MongoClient("mongodb+srv://MrVarmint_gw:5HUInvuir2390@cluster0.6fkb0.mongodb.net/cstuff?retryWrites=true&w=majority")
db = client['sadsDB']
user_collection = db['users']

app = Flask('__name__', template_folder='index')
app.secret_key = 'boi!#@$f23%^$^5u98pb7v9bu(*&*($^)(989540svirfuyvityr'

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


#helper method to get the username (first and last name) of an account
def getUserName():
    all_users = UserMethods.get_all_users()
    userName = ""
    for user in all_users:
        if user['email'] == session['email']:
            userName += f"{user['name']} {user['lastname']}"
    return userName

#method to use open AI for legal AI advice
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

#home app route
@app.route('/')
def home():
    if 'email' in session: #user is logged in, head to home page
        return render_template('home.html', username=session['email'], userName=getUserName())
    else: #user not logged in, use index.html instead
        return render_template('index.html')

#login method
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

#helper function used for ensuring license IDs for lawyers are 12 digit numbers
def is_valid_numeric_string(s):
    return s.isdigit() and len(s) == 12

#register account
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
        exists = False
        all_users = UserMethods.get_all_users()
        #for loop and if statement used to make sure the email isn't already in use
        for usr in all_users:
            if usr['email'] == email:
                exists = True
        if exists == True:
            return render_template('register.html', error="Email already in use!")
        else:
            if bar_num == "" and school == "" and firm == "":
                new_person = user(first, last, email, pwd, location, conc, "no", bar_num, school, firm)
                new_person.insert_doc()

            else:
                valid_num = is_valid_numeric_string(bar_num)
                if valid_num:
                    new_person = user(first, last, email, pwd, location, conc, "yes", bar_num, school, firm)
                else:
                    return render_template('register.html', error="License ID is invalid.")
                new_person.insert_doc()
            # Simulate user registration
            session['email'] = email  # Log the user in after registration
            return redirect(url_for('login'))
    return render_template('register.html')

#logout method
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

#contact form backend
@app.route('/submit-button', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # You can retrieve form data using request.form
        email = request.form.get('email')
        name = request.form.get('name')
        location = request.form.get('location')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Process the form data (e.g., save it to a database or send an email)

        if 'email' in session:
            return render_template('home.html', username=session['email'], userName=getUserName(), show_popup=True)
        else:
            return render_template('index.html', show_popup=True)

        # If the request method is GET, simply render the form
    return render_template('index.html')

#password reset
@app.route('/password-reset')
def passwordreset():
    if request.method == 'POST':
        email = request.form.get('email')
        return redirect(url_for('login'))
    return render_template('password-reset.html')

#claims page
@app.route('/claims', methods=['GET', 'POST'])
def claims():
    if 'email' in session:  # Need to be logged in to access claims page
        messages = []
        #posting something new
        if request.method == 'POST':
            new_post = request.form.get('concern')
            if new_post:

                UP.upload_claim(session['email'], new_post)
                return redirect(url_for('claims'))  # Refresh page to show the new post
        #viewing the page in general
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

#add comment on a claim post
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

#ai chat backend implementation
response = ""
prompt = ""
@app.route('/aichat', methods=['GET', 'POST'])
def aichat():
    if 'email' in session: #need to be logged in to access legal AI advice

        if request.method == 'POST':
            global prompt
            prompt = request.form.get('prompt')  # The content of the prompt
            global response
            response = legalAIResponse(prompt)
            return redirect(url_for('aichat'))  # Refresh page to show the new post

        return render_template('aichat.html', userName=getUserName(), response=response, question=prompt)
    else:
        return redirect(url_for('login'))

#account settings
@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'email' in session: #need to be logged in to access account settings
        userName = getUserName()
        if request.method == 'POST':

            #email: Optional[str] = request.form.get('email')
            #user_to_update = {"email" : f"{session['email']}"}
            #update_email = { '$set' :{ 'email' : f'{email}' }}
            #result = user_collection.update_one(user_to_update, update_email)


            #user_to_update = {"email": f"{email}"}
            #pwd = request.form.get('password')
            #update_pwd = {'$set':{'password': f'{pwd}'}}
            #result = user_collection.update_one(user_to_update, update_pwd)

            #first = request.form.get('first')
            #update_first = {'$set': {'name': f'{first}'}}
            #result = user_collection.update_one(user_to_update, update_first)


            #last = request.form.get('last')
            #update_last = {'$set': {'lastname': f'{last}'}}
            #result = user_collection.update_one(user_to_update, update_last)

            #location = request.form.get('location')
            #update_loc = {'$set': {'location': f'{location}'}}
            #result = user_collection.update_one(user_to_update, update_loc)
            session.pop('email', None)
            return redirect(url_for('login'))




        return render_template('account.html', userName=userName)
    else:
        return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)
