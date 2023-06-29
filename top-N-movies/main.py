from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
bootstrap = Bootstrap5(app)
db = SQLAlchemy()
db.init_app(app)

search_url = "https://api.themoviedb.org/3/search/movie?&include_adult=false&language=en-US&page=1&"
movie_url = "https://api.themoviedb.org/3/movie/"
imdb_image_url = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2'

headers = {
    "accept": "application/json",
    "Authorization": os.environ.get('Authorization')
}


class RateMovieForm(FlaskForm):
    rating = FloatField(label='Your Rating Out of 10 e.g. 7.5', validators=[DataRequired(message='Can not be blank'),
                                                                            NumberRange(min=0, max=10,
                                                                                        message='Please enter your rating out of 10')])
    review = StringField(label='Your Review', validators=[DataRequired(message='Can not be blank')])
    submit = SubmitField('Done')


class AddMovieForm(FlaskForm):
    movie_name = StringField(label='Movie Title', validators=[DataRequired(message='Can not be blank')])
    submit = SubmitField('Add Movie')


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String, unique=True, nullable=True)
    img_url = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Movie {self.title}>"


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    all_movies = db.session.query(Movie).order_by(Movie.rating, Movie.id).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    edit_form = RateMovieForm()
    movie_id = request.args.get('id')
    movie_selected = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    if edit_form.validate_on_submit() and request.method == 'POST':
        movie_selected.rating = request.form['rating']
        movie_selected.review = request.form['review']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie_selected, form=edit_form)


@app.route('/delete')
def delete_entry():
    movie_id = request.args.get('id')
    movie_selected = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    db.session.delete(movie_selected)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['POST', 'GET'])
def add_movie():
    add_form = AddMovieForm()
    if add_form.validate_on_submit() and request.method == 'POST':
        url = f"{search_url}query={request.form['movie_name']}"
        response = requests.get(url=url, headers=headers)
        try:
            response.raise_for_status()
        except:
            movies = []
        else:
            movies = response.json()['results']
        finally:
            return render_template('select.html', movies=movies)
    return render_template('add.html', form=add_form)


@app.route('/find')
def find_movie():
    movie_id = request.args.get('movie_id')
    if movie_id:
        url = f"{movie_url}{movie_id}?language=en-US"
        response = requests.get(url=url, headers=headers)
        try:
            response.raise_for_status()
        except:
            return "<h1>Movie search failed!</h1>"
        else:
            movie_data = response.json()
            movie = Movie(title=movie_data['title'], img_url=imdb_image_url + movie_data['poster_path'],
                          year=movie_data['release_date'].split('-')[0], description=movie_data['overview'])
            db.session.add(movie)
            db.session.commit()

            return redirect((url_for('edit', id=movie.id)))


if __name__ == '__main__':
    app.run(debug=True)
