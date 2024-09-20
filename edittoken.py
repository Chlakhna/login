
from flask import Flask, request, session, redirect, url_for, render_template
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'b1dcf804bcada8cdf9300f13fc3e7d7e'  # Required for session management

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dpateleg'

mysql = MySQL(app)

@app.route('/')
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    message = ''  # Initialize message to avoid UnboundLocalError

    if request.method == 'POST':
        # Get form data
        new_token = request.form.get('new_token')  # New token value
        new_groupid = request.form.get('new_groupid')  # New groupid value

        # Validate that we have the new values
        if new_token or new_groupid:  # Ensure we have at least one new value to update
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Update the first record (you can modify this to suit your actual logic for selecting the record)
            update_query = "UPDATE telegbot SET "
            params = []

            if new_token:
                update_query += "token = %s, "
                params.append(new_token)

            if new_groupid:
                update_query += "groupid = %s, "
                params.append(new_groupid)

            # Remove the last comma
            update_query = update_query.rstrip(', ')  # Trim the trailing comma

            # Example where we assume updating the first record, or you can add logic to identify the record differently
            update_query += " LIMIT 1"  # For simplicity, you may adjust this to match the specific user or record

            # Execute the update query
            cursor.execute(update_query, tuple(params))
            mysql.connection.commit()

            message = 'Information updated successfully!'
            return redirect(url_for('edit'))  # Redirect after successful update
        else:
            message = 'Please provide at least one new value to update.'

    return render_template('settings.html', message=message)


if __name__ == "__main__":
    app.run()
