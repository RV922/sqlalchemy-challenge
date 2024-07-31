# Import the dependencies.

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify ,render_template

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save reference to the table
Measurement = Base.classes.measurement
stations = Base.classes.station


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
def home_page():
    return (
        f"Home Page<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date,Measurement.prcp). \
    filter(Measurement.date >= prev_year).all()

    session.close()
    precip = {date:prcp for date,prcp in precipitation}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def resources():
    results = session.query(stations.station).all()
    session.close()
    all_St = list(np.ravel(results))
    return jsonify(all_St)


@app.route("/api/v1.0/tobs")
def observations():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
    filter(Measurement.station == "USC00519281"). \
    filter(Measurement.date  >= prev_year).all()
    session.close()

    obs = list(np.ravel(results))
    return jsonify(obs)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # start = dt.datetime.strptime(start,"%Y-%m-%d") # --> 2016-4-10
        results = session.query(*sel).\
        filter(Measurement.date >=start).all()
        session.close()
        temp = list(np.ravel(results))
        return jsonify(temp)
    
    # start = dt.datetime.strptime(start,"%Y-%m-%d") # --> 2016-4-10
    # end = dt.datetime.strptime(end,"%Y-%m-%d")
    results = session.query(*sel).\
    filter(Measurement.date >=start). \
    filter(Measurement.date <= end).all()

    session.close()
    temp = list(np.ravel(results))

    return jsonify(temp)
    


if __name__ == "__main__":
    app.run(debug=True)