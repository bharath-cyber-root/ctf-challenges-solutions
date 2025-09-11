# Simple Login - Web CTF Challenge Writeup

## Challenge Information
- **Category:** Web
- **Difficulty:** Beginner
- **Points:** 100
- **Platform:** Custom CTF Challenge

## Challenge Description
A basic web authentication challenge perfect for beginners learning web security fundamentals. The objective is to find a way to authenticate and retrieve the flag from this simple login system.

## Initial Setup
1. Run the Flask application: `python app.py`
2. Navigate to `http://localhost:5000`
3. Try to gain access to the protected area

## Enumeration Approach

### 1. Initial Reconnaissance
- Accessed the web application at `http://localhost:5000`
- Found a simple login form with username and password fields
- Observed a hint on the page: "💡 Hint: Try common default credentials..."

### 2. Source Code Analysis
- The application provides an optional `/source` endpoint for educational purposes
- Reviewed the Flask application code in `app.py`
- Identified hardcoded credentials in the source code

### 3. Application Structure Analysis
- **Login endpoint (`/`):** Handles GET and POST requests for authentication
- **Success endpoint (`/success`):** Protected area that displays the flag upon successful login
- **Logout endpoint (`/logout`):** Clears the session
- **Source endpoint (`/source`):** Optional endpoint to view source code

## Vulnerability Identification

### Primary Vulnerability: Hardcoded Credentials
The main vulnerability is the presence of hardcoded credentials directly in the application source code:

```python
# Hardcoded credentials (intentionally weak for CTF purposes)
VALID_USERNAME = 'admin'
VALID_PASSWORD = 'password123'
FLAG = 'flag{basic_web_ctf_success}'
```

### Security Issues Identified:
1. **Weak Credential Management:** Credentials are hardcoded in the application
2. **Predictable Credentials:** Uses common default username/password combination
3. **Source Code Exposure:** Optional endpoint reveals sensitive information
4. **Insecure Session Management:** Uses a hardcoded secret key

## Exploitation Steps

### Method 1: Common Credential Testing
1. Navigate to `http://localhost:5000`
2. Try common default credentials:
   - Username: `admin`
   - Password: `password123`
3. Submit the login form
4. Successfully authenticate and access the protected area

### Method 2: Source Code Review
1. Access the `/source` endpoint (if available)
2. Review the application source code
3. Identify the hardcoded credentials:
   - `VALID_USERNAME = 'admin'`
   - `VALID_PASSWORD = 'password123'`
4. Use the discovered credentials to login

## Solution

### Credentials Found:
- **Username:** `admin`
- **Password:** `password123`

### Steps to Retrieve Flag:
1. Open the application in a web browser
2. Enter the credentials:
   - Username: `admin`
   - Password: `password123`
3. Click the "Login" button
4. Successfully access the protected area
5. The flag is displayed on the success page

## Flag Obtained
```
flag{basic_web_ctf_success}
```

## Key Learning Points

### 1. Credential Security
- Never hardcode credentials in application source code
- Use environment variables or secure configuration management
- Implement proper credential complexity requirements

### 2. Authentication Best Practices
- Avoid using default or predictable credentials
- Implement account lockout mechanisms to prevent brute force attacks
- Use secure session management with randomly generated secret keys

### 3. Source Code Protection
- Never expose application source code in production environments
- Implement proper access controls for sensitive endpoints
- Use proper deployment practices to protect sensitive information

### 4. Web Application Security Testing
- Always test for common default credentials
- Review application source code when available
- Understand the importance of proper credential management

## Recommendations

For a production environment, the following improvements should be implemented:

1. **Secure Credential Storage:**
   ```python
   import os
   VALID_USERNAME = os.environ.get('APP_USERNAME')
   VALID_PASSWORD = os.environ.get('APP_PASSWORD')
   ```

2. **Strong Session Management:**
   ```python
   import secrets
   app.secret_key = secrets.token_hex(32)
   ```

3. **Input Validation and Rate Limiting:**
   - Implement proper input validation
   - Add rate limiting to prevent brute force attacks
   - Use CSRF protection for forms

4. **Remove Debug Endpoints:**
   - Remove or properly secure the `/source` endpoint
   - Disable debug mode in production

## Conclusion

This challenge effectively demonstrates the importance of secure credential management in web applications. The vulnerability was easily exploitable due to the use of hardcoded, predictable credentials. This serves as an excellent introduction to web application security testing and highlights fundamental security principles that should be followed in real-world applications.

The Simple Login challenge provides a solid foundation for understanding:
- Basic web authentication mechanisms
- The dangers of hardcoded credentials
- Simple enumeration and exploitation techniques
- Essential web application security best practices
