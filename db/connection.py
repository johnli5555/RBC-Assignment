import psycopg2
import os

# In a real-world setting the values here would not be hard-coded. They would be instead stored safely elsewhere or stored in env variables
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "clientdb"),
        user=os.getenv("DB_USER", "client_admin"),
        password=os.getenv("DB_PASSWORD", "secure_password")
    )