import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Column, String, Integer, ForeignKey, Numeric, Float, DateTime

from flask import Flask, jsonify, render_template, request, json
from flask_sqlalchemy import SQLAlchemy

import pymysql
import requests
import pymongo

app = Flask(__name__)

# engine = create_engine("sqlite:///hawaii.sqlite")
# Base = automap_base()
# Base.prepare(engine, reflect=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/hawaii.sqlite"
db = SQLAlchemy(app)

class measurement(db.Model):
    __tablename__ = 'measurement'
    
    station = db.Column(db.String, primary_key=True)
    date = db.Column(db.String)
    prcp = db.Column(db.Float)
    tobs = db.Column(db.Integer)

def __repr__(self):
        return '<measurement %r>' % (self.name)

class Station(db.Model):
    __tablename__ = 'Station'
    
    station = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    elevation = db.Column(db.Float)

def __repr__(self):
        return '<Station %r>' % (self.name)

# Measurement = Base.classes.measurement
# Station = Base.classes.station

# session = Session(engine)

@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()

@app.route("/")
def homepage():
    """List of all returnable API routes."""
    return(
        f"Available Routes:<br/>"
        f"(Note: Most recent available date is 2017-08-23 while the latest is 2010-01-01).<br/>"

        f"/api/v1.0/precipitation<br/>"
        f"Precipitaiton for all stations. <br/>"

        f"/api/v1.0/stations<br/>"
        f"Station list. <br/>"

        f"/api/v1.0/temperature<br/>"
        f"Temperature for all stations. <br/>"

        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"Max, Average, and Min temperature for given date.<br/>"

        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"Max, Average, and Min temperature for given period.<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = db.session.query(measurement.date, measurement.prcp).all()

    trace = {
        "date": dates,
        "precipitation": precip
    }

    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():
    results = db.session.query(Station.station, Station.name).all()
    
    return jsonify(results)


@app.route("/api/v1.0/temperature")
def temperature():
    results = db.session.query(measurement.date, measurement.tobs).all()
    return jsonify(results)


@app.route('/api/v1.0/<date>')
def given_date(date):
    results = db.session.query(func.max(measurement.tobs), func.avg(measurement.tobs), func.min(measurement.tobs)).\
        filter(measurement.date >= start_date, measurement.date == "2017-08-23").all()
    data_list = []
    for result in results:
        row = {}
        row['Date'] = result[0]
        row['Highest Temperature'] = float(result[1])
        row['Average Temperature'] = float(result[2])
        row['Lowest Temperature'] = float(result[3])
        data_list.append(row)
    return jsonify(data_list)


@app.route('/api/v1.0/<start_date>/<end_date>')
def query_dates(start_date, end_date):
    results = db.session.query(func.max(measurement.tobs), func.avg(measurement.tobs), func.min(measurement.tobs)).\
        filter(measurement.date >= start_date, measurement.date <= end_date).all()
    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = float(result[0])
        row["Highest Temperature"] = float(result[1])
        row["Lowest Temperature"] = float(result[2])
        data_list.append(row)
    return jsonify(data_list)


if __name__ == '__main__':
    app.run(debug=True)