from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
# import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafe.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class Cafe(db.Model):
    cafe_name = db.Column(db.String, primary_key=True)
    cafe_location = db.Column(db.String, nullable=False)
    open = db.Column(db.String, nullable=False)
    close = db.Column(db.String, nullable=False)
    coffee = db.Column(db.String, nullable=False)
    wifi = db.Column(db.String, nullable=False)
    power = db.Column(db.String, nullable=False)


class CafeList(db.Model):
    cafe_name = db.Column(db.String, primary_key=True)


db.create_all()


class CafeForm(FlaskForm):
    list_of_cafe = db.session.query(CafeList).all()
    choice = []
    # cafe = StringField(label='Cafe name', validators=[DataRequired()])
    for cafe in list_of_cafe:
        choi = (f"{cafe.cafe_name}", f"{cafe.cafe_name}")
        choice.append(choi)
    print(choice)
    cafe = SelectField(u'Cafe Name', choices=choice)
    location = StringField(label='Cafe Location on Google Maps (URL)', validators=[URL()])
    open_time = StringField(label='Opening Time e.g. 8AM', validators=[DataRequired()])
    close_time = StringField(label='Closing Time e.g. 05:30PM', validators=[DataRequired()])
    coffee_rating = SelectField(u'Coffee Rating', choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕', '☕☕☕☕☕☕'], default='☕', validators=[DataRequired()])
    wifi_rating = SelectField(u'Wifi Strength Rating', choices=['❌', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'], default='❌', validators=[DataRequired()])
    power_socket = SelectField(u'Power Socket Availability', choices=['❌', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], default='❌', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            cafe_name=form.cafe.data,
            cafe_location=form.location.data,
            open=form.open_time.data,
            close=form.close_time.data,
            coffee=form.coffee_rating.data,
            wifi=form.wifi_rating.data,
            power=form.power_socket.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        # with open('cafe-data.csv', mode='a', encoding='utf8') as csv_file:
        #     csv_file.write(f"\n{form.cafe.data},{form.location.data},{form.open_time.data},{form.close_time.data},"
        #                    f"{form.coffee_rating.data},{form.wifi_rating.data},{form.power_socket.data}")
        return redirect(url_for('add_cafe'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    # with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
    #     csv_data = csv.reader(csv_file, delimiter=',')
    #     list_of_rows = []
    #     for row in csv_data:
    #         list_of_rows.append(row)
    list_of_rows = db.session.query(Cafe).all()
    print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
