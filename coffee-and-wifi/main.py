from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


def choices(times: int, icon: str) -> str:
    return icon * (times+1)

class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    url = URLField(label='Location', validators=[URL()])
    open_time = StringField(label='Open', validators=[DataRequired()])
    close_time = StringField(label='Close', validators=[DataRequired()])
    coffee_rating = SelectField(label='Coffee', choices=[choices(i, '☕️') for i in range(5)], default='☕️')
    wifi = SelectField(label='Wifi', choices=['✘️']+[choices(i, '💪') for i in range(5)])
    power_outlet = SelectField(label='Power', choices=['✘️']+[choices(i, '🔌️') for i in range(5)])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        data = ['\n'+form.cafe.data, form.url.data, form.open_time.data, form.close_time.data, form.coffee_rating.data,
                form.wifi.data, form.power_outlet.data]
        with open('cafe-data.csv', 'a', encoding="utf8") as f:
            writer = csv.writer(f)
            writer.writerow(data)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding="utf8", newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
