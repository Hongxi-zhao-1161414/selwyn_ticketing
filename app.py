from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from datetime import date, datetime, timedelta
import MySQLdb
from MySQLdb.cursors import DictCursor
import connect

app = Flask(__name__)
app.secret_key = '1234_fsaf7981——asas'

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

@app.template_filter('format_date')
def format_date(value):
    if isinstance(value, (date, datetime)):
        return value.strftime('%d/%m/%Y')
    return value

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
    cursor = getCursor()
    cursor.execute("SELECT event_name, event_date FROM events WHERE event_id = %s;", (event_id,))
    event = cursor.fetchone()

    if not event:
        flash("Event not found", "danger")
        return redirect(url_for('events'))

    qstr = """
          SELECT c.customer_id, c.first_name, c.family_name, c.date_of_birth, c.email, ts.tickets_purchased
          FROM customers c
          JOIN ticket_sales ts ON c.customer_id = ts.customer_id
          WHERE ts.event_id = %s
          ORDER BY c.family_name, c.first_name, c.date_of_birth DESC;
      """
    cursor.execute(qstr, (event_id,))
    customerlist = cursor.fetchall()

    return render_template("eventcustomerlist.html",
                           event_name=event['event_name'],
                           event_date=event['event_date'],
                           customerlist=customerlist)

@app.route("/customers")
def customers():
    cursor = getCursor()
    cursor.execute("SELECT * FROM customers ORDER BY family_name, first_name;")
    customers = cursor.fetchall()
    return render_template("customers.html", customers=customers)


@app.route("/search_customers", methods=["GET"])
def search_customers():
    search_query = request.args.get('search', '')
    results = []

    if search_query:
        cursor = getCursor()
        query = """
            SELECT * FROM customers 
            WHERE first_name LIKE %s OR family_name LIKE %s OR email LIKE %s
            ORDER BY family_name, first_name;
        """
        search_term = f"%{search_query}%"
        cursor.execute(query, (search_term, search_term, search_term))
        results = cursor.fetchall()

    return render_template("search_customers.html",
                           search_query=search_query,
                           search_results=results)


@app.route("/add_customer", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        first_name = request.form['first_name']
        family_name = request.form['family_name']
        date_of_birth = request.form['date_of_birth']
        email = request.form['email']

        if not all([first_name, family_name, date_of_birth, email]):
            flash("All fields are required", "danger")
            return render_template("add_edit_customer.html")

        cursor = getCursor()
        try:
            cursor.execute("SELECT MAX(customer_id) AS max_id FROM customers;")
            max_id = cursor.fetchone()['max_id'] or 0
            new_id = max_id + 1

            cursor.execute("""
                INSERT INTO customers (customer_id, first_name, family_name, date_of_birth, email)
                VALUES (%s, %s, %s, %s, %s);
            """, (new_id, first_name, family_name, date_of_birth, email))

            flash("Customer added successfully", "success")
            return redirect(url_for('customers'))
        except Exception as e:
            flash(f"Error adding customer: {str(e)}", "danger")

    return render_template("add_edit_customer.html")


@app.route("/edit_customer/<int:customer_id>", methods=["GET", "POST"])
def edit_customer(customer_id):
    cursor = getCursor()
    cursor.execute("SELECT * FROM customers WHERE customer_id = %s;", (customer_id,))
    customer = cursor.fetchone()

    if not customer:
        flash("Customer not found", "danger")
        return redirect(url_for('customers'))

    if request.method == "POST":
        first_name = request.form['first_name']
        family_name = request.form['family_name']
        date_of_birth = request.form['date_of_birth']
        email = request.form['email']

        try:
            cursor.execute("""
                UPDATE customers 
                SET first_name = %s, family_name = %s, date_of_birth = %s, email = %s
                WHERE customer_id = %s;
            """, (first_name, family_name, date_of_birth, email, customer_id))

            flash("Customer updated successfully", "success")
            return redirect(url_for('customer_summary', customer_id=customer_id))
        except Exception as e:
            flash(f"Error updating customer: {str(e)}", "danger")

    return render_template("add_edit_customer.html", customer=customer)


@app.route("/customer/<int:customer_id>")
def customer_summary(customer_id):
    cursor = getCursor()

    cursor.execute("SELECT * FROM customers WHERE customer_id = %s;", (customer_id,))
    customer = cursor.fetchone()

    if not customer:
        flash("Customer not found", "danger")
        return redirect(url_for('customers'))

    cursor.execute("""
        SELECT e.event_name, e.event_date, ts.tickets_purchased
        FROM ticket_sales ts
        JOIN events e ON ts.event_id = e.event_id
        WHERE ts.customer_id = %s;
    """, (customer_id,))
    purchases = cursor.fetchall()

    total_tickets = sum(p['tickets_purchased'] for p in purchases) if purchases else 0

    return render_template("customer_summary.html",
                           customer=customer,
                           purchases=purchases,
                           total_tickets=total_tickets)

@app.route("/futureevents")
def futureevents():
    today = date.today()

    cursor.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.age_restriction, e.capacity,
                   (e.capacity - COALESCE(SUM(ts.tickets_purchased), 0)) AS available_tickets
            FROM events e
            LEFT JOIN ticket_sales ts ON e.event_id = ts.event_id
            WHERE e.event_date >= %s
            GROUP BY e.event_id
            HAVING available_tickets > 0
            ORDER BY e.event_date;
        """, (today,))
    events = cursor.fetchall()

    return render_template("futureevents.html", events=events)


@app.route("/tickets/buy", methods=["GET", "POST"])
def buytickets():
    if request.method == "GET":
        event_id = request.args.get('event_id')
    else:
        event_id = request.form.get('event_id')

    cursor = getCursor()
    today = date.today()

    if request.method == "POST":
        event_id = request.form['event_id']
        customer_id = request.form['customer_id']
        tickets = int(request.form['tickets'])

        cursor.execute("""
                SELECT e.capacity, COALESCE(SUM(ts.tickets_purchased), 0) AS sold
                FROM events e
                LEFT JOIN ticket_sales ts ON e.event_id = ts.event_id
                WHERE e.event_id = %s
                GROUP BY e.event_id;
            """, (event_id,))
        event_data = cursor.fetchone()

        if not event_data:
            flash("Event not found", "danger")
            return redirect(url_for('buytickets'))

        available = event_data['capacity'] - event_data['sold']
        if tickets > available:
            flash(f"Only {available} tickets available", "danger")
            return redirect(url_for('buytickets', event_id=event_id))

        cursor.execute("""
                SELECT c.date_of_birth, e.age_restriction
                FROM customers c
                JOIN events e ON e.event_id = %s
                WHERE c.customer_id = %s;
            """, (event_id, customer_id))
        age_data = cursor.fetchone()

        if age_data:
            dob = age_data['date_of_birth']
            age_restriction = age_data['age_restriction']
            age = (today - dob).days // 365
            if age < age_restriction:
                flash(f"Customer must be at least {age_restriction} years old to attend this event", "danger")
                return redirect(url_for('buytickets', event_id=event_id))

        try:
            cursor.execute("""
                    INSERT INTO ticket_sales (customer_id, event_id, tickets_purchased)
                    VALUES (%s, %s, %s);
                """, (customer_id, event_id, tickets))

            flash(f"{tickets} tickets purchased successfully", "success")
            return redirect(url_for('customer_summary', customer_id=customer_id))
        except Exception as e:
            flash(f"Error purchasing tickets: {str(e)}", "danger")

    event = None
    if event_id:
        cursor.execute("""
                SELECT e.*, (e.capacity - COALESCE(SUM(ts.tickets_purchased), 0)) AS available_tickets
                FROM events e
                LEFT JOIN ticket_sales ts ON e.event_id = ts.event_id
                WHERE e.event_id = %s
                GROUP BY e.event_id;
            """, (event_id,))
        event = cursor.fetchone()

        if not event or event['available_tickets'] <= 0 or event['event_date'] < today:
            flash("No tickets available for this event", "danger")
            return redirect(url_for('futureevents'))

    cursor.execute("SELECT * FROM customers ORDER BY family_name, first_name;")
    customers = cursor.fetchall()

    return render_template("buytickets.html", event=event, customers=customers, today=today)


if __name__ == '__main__':
    app.run(debug=True)
