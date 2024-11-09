from flask import Flask, render_template, request, redirect, url_for, session

app = Flask('__name__')
app.secret_key = 'boi!#@$f23%^$^5u98pb7v9bu(*&*($^)(989540svirfuyvityr'

#mongodb stuff


@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('index.html')
