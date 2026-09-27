
from flask import Flask, render_template, request, redirect
from database import create_connection

app = Flask(__name__)


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ADD STUDENT ----------------

@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        dept = request.form["dept"]
        email = request.form["email"]

        connection = create_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO student_details (name, age, dept, email)
        VALUES (%s, %s, %s, %s)
        """

        values = (name, age, dept, email)

        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/")

    return render_template("add_student.html")


# ---------------- VIEW STUDENTS ----------------

@app.route("/students")
def view_students():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM student_details")

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("students.html", students=students)


# ---------------- UPDATE STUDENT ----------------

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):

    connection = create_connection()
    cursor = connection.cursor()

    # If form is submitted
    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        dept = request.form["dept"]
        email = request.form["email"]

        sql = """
        UPDATE student_details
        SET name = %s, age = %s, dept = %s, email = %s
        WHERE id = %s
        """

        values = (name, age, dept, email, id)

        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/students")

    # Get existing student details
    sql = "SELECT * FROM student_details WHERE id = %s"

    cursor.execute(sql, (id,))

    student = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("update.html", student=student)


# ---------------- DELETE STUDENT ----------------

@app.route("/delete/<int:id>")
def delete_student(id):

    connection = create_connection()
    cursor = connection.cursor()

    # Delete the student
    sql = "DELETE FROM student_details WHERE id = %s"
    cursor.execute(sql, (id,))

    connection.commit()

    # Check whether the table is empty
    cursor.execute("SELECT COUNT(*) FROM student_details")
    count = cursor.fetchone()[0]

    # Reset ID if there are no students
    if count == 0:
        cursor.execute("ALTER TABLE student_details AUTO_INCREMENT = 1")
        connection.commit()

    cursor.close()
    connection.close()

    return redirect("/students")


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)
