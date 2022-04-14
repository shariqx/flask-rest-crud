#!/usr/bin/python
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS


def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn


def create_db_table():
    try:
        conn = connect_to_db()
        #conn.execute('''DROP TABLE student''')
        conn.execute('''
            CREATE TABLE student (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                dob TEXT NOT NULL,
                amount_due TEXT NOT NULL
            );
        ''')

        conn.commit()
        print("Student table created successfully")
    except:
        print("Student table creation failed..")
    finally:
        conn.close()


def insert_student(student):
    inserted_student = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO student (first_name, last_name, dob, amount_due) VALUES (?, ?, ?, ?)",
                    (student['first_name'], student['last_name'], student['dob'], student['amount_due']))
        conn.commit()
        inserted_student = get_student_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_student


def get_students():
    students = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            student = dict()
            student["student_id"] = i["student_id"]
            student["first_name"] = i["first_name"]
            student["last_name"] = i["last_name"]
            student["dob"] = i["dob"]
            student["amount_due"] = i["amount_due"]
            students.append(student)

    except:
        students = []

    return students


def get_student_by_id(student_id):
    student = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE student_id = ?", (student_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        student["student_id"] = row["student_id"]
        student["first_name"] = row["first_name"]
        student["last_name"] = row["last_name"]
        student["dob"] = row["dob"]
        student["amount_due"] = row["amount_due"]
    except:
        student = {}

    return student


def update_student(student):
    updated_student = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE student SET first_name = ?, last_name = ?, dob = ?, amount_due = ? WHERE student_id =?", (student["first_name"], student["last_name"], student["dob"], student["amount_due"], student["student_id"],))
        conn.commit()

        updated_student = get_student_by_id(student["student_id"])

    except:
        conn.rollback()
        updated_student = {}
    finally:
        conn.close()

    return updated_student


def delete_student(student_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from student WHERE student_id = ?", (student_id))
        conn.commit()
        message["status"] = "Student deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete student"
    finally:
        conn.close()

    return message


students = []
student0 = {
    "dob": "17-03-1993",
    "last_name": "Bakshi",
    "first_name": "Krishna",
    "amount_due": "110$"
}

student1 = {
    "dob": "30-05-1994",
    "last_name": "Shaikh",
    "first_name": "Shariq",
    "amount_due": "60$"
}

students.append(student0)
students.append(student1)

create_db_table()

for i in students:
    print(insert_student(i))




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/students', methods=['GET'])
def api_get_students():
    return jsonify(get_students())

@app.route('/api/students/<student_id>', methods=['GET'])
def api_get_student(student_id):
    return jsonify(get_student_by_id(student_id))

@app.route('/api/students/add',  methods = ['POST'])
def api_add_student():
    student = request.get_json()
    return jsonify(insert_student(student))

@app.route('/api/students/update',  methods = ['PUT'])
def api_update_student():
    student = request.get_json()
    return jsonify(update_student(student))

@app.route('/api/students/delete/<student_id>',  methods = ['DELETE'])
def api_delete_student(student_id):
    return jsonify(delete_student(student_id))


if __name__ == "__main__":
    app.run()