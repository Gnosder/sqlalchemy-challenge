import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func 

from flask import Flask, jsonify

# Database Setup
############################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Flask Setup
############################################################
app = Flask(__name__)

# Flask Routes
############################################################
@app.route("/")
def home():
    '''List all available api routes.'''
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session from Python to the DB
    session = Session(engine)

    '''Convert Query to dict using date as the key and prcp as the value
    Return JSON of dict.'''


@app.route("/api/v1.0/stations")
def stations():
# Create session from Python to the DB
    session = Session(engine)

    '''Return a JSON list of stations from the dataset.'''
    
    stations = session.query(Measurement.station).group_by(Measurement.station).all()
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
# Create session from Python to the DB
    session = Session(engine)

    '''Query the dates and temperature observations of the most 
    active station for the last year of data.
    Return a JSON list of temperature observations (TOBS) for the previous year.'''


@app.route("/api/v1.0/<start>/<end>")
def start(start, end=''):
    # Create session from Python to the DB
    session = Session(engine)

    '''Return a JSON list of the minimum temperature, the average temperature, 
    and the max temperature for a given start or start-end range.
        When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for 
    all dates greater than and equal to the start date.
        When given the start and the end date, calculate the `TMIN`, `TAVG`, 
    and `TMAX` for dates between the start and end date inclusive.'''



@app.route("/magic")
def magic():
    return "I didn't think you'd get this far so... you win?"


if __name__ == "__main__":
    app.run(debug=True)