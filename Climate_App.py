import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Homepage
# List all available API routes
@app.route("/")
def welcome():
    
    print("Server received request for 'Home' Page")
    return (
        f"Welcome to my 'Home' Page!<br/><br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Convert the query results to a Dictionary using date as the key and prcp as the value
# Return the JSON representation of your dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    data_precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= query_date).order_by(Measurement.date).all()

    # Define a dictionary and add in Key and Value from data_precipitation
    prcp_dict = {date:prcp for date, prcp in data_precipitation}

    return jsonify(prcp_dict)

# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    # To obtain a list of station from a list of tuples
    station = list(np.ravel(results))
    
    return jsonify(station)

# Query for the dates and temperature observations from a year from the last data point
# Return a JSON list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def temperature():

    query_date_temps = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    data_precipitation_temps = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= query_date_temps).order_by(Measurement.date).all()

    temp_dict = {date:tobs for date, tobs in data_precipitation_temps}
    
    return jsonify(temp_dict)

# Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start or start-end range
# When given the start only, calculate TMIN, TAVG, and TMAX 
# for all dates greater than and equal to the start date
# When given the start and the end date, calculate the TMIN, 
# TAVG, and TMAX for dates between the start and end date inclusive
@app.route("/api/v1.0/<start>")
def temperature():

    query_date_temps = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    data_precipitation_temps = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= query_date_temps).order_by(Measurement.date).all()

    temp_dict = {date:tobs for date, tobs in data_precipitation_temps}
    
    return jsonify(temp_dict)



if __name__ == '__main__':
    app.run(debug=True)