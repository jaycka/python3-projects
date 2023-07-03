from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from datetime import datetime
import smtplib
import os
import bleach
from sqlalchemy.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from functools import wraps
from flask import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##SET UP WEB AUTHENTICATION
login_manager = LoginManager()
login_manager.init_app(app)

##SET UP GRAVATER
gravatar = Gravatar(app,
                    size=50,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


##CONFIGURE TABLE
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    post = relationship("BlogPost", back_populates="author")
    comment = relationship("Comment", back_populates="comment_author")


class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = relationship("User", back_populates='post')

    comment = relationship("Comment", back_populates='parent_post')

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    comment_author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comment_author = relationship("User", back_populates="comment")
    parent_post_id = db.Column(db.Integer, db.ForeignKey("blog_post.id"))
    parent_post = relationship("BlogPost", back_populates="comment")


with app.app_context():
    db.create_all()


def clean_content(content):
    allowed_tags = ['a', 'abbr', 'acronym', 'address', 'b', 'br', 'div', 'dl', 'dt',
                    'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
                    'li', 'ol', 'p', 'pre', 'q', 's', 'small', 'strike',
                    'span', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
                    'thead', 'tr', 'tt', 'u', 'ul']
    allowed_attrs = {'a': ['href', 'target', 'title'], 'img': ['src', 'alt', 'width', 'height']}
    cleaned = bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs, strip=True)
    return cleaned


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == user_id).first()


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts, logged_in=current_user.is_authenticated)


@app.route("/post/<int:index>", methods=['GET', 'POST'])
def show_post(index):
    comment_form = CommentForm()
    requested_post = db.session.query(BlogPost).filter(BlogPost.id == index).first()
    if comment_form.validate_on_submit() and request.method == 'POST':
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
        comment = Comment(
            text=clean_content(request.form['comment']),
            comment_author_id=current_user.id,
            parent_post_id=requested_post.id
        )
        db.session.add(comment)
        db.session.commit()
    return render_template("post.html", post=requested_post, form=comment_form, logged_in=current_user.is_authenticated)


@app.route("/about")
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        try:
            with smtplib.SMTP(host='smtp.office365.com', port=587) as connection:
                connection.starttls()
                connection.login(user=os.environ.get('username'), password=os.environ.get('password'))
                connection.sendmail(
                    to_addrs='woaiwojialuther@gmail.com',
                    from_addr=os.environ.get('username'),
                    msg=f"Subject: {name} sent you a message\n\nName: {name}\n\nEmail: {email}\n\nPhone: {phone}\n\nMessage: {message}"
                )
        except:
            return "<h1>Email didn't send successfully, please try again!</h1>"
        else:
            return render_template('contact.html', msg=True, logged_in=current_user.is_authenticated)
    return render_template('contact.html', msg=False, logged_in=current_user.is_authenticated)


@app.route('/new-post', methods=['GET', 'POST'])
@login_required
@admin_only
def new_post():
    create_post_form = CreatePostForm()
    if create_post_form.validate_on_submit() and request.method == 'POST':
        post = BlogPost(
            title=clean_content(request.form['title']),
            subtitle=clean_content(request.form['subtitle']),
            author_id=current_user.id,
            img_url=clean_content(request.form['img_url']),
            body=clean_content(request.form['body']),
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=create_post_form, new=True, logged_in=current_user.is_authenticated)


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
@admin_only
def edit_post(post_id):
    try:
        selected_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    except NoResultFound:
        return jsonify(response={'error': "Sorry no post with that ID was found in database."})
    else:
        edit_post_form = CreatePostForm(
            title=selected_post.title,
            subtitle=selected_post.subtitle,
            img_url=selected_post.img_url,
            body=selected_post.body
        )
        if edit_post_form.validate_on_submit() and request.method == 'POST':
            selected_post.title = clean_content(request.form['title'])
            selected_post.subtitle = clean_content(request.form['subtitle'])
            selected_post.img_url = clean_content(request.form['img_url'])
            selected_post.body = clean_content(request.form['body'])
            db.session.commit()
            return redirect(url_for('show_post', index=post_id))
        return render_template('make-post.html', form=edit_post_form, new=False,
                               logged_in=current_user.is_authenticated)


@app.route('/delete/<int:post_id>')
@login_required
@admin_only
def delete(post_id):
    selected_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    db.session.delete(selected_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        if db.session.query(User).filter(User.email == request.form['email']).first():
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
        return redirect(url_for('get_all_posts'))
    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.session.query(User).filter(User.email == email).first()
        if not user:
            flash('That email does not exist, please try again.')
            return redirect(url_for('login'))
        elif not check_password_hash(pwhash=user.password, password=password):
            flash('Password incorrect, please try again.')

            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True)
