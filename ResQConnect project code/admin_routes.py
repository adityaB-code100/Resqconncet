from flask import Blueprint, render_template, redirect, request, session, url_for, make_response
from extension import mongo
from collections import Counter
import plotly.graph_objs as go
import plotly
import json
from functools import wraps

admin_bp = Blueprint('admin', __name__)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/Admin")
@login_required
def dashboard():
    return render_template('Admin.html')


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "Admin" and password == "1234":
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("admin.dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@admin_bp.route("/admin/complaints")
@login_required
def ad_complaints():
    complaints = list(mongo.db.complaints.find())
    complaints.reverse()
    title = "Complaints Registered"
    return render_template('complaint.html', complaints=complaints, title=title)


@admin_bp.route("/admin/contact_request")
@login_required
def ad_contact_request():
    contacts = list(mongo.db.contacts.find())
    contacts.reverse()
    title = "Contact Request Registered"
    return render_template('complaint.html', complaints=contacts, title=title)


@admin_bp.route('/admin/data-graph')
@login_required
def data_graph():
    data = list(mongo.db.complaints.find())

    # Emergency Type Frequency
    emergency_types = [entry.get('emergency_type') for entry in data if entry.get('emergency_type')]
    type_counts = dict(Counter(emergency_types))
    bar_chart = go.Bar(x=list(type_counts.keys()), y=list(type_counts.values()), marker_color='rgb(66, 135, 245)')
    fig_type = go.Figure(data=[bar_chart], layout=go.Layout(title='Emergency Type Frequency'))
    graphJSON_type = json.dumps(fig_type, cls=plotly.utils.PlotlyJSONEncoder)

    # Complaints Per Day
    date_counts = Counter(
        entry['timestamp'].strftime('%Y-%m-%d')
        for entry in data if entry.get('timestamp')
    )
    line_chart = go.Scatter(x=sorted(date_counts), y=[date_counts[d] for d in sorted(date_counts)],
                            mode='lines+markers', marker=dict(color='rgb(255, 100, 100)'))
    fig_date = go.Figure(data=[line_chart], layout=go.Layout(title='Complaints Per Day'))
    graphJSON_date = json.dumps(fig_date, cls=plotly.utils.PlotlyJSONEncoder)

    # Emergencies by Location
    locations = [entry.get('location') for entry in data if entry.get('location')]
    location_counts = dict(Counter(locations))
    location_chart = go.Bar(x=list(location_counts.keys()), y=list(location_counts.values()),
                            marker_color='rgb(100, 200, 100)')
    fig_location = go.Figure(data=[location_chart], layout=go.Layout(title='Emergencies by Location'))
    graphJSON_location = json.dumps(fig_location, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("datagraph.j2",
                           graphJSON_type=graphJSON_type,
                           graphJSON_date=graphJSON_date,
                           graphJSON_location=graphJSON_location)


@admin_bp.route("/admin/Service_Register")
@login_required
def service_register():
    return render_template("Adservice.html")


@admin_bp.route('/add-service', methods=['POST'])
@login_required
def add_service():
    if request.method == 'POST':
        service = {
            "title": request.form['serviceTitle'],
            "image_url": request.form['serviceImage'],
            "number": request.form['helpline'],
            "description": request.form['firstAid']
        }
        mongo.db.card.insert_one(service)
        return redirect('/admin/Service_Register')
    return redirect("/admin")


# ------------------------
# Cache-Control: Prevent Back Button Issue
# ------------------------
@admin_bp.after_app_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
