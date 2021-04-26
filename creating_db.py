"""Import data from the .csv file to the sqlite database"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///statistics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Logs(db.Model):
    """The main table of the database"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.DateTime)
    channel = db.Column(db.String(50))
    country = db.Column(db.String(10))
    os = db.Column(db.String(20))
    impressions = db.Column(db.Integer)
    clicks = db.Column(db.Integer)
    installs = db.Column(db.Integer)
    spend = db.Column(db.Float)
    revenue = db.Column(db.Float)
    cpi = db.Column(db.Float)

    def __repr__(self):
        return '<Log %r>' % self.id


def load_data(file_name):
    """Returns all rows from the .csv file"""
    all_rows = []
    with open(file_name) as f:
        reader = csv.reader(f)
        for row in reader:
            all_rows.append(row)
    all_rows.remove(all_rows[0])
    return all_rows


if __name__ == "__main__":
    db.create_all()
    file_name = "data/dataset.csv"
    rows = load_data(file_name)
    # add the rows to the database
    i = 1
    for row in rows:
        try:
            datetime_object = datetime.strptime(row[0], '%Y-%m-%d')
            log = Logs(date=datetime_object, channel=row[1], country=row[2],
                       os=row[3], impressions=int(row[4]), clicks=int(row[5]),
                       installs=int(row[6]), spend=float(row[7]), revenue=float(row[8]),
                       cpi=(float(row[7]) / int(row[6])))
            db.session.add(log)
            db.session.flush()
            db.session.commit()
            i += 1
        except:
            print(i)
            db.session.rollback()
            print("There was some mistake.")
