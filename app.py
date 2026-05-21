from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-super-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///linkhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─────────────────────────────────
# Database Tables
# ─────────────────────────────────

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# ─────────────────────────────────
# Your Personal Info
# ─────────────────────────────────

my_info = {
    "name": "Jesse Kuykendall",
    "bio": "A short sentence about yourself",
    "links": [
        {"label": "GitHub", "url": "https://github.com"},
        {"label": "LinkedIn", "url": "https://linkedin.com"},
        {"label": "Portfolio", "url": "https://yoursite.com"},
    ]
}

# ─────────────────────────────────
# Routes
# ─────────────────────────────────

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html', info=my_info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            session['logged_in'] = True
            session['username'] = user.username
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    
    # Save to database
    new_contact = Contact(
        name=data['name'],
        email=data['email'],
        message=data['message']
    )
    db.session.add(new_contact)
    db.session.commit()

    print(f"New message from {data['name']} ({data['email']}): {data['message']}")
    return jsonify({"message": f"Thanks {data['name']}, I'll be in touch!"})

@app.route('/messages')
def messages():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    all_messages = Contact.query.order_by(Contact.date.desc()).all()
    return render_template('messages.html', messages=all_messages)

# ─────────────────────────────────
# Initialize Database
# ─────────────────────────────────

def create_admin():
    with app.app_context():
        db.create_all()
        # Only create admin if no users exist yet
        if not User.query.first():
            admin = User(
                username='jesse',
                password=generate_password_hash('password123')
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")

create_admin()

if __name__ == '__main__':
    app.run(debug=True)