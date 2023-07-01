from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime
import smtplib
import os
import bleach
from sqlalchemy.exc import NoResultFound

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


def clean_content(content):
    allowed_tags = ['a', 'abbr', 'acronym', 'address', 'b', 'br', 'div', 'dl', 'dt',
                    'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
                    'li', 'ol', 'p', 'pre', 'q', 's', 'small', 'strike',
                    'span', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
                    'thead', 'tr', 'tt', 'u', 'ul']
    allowed_attrs = {'a': ['href', 'target', 'title'], 'img': ['src', 'alt', 'width', 'height']}
    cleaned = bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs, strip=True)
    return cleaned


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    posts = db.session.query(BlogPost).all()
    for post in posts:
        if post.id == index:
            return render_template("post.html", post=post)


@app.route("/about")
def about():
    return render_template("about.html")


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
            return render_template('contact.html', msg=True)
    return render_template('contact.html', msg=False)


@app.route('/new-post', methods=['GET', 'POST'])
def new_post():
    create_post_form = CreatePostForm()
    if create_post_form.validate_on_submit() and request.method == 'POST':
        post = BlogPost(
            title=clean_content(request.form['title']),
            subtitle=clean_content(request.form['subtitle']),
            author=clean_content(request.form['author']),
            img_url=clean_content(request.form['img_url']),
            body=clean_content(request.form['body']),
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=create_post_form, new=True)


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    try:
        selected_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    except NoResultFound:
        return jsonify(response={'error': "Sorry no post with that ID was found in database."})
    else:
        edit_post_form = CreatePostForm(
            title=selected_post.title,
            subtitle=selected_post.subtitle,
            author=selected_post.author,
            img_url=selected_post.img_url,
            body=selected_post.body
        )
        if edit_post_form.validate_on_submit() and request.method == 'POST':
            selected_post.title = clean_content(request.form['title'])
            selected_post.subtitle = clean_content(request.form['subtitle'])
            selected_post.author = clean_content(request.form['author'])
            selected_post.img_url = clean_content(request.form['img_url'])
            selected_post.body = clean_content(request.form['body'])
            db.session.commit()
            return redirect(url_for('show_post', index=post_id))
        return render_template('make-post.html', form=edit_post_form, new=False)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    selected_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    db.session.delete(selected_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True)
