import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="AnoraSharon@05",
        database="student_db"
    )