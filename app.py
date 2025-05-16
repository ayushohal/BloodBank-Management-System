from flask import Flask, render_template, redirect, send_file, session, url_for, flash, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from werkzeug.security import check_password_hash
from functools import wraps
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = 'secret'

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-001:generateContent?key={GEMINI_API_KEY}"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:3306/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    hospital_name = db.Column(db.String(100), nullable=True)

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    blood_group = db.Column(db.String(5))
    contact = db.Column(db.String(20))

class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    blood_group = db.Column(db.String(5))
    units_required = db.Column(db.Integer)
    hospital_name = db.Column(db.String(100))
    contact = db.Column(db.String(20))  
    requested_by = db.Column(db.String(20))  
    status = db.Column(db.String(20), default="Pending")

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_group = db.Column(db.String(5), unique=True)
    units_available = db.Column(db.Integer)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'))
    recipient_name = db.Column(db.String(100))
    blood_group = db.Column(db.String(5))
    unit_donated = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

def login_required(user_type):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session or session.get('user_type') != user_type:
                return redirect(url_for(f'{user_type}_login'))
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/bloodbank_login', methods=['GET', 'POST'])
def bloodbank_login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password_input):
          if user.role == 'bloodbank':
            session['user_id'] = user.id
            session['user_type'] = 'bloodbank'
            return redirect('/bloodbank/inventory')
        else:
            flash('Invalid username or password.')

    return render_template('bloodbank_login.html')

@app.route('/bloodbank/add_donor', methods=['GET', 'POST'])
@login_required('bloodbank')
def add_donor():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        blood_group = request.form['blood_group']
        contact = request.form['contact']

        donor = Donor(name=name, age=age, email=email, blood_group=blood_group, contact=contact)
        db.session.add(donor)

        inventory_entry = Inventory.query.filter_by(blood_group=blood_group).first()
        if inventory_entry:
            inventory_entry.units_available += 1
        else:
            new_inventory = Inventory(blood_group=blood_group, units_available=1)
            db.session.add(new_inventory)

        db.session.commit()
        return redirect('/bloodbank/view_donors')
    return render_template('bloodbank/add_donor.html')

@app.route('/bloodbank/view_donors')
@login_required('bloodbank')
def view_donors():
    donors = Donor.query.all()
    return render_template('bloodbank/view_donors.html', donors=donors)

@app.route('/bloodbank/inventory')
@login_required('bloodbank')
def inventory():
    inventory = Inventory.query.all()
    return render_template('bloodbank/inventory.html', inventory=inventory)

@app.route('/bloodbank/request_blood', methods=['GET', 'POST'])
@login_required('bloodbank')
def bloodbank_request():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        blood_group = request.form['blood_group']
        units_required = request.form['units_required']
        hospital_name = request.form['hospital_name']
        contact = request.form['contact']  

        recipient = Recipient(
            name=name,
            age=age,
            email=email,
            blood_group=blood_group,
            units_required=units_required,
            hospital_name=hospital_name,
            contact=contact
        )
        db.session.add(recipient)
        db.session.commit()
        return redirect('/bloodbank/view_requests')
    return render_template('bloodbank/request_blood.html')

@app.route('/bloodbank/view_requests', methods=['GET', 'POST'])
@login_required('bloodbank')
def view_requests():
    if request.method == 'POST':
        request_id = request.form['id']
        action = request.form['action']
        req = Recipient.query.get(request_id)

        if req and action == 'Approved' and req.status != 'Approved':
            req.status = 'Approved'
            inventory_entry = Inventory.query.filter_by(blood_group=req.blood_group).first()
            if inventory_entry and inventory_entry.units_available >= req.units_required:
                inventory_entry.units_available -= req.units_required
                donation = Donation(
                    recipient_id=req.id,
                    recipient_name=req.name,
                    blood_group=req.blood_group,
                    unit_donated=req.units_required,
                    date=datetime.utcnow()
                )
                db.session.add(donation)
            else:
                return "Error: Not enough blood units available for approval.", 400
            db.session.commit()

        elif req:
            req.status = action
            db.session.commit()

    requests_list = Recipient.query.all()
    return render_template('bloodbank/view_requests.html', requests=requests_list)

@app.route('/bloodbank/donations', methods=['GET', 'POST'])
@login_required('bloodbank')
def view_donations():
    filters = []
    sort_by = Donation.date.asc()

    if request.method == 'POST':
        blood_group = request.form.get('blood_group')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        sort_option = request.form.get('sort_order')

        if blood_group:
            filters.append(Donation.blood_group == blood_group)
        if start_date:
            try:
                filters.append(Donation.date >= datetime.strptime(start_date, '%Y-%m-%d'))
            except ValueError:
                pass
        if end_date:
            try:
                filters.append(Donation.date <= datetime.strptime(end_date, '%Y-%m-%d'))
            except ValueError:
                pass

        if sort_option == 'asc':
            sort_by = Donation.date.asc()
        elif sort_option == 'desc':
            sort_by = Donation.date.desc()

    donations = Donation.query.filter(*filters).order_by(sort_by).all()

    session['filtered_ids'] = [d.id for d in donations]

    return render_template('bloodbank/donations.html', donations=donations)

@app.route('/download_pdf', methods=['GET'])
@login_required('bloodbank')
def download_pdf():
    filtered_ids = session.get('filtered_ids')
    
    if filtered_ids:
        donations = Donation.query.filter(Donation.id.in_(filtered_ids)).all()
    else:
        donations = Donation.query.all()

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Heading
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 30, "Blood Donation Report")
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 50, f"Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Table headers
    y = height - 80
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y, "ID")
    c.drawString(70, y, "Recipient Name")
    c.drawString(200, y, "Blood Group")
    c.drawString(280, y, "Units Donated")
    c.drawString(380, y, "Date")
    y -= 20

    c.setFont("Helvetica", 10)
    for donation in donations:
        if y < 50:
            c.showPage()
            y = height - 50
        c.drawString(30, y, str(donation.id))
        c.drawString(70, y, donation.recipient_name)
        c.drawString(200, y, donation.blood_group)
        c.drawString(280, y, str(donation.unit_donated))
        c.drawString(380, y, donation.date.strftime('%Y-%m-%d'))
        y -= 20

    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="donations_report.pdf", mimetype="application/pdf")

@app.route('/hospital_login', methods=['GET', 'POST'])
def hospital_login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']
        hospital_name = request.form['hospital_name']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password_input):
          if user.role == 'hospital' and user.hospital_name == hospital_name:
            session['user_id'] = user.id
            session['user_type'] = 'hospital'
            session['hospital_name'] = user.hospital_name
            return redirect('/hospital/status')
        else:
            flash('Invalid username or password.')

    return render_template('hospital_login.html')

@app.route('/hospital/request_blood', methods=['GET', 'POST'])
@login_required('hospital')
def hospital_request():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        blood_group = request.form['blood_group']
        units_required = request.form['units_required']
        hospital_name = request.form['hospital_name']
        contact = request.form['contact'] 

        recipient = Recipient(
            name=name,
            age=age,
            email=email,
            blood_group=blood_group,
            units_required=units_required,
            hospital_name=hospital_name,
            contact=contact
        )
        db.session.add(recipient)
        db.session.commit()
        return redirect('/hospital/status')
    return render_template('hospital/request_blood.html')

@app.route('/hospital/status', methods=['GET', 'POST'])
@login_required('hospital')
def request_status():
    requests_list = []
    if request.method == 'POST':
        hospital_name = request.form['hospital_name']
        requests_list = Recipient.query.filter_by(hospital_name=hospital_name).all()
    return render_template('hospital/status.html', requests=requests_list)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
def logout():
    logout_user()  
    session.clear()  
    return redirect('/')

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get("query")

    gemini_payload = {
        "contents": [{"parts": [{"text": user_input}]}]
    }

    try:
        gemini_response = requests.post(GEMINI_API_URL, json=gemini_payload)
        gemini_data = gemini_response.json()

        print("Gemini API response:", gemini_data) 

        parsed_text = (
            gemini_data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        if parsed_text is None or parsed_text.strip() == "":
            parsed_text = "I'm here to help! Try asking about blood donors, inventory, or donations."
    except Exception as e:
        print("Gemini parse error:", e)
        return jsonify({"response": "Sorry, I couldn't understand your request."})

    try:
        if "available" in user_input and "blood group" in user_input:
            blood_group = extract_blood_group(user_input)
            inventory = Inventory.query.filter_by(blood_group=blood_group).first()
            units = inventory.units_available if inventory else 0
            return jsonify({"response": f"{units} units of {blood_group} are available."})

        elif "donor" in user_input and "exist" in user_input:
            blood_group = extract_blood_group(user_input)
            donor_exists = Donor.query.filter_by(blood_group=blood_group).first() is not None
            return jsonify({"response": f"Yes, a donor with blood group {blood_group} exists." if donor_exists else f"No donors found for {blood_group}."})

        elif "total donations" in user_input or "how many donations" in user_input:
            total = Donation.query.count()
            return jsonify({"response": f"Total donations so far: {total}."})

        elif "inventory" in user_input:
            all_inventory = Inventory.query.all()
            response = "\n".join([f"{inv.blood_group}: {inv.units_available} units" for inv in all_inventory])
            return jsonify({"response": f"Inventory status:\n{response}"})

        elif "donation data" in user_input or "donation summary" in user_input:
            donations = Donation.query.order_by(Donation.date.desc()).limit(5).all()
            if not donations:
                return jsonify({"response": "No donation data available."})
            summary = "\n".join([f"{d.recipient_name} - {d.blood_group} - {d.unit_donated} units on {d.date.strftime('%Y-%m-%d')}" for d in donations])
            return jsonify({"response": f"Recent donations:\n{summary}"})

        else:
            return jsonify({"response": parsed_text})

    except Exception as e:
        print("Custom rule error:", e)
        return jsonify({"response": f"Something went wrong while processing your request."})



def extract_blood_group(text):
    groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    for g in groups:
        if g in text.upper():
            return g
    return 'O+'  

if __name__ == '__main__':
    app.run(debug=True)
