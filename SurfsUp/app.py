# Dependencies
import numpy as np
import sqlalchemy
import datetime as dt
from datetime import timedelta
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(bind=engine)

#Create an app, being sure to pass_name_
app = Flask(__name__)

#Routes
@app.route("/")
def Home():
    #List all the available routes
    return (
        f"Welcome to Hawaii Climate Page<br/> "
        f"API Static Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"API Dynamic Route:<br/>"
        f"/api/v1.0/temp/start_date<br/>"
        f"/api/v1.0/temp/start_date/end_date<br/>"


    )


#Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session
    session = Session(engine)
    
    # Query all dates and precipitation
    data_prescipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        all()

    session.close()

   #Create a dictionary and append
    precipitation = []
    for date,prcp in data_prescipitation:
        prcp_dict_list = {}
        prcp_dict_list["date"] = date
        prcp_dict_list["prcp"] = prcp
        precipitation.append(prcp_dict_list)

    return jsonify(precipitation)


    # Stations Route
@app.route("/api/v1.0/stations")
def stations():
    # Create session
    session = Session(engine)

    """All stations names"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary and append
    stations = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations.append(stations_dict)

    return jsonify(stations)


#Tobs Route
@app.route("/api/v1.0/tobs")
def tobs():
# Create session
    session = Session(engine)

# Find lastest date in the data set.
    latest=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest

#most active stations (i.e. what stations have the most rows?)
    most_active_stations = session.query(Measurement.station, func.count(Measurement.id))\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.id).desc()).all()

    most_active_stations

#most active station (USC00519281) 
    temp_for_last_year= session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= "2016-08-23").\
filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all()
    temp_for_last_year
    session.close()

# Create a dictionary and append
    tobs_dict = dict(temp_for_last_year)
# return json list of dict
    return jsonify(tobs_dict)


# Start Route
@app.route("/api/v1.0/temp/<start_date>")
def begin (start_date=None):
    # Create session 
    #session = Session(engine)
    start_date = dt.datetime.strptime(start_date, "%m%d%Y")
    #print(start_date)
    temps= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    session.close()
    TMIN = temps[0][0]
    TMAX = temps[0][1]
    TAVG = temps[0][2]
    return jsonify({"Minium Temperature":TMIN,"Maximum Temperature":TMAX,"Average Temperature":TAVG})


#Ending Route
@app.route('/api/v1.0/<start_date>/<end_date>')
def ending (start_date=None, end_date=None):
    # Create session 
    #session = Session(engine)
    start_date = dt.datetime.strptime(start_date, "%m%d%Y")
    end_date = dt.datetime.strptime(end_date, "%m%d%Y")
    temps= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    session.close()
    TMIN = temps[0][0]
    TMAX = temps[0][1]
    TAVG = temps[0][2]
    return jsonify({"Minium Temperature":TMIN,"Maximum Temperature":TMAX,"Average Temperature":TAVG})



if __name__ == '__main__':
    app.run(debug=True)







