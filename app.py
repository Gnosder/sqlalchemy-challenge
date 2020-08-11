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
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session from Python to the DB
    session = Session(engine)

    '''Convert Query to dict using date as the key and prcp as the value
    Return JSON of dict.'''

    import datetime as dt
    from dateutil.relativedelta import relativedelta as rd
    # Query
    last_date = session.query(func.max(Measurement.date)).first()
    d = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date()
    date = (d - rd(years=1)).strftime('%Y-%m-%d')

    q = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > date).\
        order_by(Measurement.date).all()

    out = dict(q)
    return jsonify(out)

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

    import datetime as dt
    from dateutil.relativedelta import relativedelta as rd
    # Query
    last_date = session.query(func.max(Measurement.date)).first()
    d = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date()
    date = (d - rd(years=1)).strftime('%Y-%m-%d')

    most_active = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc())

    most_active_station = most_active[0][0]

    most_active_year = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date > date).\
        group_by(Measurement.date).all()

    tobs = dict(most_active_year)
    
    return jsonify(tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create session from Python to the DB
    session = Session(engine)

    '''Return a JSON list of the minimum temperature, the average temperature, 
    and the max temperature for a given start or start-end range.
        When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for 
    all dates greater than and equal to the start date.
        When given the start and the end date, calculate the `TMIN`, `TAVG`, 
    and `TMAX` for dates between the start and end date inclusive.'''

    end='2017-08-23'
    lowest_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date > start).\
        filter(Measurement.date < end)[0]
    highest_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date > start).\
        filter(Measurement.date < end)[0]
    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date > start).\
        filter(Measurement.date < end)[0]

    listy = [lowest_temp[0], highest_temp[0], avg_temp[0]]

    return jsonify(listy)

@app.route("/api/v1.0/<start>/<end>")
def start_stop(start, end):
    # Create session from Python to the DB
    session = Session(engine)

    '''Return a JSON list of the minimum temperature, the average temperature, 
    and the max temperature for a given start or start-end range.
        When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for 
    all dates greater than and equal to the start date.
        When given the start and the end date, calculate the `TMIN`, `TAVG`, 
    and `TMAX` for dates between the start and end date inclusive.'''

    start = str(start)
    lowest_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date > start).\
        filter(Measurement.date < end)[0]
    highest_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date > start).\
        filter(Measurement.date < end)[0]
    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date > start).\
        filter(Measurement.date < end)[0]

    listy = [lowest_temp[0], highest_temp[0], avg_temp[0]]

    return jsonify(listy)


@app.route("/magic")
def magic():
    return "I didn't think you'd get this far so... you win?"


if __name__ == "__main__":
    app.run(debug=True)

# Debug URLs
# http://127.0.0.1:5000/api/v1.0/precipitation
# http://127.0.0.1:5000/api/v1.0/stations
# http://127.0.0.1:5000/api/v1.0/tobs
# http://127.0.0.1:5000/api/v1.0/2010-01-01
# http://127.0.0.1:5000/api/v1.0/2010-01-01/2017-08-23
# http://127.0.0.1:5000/magic