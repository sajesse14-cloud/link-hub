from flask import Flask, render_template

app = Flask(__name__)

my_info = {
    "name": "Jesse Kuykendall",
    "bio": "Below you'll find common websites",
    "links": [
        {"label": "Jira", "url": "https://healthlinkdimensions.atlassian.net/jira/dashboards/10724"},
        {"label": "Trigger Email", "url": "https://triggeremail.hldapps.com/dashboard"},
        {"label": "Ongage", "url": "https://app.ongage.com/"},
    ]
}

@app.route('/')
def home():
    return render_template('home.html', info=my_info)

from flask import Flask, render_template, request, jsonify

@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    name = data['name']
    email = data['email']
    message = data['message']

    # Print to terminal for now
    print(f"New message from {name} ({email}): {message}")

    return jsonify({"message": f"Thanks {name}, I'll be in touch!"})

if __name__ == '__main__':
    app.run(debug=True)