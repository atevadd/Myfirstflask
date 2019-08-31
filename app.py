from flask import Flask, render_template, url_for, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager, mixins, logout_user, login_required
import models
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:atevadd@localhost:3306/niit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "ynI\xcc\xdb\x03\xd6QR8X\x12\xff\xd3Wv\xf3\x14{Z\xc5\x08"
app.config['extend_existing'] = True

db = SQLAlchemy(app)
login = LoginManager(app)
MyAnonymousUser = login.anonymous_user

# ? homepage
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# ? register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if name == '' or password == '':
            return render_template('register.html', message='Please Enter The Required Field')
        if db.session.query(models.User).filter(models.User.email == email).count() == 0:
            data = models.User(name=name, username=username,
                               email=email, password=password)
            db.session.add(data)
            db.session.commit()
            return render_template('login.html', mess='Signup Successful, Please Login.')
        return render_template('register.html', message='Email is already taken')
    return render_template('register.html')

# ? login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = models.User(username=username, password=password)
        if db.session.query(models.User).filter_by(username=username, password=password).count() >= 1:
            session['username'] = username
            return redirect(url_for('profile', username=username))
        else:
            return render_template('login.html', message='Incorrect Username or Password')
    return render_template('login.html')


@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    session['username'] = username
    return render_template('profile.html')


# ? logout
@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    return render_template('login.html')


@app.route('/todo', methods=['GET', 'POST'])
def todo():
    # user = User.query.filter_by(username).first()
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title == '':
            return render_template('todo.html', message='Please Enter a title')
        data = models.Todo(title=title, description=desc, user_id=current_user)
        db.session.add(data)
        db.session.commit()
        return render_template('profile.html', user_id=current_user )
    return render_template('todo.html')


if __name__ == '__main__':
    app.run(debug=True)
