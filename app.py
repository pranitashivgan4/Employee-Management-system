from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

# -----------------------------
# Create Flask App
# -----------------------------
app = Flask(__name__)
CORS(app)

# -----------------------------
# Helper: Create DB Connection
# -----------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # update if your MySQL has a password
        database="employee_db"
    )

# -----------------------------
# Bootstrap: Ensure tables
# -----------------------------
def ensure_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    # Employees (assumed existing)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            phone VARCHAR(50),
            position VARCHAR(100),
            salary DECIMAL(12,2),
            join_date DATE
        )
    """)

    # Departments (aligning with your usage of dept_id, dept_name, manager)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            dept_id INT AUTO_INCREMENT PRIMARY KEY,
            dept_name VARCHAR(255) NOT NULL,
            manager VARCHAR(255)
        )
    """)

    # Attendance: stores employee_id (FK), name, date, status
    # Unique constraint on (employee_id, date) so one record per day
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            employee_id INT NOT NULL,
            name VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            status ENUM('Present','Absent') NOT NULL,
            PRIMARY KEY (employee_id, date),
            CONSTRAINT fk_attendance_employee
                FOREIGN KEY (employee_id) REFERENCES employees(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

ensure_tables()

# -----------------------------
# Employee Routes
# -----------------------------
@app.route("/add_employee", methods=["POST"])
def add_employee():
    data = request.json
    sql = """
        INSERT INTO employees
        (name, email, phone, position, salary, join_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        data.get("name"),
        data.get("email"),
        data.get("phone"),
        data.get("position"),
        data.get("salary"),
        data.get("join_date")
    )
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Employee added successfully!"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400

@app.route("/employees", methods=["GET"])
def get_employees():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "phone": r[3],
            "position": r[4],
            "salary": float(r[5]) if r[5] is not None else None,
            "join_date": str(r[6]) if r[6] is not None else None
        })
    return jsonify(result)

@app.route("/delete_employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Employee deleted successfully!"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400

@app.route("/update_employee/<int:id>", methods=["PUT"])
def update_employee(id):
    data = request.json
    sql = """
        UPDATE employees
        SET name=%s, email=%s, phone=%s, position=%s, salary=%s, join_date=%s
        WHERE id=%s
    """
    values = (
        data["name"], data["email"], data["phone"],
        data["position"], data["salary"], data["join_date"], id
    )
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Employee updated successfully!"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400

# -----------------------------
# Dashboard Routes (Counts Only)
# -----------------------------
@app.route("/dashboard/summary", methods=["GET"])
def dashboard_summary():
    """Return key metrics: total employees, total departments, average salary"""
    conn = get_db_connection()
    cur = conn.cursor()

    # Total employees
    cur.execute("SELECT COUNT(*) FROM employees")
    total_employees = cur.fetchone()[0]

    # Total departments
    cur.execute("SELECT COUNT(*) FROM departments")
    total_departments = cur.fetchone()[0]

    # Average salary
    cur.execute("SELECT AVG(salary) FROM employees")
    avg_salary = cur.fetchone()[0] or 0

    cur.close()
    conn.close()

    return jsonify({
        "total_employees": total_employees,
        "total_departments": total_departments,
        "avg_salary": round(float(avg_salary), 2)
    })

# -----------------------------
# Department Routes
# -----------------------------
@app.route("/departments", methods=["GET"])
def get_departments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM departments")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    departments = [{"dept_id": r[0], "dept_name": r[1], "manager": r[2]} for r in rows]
    return jsonify(departments)

@app.route("/departments", methods=["POST"])
def add_department():
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO departments (dept_name, manager) VALUES (%s, %s)",
            (data['dept_name'], data['manager'])
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Department added successfully"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400

@app.route("/departments/<int:id>", methods=["PUT"])
def update_department(id):
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE departments SET dept_name=%s, manager=%s WHERE dept_id=%s",
            (data['dept_name'], data['manager'], id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Department updated successfully"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400

@app.route("/departments/<int:id>", methods=["DELETE"])
def delete_department(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM departments WHERE dept_id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Department deleted successfully"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400

# -----------------------------
# Attendance Routes
# -----------------------------
@app.route("/attendance", methods=["POST"])
def submit_attendance():
    """
    Accepts a JSON array of records:
    [{ "employee_id": 1, "name": "Pranita Shivgan", "date": "2025-11-30", "status": "Present" }, ...]
    Upserts by (employee_id, date).
    """
    data = request.get_json(force=True)
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of attendance records"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
            INSERT INTO attendance (employee_id, name, date, status)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE name=VALUES(name), status=VALUES(status)
        """
        for record in data:
            cur.execute(sql, (
                int(record["employee_id"]),
                record["name"],
                record["date"],
                record["status"]
            ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Attendance saved successfully!"})
    except (mysql.connector.Error, KeyError, ValueError) as err:
        return jsonify({"error": str(err)}), 400

@app.route("/attendance/<date>", methods=["GET"])
def view_attendance(date):
    """
    Returns { present: [{id, name}], absent: [{id, name}] } for given date
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT employee_id, name, status FROM attendance WHERE date=%s", (date,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    present = [{"id": r[0], "name": r[1]} for r in rows if r[2] == "Present"]
    absent = [{"id": r[0], "name": r[1]} for r in rows if r[2] == "Absent"]

    return jsonify({"present": present, "absent": absent})

# -----------------------------
# Run Flask App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)