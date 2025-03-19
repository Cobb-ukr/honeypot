from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from password_generator import add_user
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Ensure directories exist
for directory in ['logs', 'pictures']:
    os.makedirs(directory, exist_ok=True)

# Initialize data.json if it doesn't exist
if not os.path.exists('data.json'):
    with open('data.json', 'w') as f:
        json.dump({}, f)

@app.route('/')
def index():
    # Reset login attempts when visiting the login page
    if 'login_attempts' not in session:
        session['login_attempts'] = 0
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Check credentials
    with open('data.json', 'r') as f:
        data = json.load(f)
    
    if username in data and data[username] == password:
        # Successful login
        session['login_attempts'] = 0
        return redirect(url_for('success'))
    else:
        # Failed login
        session['login_attempts'] = session.get('login_attempts', 0) + 1
        
        if session['login_attempts'] >= 3:
            # Run logger.py after 3 failed attempts
            subprocess.run(['python', 'logger.py'])
            session['login_attempts'] = 0
            
        return redirect(url_for('index'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            password = add_user(username)
            return f"User registered! Your password is: {password}"
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)