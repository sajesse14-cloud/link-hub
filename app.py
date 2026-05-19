from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your-super-secret-key-change-this'

# Your credentials
USERNAME = 'jesse'
PASSWORD = generate_password_hash('password123')

# Your personal info
my_info = {
    "name": "Jesse Kuykendall",
    "bio": "A short sentence about yourself",
    "links": [
        {"label": "GitHub", "url": "https://github.com"},
        {"label": "LinkedIn", "url": "https://linkedin.com"},
        {"label": "Portfolio", "url": "https://yoursite.com"},
    ]
}

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html', info=my_info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        if data['username'] == USERNAME and check_password_hash(PASSWORD, data['password']):
            session['logged_in'] = True
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
    name = data['name']
    email = data['email']
    message = data['message']
    print(f"New message from {name} ({email}): {message}")
    return jsonify({"message": f"Thanks {name}, I'll be in touch!"})

if __name__ == '__main__':
    app.run(debug=True)