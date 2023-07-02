from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash, safe_join
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.exc import NoResultFound

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# Line below only required once, when creating DB.
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        user = User(
            email=request.form['email'],
            password=generate_password_hash(request.form['password'], 'pbkdf2', 8),
            name=request.form['name']
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('secrets'))
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = db.session.query(User).filter(User.email == email).one()
        except NoResultFound:
            flash('That email does not exist, please try again')
            return redirect(url_for('login'))
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Logged in successfully')
                return redirect(url_for('secrets'))
            else:
                flash('Password incorrect, please try again')
                return redirect(url_for('login'))
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name, logged_in=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download/<path:name>')
def download(name):
    # print(werkzeug.security.safe_join('files', name))
    return send_from_directory('static', safe_join('files', name))


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == user_id).one()


if __name__ == "__main__":
    app.run(debug=True)
