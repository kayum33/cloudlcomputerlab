import hashlib
import os
import mysql.connector
from google.cloud import sql

# Connect to the MySQL database
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")
db_connection = mysql.connector.connect(user=db_user, password=db_password, database=db_name)
cursor = db_connection.cursor()

# Create the users table
cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255))")

# Register a new user
def register_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password_hash))
    db_connection.commit()

# Validate a user login
def validate_login(username, password):
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    stored_password_hash = cursor.fetchone()[0]
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return stored_password_hash == password_hash
