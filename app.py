from flask import Flask, render_template, request, redirect, url_for, session

app = Flask('__name__', template_folder='index')
app.secret_key = 'boi!#@$f23%^$^5u98pb7v9bu(*&*($^)(989540svirfuyvityr'

#mongodb stuff


@app.route('/')
def home():
    if 'email' in session:
        return render_template('home.html', username=session['email'])
    else:
        return render_template('index.html')



@app.route('/')
def login():
    if request.method == 'POST':
        username = request.form['email']
        pwd = request.form['password']
        #add code to get from mongo db
        #if user and pwd = user[1]:
            #session['email'] = user[0]
            #return redirect(url_for('home'))
        #else
            #return render_template('login.html', error='Invalid email or password!')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)