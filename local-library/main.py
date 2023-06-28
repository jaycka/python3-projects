from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

bootstrap = Bootstrap5(app)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'test'
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"


class BookForm(FlaskForm):
    title = StringField(label='Book Name:', validators=[DataRequired()])
    author = StringField(label='Author:', validators=[DataRequired()])
    rating = StringField(label='Rating:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    rating = StringField('New Rating: ', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    form = BookForm()
    if form.validate_on_submit() and request.method == 'POST':
        db.session.add(Book(title=request.form['title'], author=request.form['author'], rating=request.form['rating']))
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    edit_form = EditForm()
    book_id = request.args.get('id')
    book_selected = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    if edit_form.validate_on_submit() and request.method == 'POST':
        book_selected.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book=book_selected, form=edit_form)


@app.route('/delete', methods=['GET', 'POST'])
def delete_entry():
    book_id = request.args.get('id')
    book_selected = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_selected)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
