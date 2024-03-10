#Turning in for at least credit
# Import the dependencies.

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
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
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query to retrieve the last 12 months of precipitation data
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp)\
                            .filter(Measurement.date >= one_year_ago).all()
    
    # Convert query results to a dictionary with date as key and precipitation as value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    # Return the JSON representation of the dictionary
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query to retrieve the list of stations
    stations_data = session.query(Station.station, Station.name).all()
    
    # Convert query results to a list of dictionaries
    stations_list = [{"Station": station, "Name": name} for station, name in stations_data]
    
    # Return the JSON representation of the list of dictionaries
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query to retrieve the most active station
    most_active_station_id = session.query(Measurement.station)\
                                .group_by(Measurement.station)\
                                .order_by(func.count(Measurement.station).desc())\
                                .first()[0]
    
    # Query to retrieve the last 12 months of temperature observation data for the most active station
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    temperature_data = session.query(Measurement.date, Measurement.tobs)\
                        .filter(Measurement.station == most_active_station_id)\
                        .filter(Measurement.date >= one_year_ago).all()
    
    # Convert query results to a list of dictionaries
    temperature_list = [{"Date": date, "Temperature": tobs} for date, tobs in temperature_data]
    
    # Return the JSON representation of the list of dictionaries
    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Query to calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start).all()
    
    # Convert query results to a list of dictionaries
    temperature_list = [{"Start Date": start,
                         "TMIN": temperature_stats[0][0],
                         "TAVG": temperature_stats[0][1],
                         "TMAX": temperature_stats[0][2]}]
    
    # Return the JSON representation of the list of dictionaries
    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Query to calculate TMIN, TAVG, and TMAX for dates between the start and end date (inclusive)
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start)\
                            .filter(Measurement.date <= end).all()
    
    # Convert query results to a list of dictionaries
    temperature_list = [{"Start Date": start,
                         "End Date": end,
                         "TMIN": temperature_stats[0][0],
                         "TAVG": temperature_stats[0][1],
                         "TMAX": temperature_stats[0][2]}]
    
    # Return the JSON representation of the list of dictionaries
    return jsonify(temperature_list)