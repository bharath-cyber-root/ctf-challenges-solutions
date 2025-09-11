#!/usr/bin/env python3
"""
Simple Login - Web CTF Challenge
A basic Flask application with hardcoded credentials for educational purposes.

Objective: Find the correct username and password to retrieve the flag.
Credentials: admin / password123
"""

from flask import Flask, request, render_template_string, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_ctf'  # In production, use a secure random key

# Hardcoded credentials (intentionally weak for CTF purposes)
VALID_USERNAME = 'admin'
VALID_PASSWORD = 'password123'
FLAG = 'flag{basic_web_ctf_success}'

# Simple HTML templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple Login Challenge</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f0f0f0; }
        .container { max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #333; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        .submit-btn { width: 100%; padding: 12px; background-color: #007bff; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
        .submit-btn:hover { background-color: #0056b3; }
        .error { color: red; text-align: center; margin-top: 10px; }
        .hint { font-size: 12px; color: #666; text-align: center; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🔐 Simple Login Challenge</h1>
        <p style="text-align: center; color: #666;">Find the correct credentials to access the flag!</p>
        
        <form method="POST">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="submit-btn">Login</button>
        </form>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <div class="hint">
            💡 Hint: Try common default credentials...
        </div>
    </div>
</body>
</html>
'''

SUCCESS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login Successful!</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f0f0f0; }
        .container { max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
        .success { color: #28a745; font-size: 24px; margin-bottom: 20px; }
        .flag { background-color: #f8f9fa; border: 2px solid #28a745; border-radius: 5px; padding: 20px; font-family: monospace; font-size: 18px; margin: 20px 0; }
        .logout-btn { padding: 10px 20px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
        .logout-btn:hover { background-color: #c82333; text-decoration: none; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="success">🎉 Login Successful!</h1>
        <p>Congratulations! You've successfully authenticated.</p>
        
        <div class="flag">
            <strong>Your Flag:</strong><br>
            {{ flag }}
        </div>
        
        <p>Well done! You've completed this basic web authentication challenge.</p>
        
        <a href="{{ url_for('logout') }}" class="logout-btn">Logout</a>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Check credentials
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('success'))
        else:
            error = '❌ Invalid username or password. Try again!'
    
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/success')
def success():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template_string(SUCCESS_TEMPLATE, flag=FLAG)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/source')
def source():
    """Optional endpoint to view source code (for educational purposes)"""
    return f'''<pre>{open(__file__, 'r').read()}</pre>'''

if __name__ == '__main__':
    # For development only - use a proper WSGI server in production
    app.run(host='0.0.0.0', port=5000, debug=True)
