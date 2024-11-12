from flask import Flask, render_template
import pymysql.cursors
import sys

app = Flask(__name__)

db_config = {
    "host": "localhost",          # MySQL host
    "user": "root",               # Your MySQL username
    "password": "stations",       # Your MySQL password
    "database": "flask_db",       # Your MySQL database name
}

def get_db_connection():
    """Create and return a new MySQL connection."""
    try:
        connection = pymysql.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"],
            cursorclass=pymysql.cursors.DictCursor  # To return results as dictionaries
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        sys.exit(1)

def fetch_users():
    """Fetch all users from the 'users' table."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Query to select all users from the table
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        return users
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        connection.close()

@app.route('/')
def index():
    """Handle the root URL and display users."""
    users = fetch_users()  # Fetch the users from the database
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
