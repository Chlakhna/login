from flask import Flask, request, session, redirect, url_for, render_template
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)
app.secret_key = 'b1dcf804bcada8cdf9300f13fc3e7d7e'  # Required for session management

# # MySQL configurations
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'dpa'

# Configure MySQL using environment variables
# app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
# app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
# app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
# app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
# app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))      
app.config.from_prefixed_env() 
mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
# def login():
#     mesage = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM Users WHERE username = % s AND password = % s', (username, password, ))
#         user = cursor.fetchone()
#         if user:
#
#             session['loggedin'] = True
#             session['userid'] = user['id']  # Using 'id' as per your table structure
#             session['username'] = user['username']
#             session['phone'] = user['phone']
#             session['role'] = user['role']
#             session['userlevel'] = user['userlevel']
#             mesage = 'Logged in successfully!'
#             return redirect(url_for('register'))
#             # return render_template('login.html', mesage = mesage)
#         else:
#             mesage = 'Please enter correct username / password !'
#     return render_template('login.html', mesage = mesage)

def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # Query to check for username and password in the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        if user:
            # If user exists, store information in the session
            session['loggedin'] = True
            session['userid'] = user['id']
            session['username'] = user['username']
            session['phone'] = user['phone']
            session['role'] = user['role']
            session['userlevel'] = user['userlevel']
            message = 'Logged in successfully!'
            return redirect(url_for('register'))  # Redirect to the user profile or other page
        else:
            message = 'Incorrect username or password. Please try again.'

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        role = request.form['role']  # User must provide a role
        userlevel = request.form.get('userlevel', 'user')  # Default to 'user'

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Check if the username already exists
        cursor.execute('SELECT * FROM Users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            mesage = 'Account already exists!'
        elif not phone or not password or not username or not role:
            mesage = 'Please fill out the form!'
        else:
            # Insert the new user into the Users table
            cursor.execute('INSERT INTO Users (username, password, phone, role, userlevel) VALUES (%s, %s, %s, %s, %s)',
                           (username, password, phone, role, userlevel))
            mysql.connection.commit()
            mesage = 'You have successfully registered!'
            return redirect(url_for('login'))  # Redirect to login after successful registration

        cursor.close()

    return render_template('index.html', mesage=mesage)





if __name__ == "__main__":
    app.run()
