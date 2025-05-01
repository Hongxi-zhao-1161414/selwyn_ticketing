from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from datetime import date, datetime, timedelta
import MySQLdb
from MySQLdb.cursors import DictCursor
import connect

app = Flask(__name__)

connection = None
cursor = None

def getCursor():
    global connection
    global cursor

    if connection is None:
        connection = MySQLdb.connect(
            user=connect.dbuser,
            password=connect.dbpass,
            host=connect.dbhost,
            database=connect.dbname,
            port=int(connect.dbport),
            autocommit=True
        )
    cursor = connection.cursor(DictCursor)
    return cursor


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/events", methods=["GET"])
def events():
    cursor = getCursor()
    if request.method=="GET":
        # Lists the events        
        qstr = "select event_id, event_name from events;" 
        cursor.execute(qstr)        
        events = cursor.fetchall()

        return render_template("events.html", events=events)

@app.route("/events/customerlist", methods=["POST"])
def eventcustomerlist():
    event_id = request.form.get('event_id')
    # Display the list of customers who have purchased tickets for a particular event
    event_name = ""; # update to get the name of the event
    customerlist = {} # update to get the list of customers who have purchased tickets for a particular event
    return render_template("eventcustomerlist.html", event_name = event_name, customerlist = customerlist)


@app.route("/customers")
def customers():
    #List customer details.
    return render_template("customers.html")  


@app.route("/futureevents")
def futureevents():
    #Future Events which still have tickets available.
    return render_template("futureevents.html")  


@app.route("/tickets/buy")
def buytickets():
    #Buy tickets
    return render_template()