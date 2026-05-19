"""
Hotel Reservation & Room Booking System
Flask Backend — Group 01 (Absar 22P-9068 | Hina Rashid 22P-9198)

Requirements:
    pip install flask flask-cors mysql-connector-python pyjwt werkzeug python-dotenv

Run:
    python3 app.py
    Then open http://localhost:5000 in your browser.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import mysql.connector
import os

# ─── APP SETUP ────────────────────────────────────────────────
app = Flask(__name__, static_folder=".")
CORS(app)

# ─── DATABASE CONNECTION ───────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",        
    "password": "123456",      # Updated MySQL Password
    "database": "hotel",
    "autocommit": True
}

def get_db():
    """Return a fresh MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)

def query(sql, params=(), fetchone=False, commit=False):
    """
    Execute a SQL query.
    - For SELECT: returns list of dicts (or one dict if fetchone=True).
    - For INSERT/UPDATE/DELETE: returns lastrowid.
    """
    conn = get_db()
    cur  = conn.cursor(dictionary=True)
    cur.execute(sql, params)
    if commit:
        conn.commit()
        result = cur.lastrowid
    elif fetchone:
        result = cur.fetchone()
    else:
        result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# ─── APIS ─────────────────────────────────────────────────────

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    # Simple check for testing/roles
    if username == "admin@abhistay.com" or username == "admin":
        return jsonify({"role": "admin", "name": "Admin Absar", "token": "dummy-token-admin"})
    elif username == "reception":
        return jsonify({"role": "reception", "name": "Reception Desk", "token": "dummy-token-reception"})
    
    # Guest check from MySQL database
    sql = "SELECT * FROM Customers WHERE Email_Address = %s OR First_Name = %s"
    customer = query(sql, (username, username), fetchone=True)
    
    if customer:
        return jsonify({
            "role": "guest",
            "name": f"{customer['First_Name']} {customer['Last_Name']}",
            "token": "dummy-token-guest"
        })
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name", "").split(" ", 1)
    first_name = name[0]
    last_name = name[1] if len(name) > 1 else ""
    email = data.get("email")
    phone = data.get("phone")
    
    # Find next available Customer ID
    next_id_res = query("SELECT MAX(Customer_ID) AS max_id FROM Customers", fetchone=True)
    next_id = (next_id_res["max_id"] or 0) + 1
    
    sql = """
        INSERT INTO Customers (Customer_ID, First_Name, Last_Name, Email_Address, Phone_Number)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        query(sql, (next_id, first_name, last_name, email, phone), commit=True)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/hotels", methods=["GET"])
def get_hotels():
    sql = """
        SELECT h.*, hc.Hotel_Chain_Name, COUNT(r.Room_ID) AS Room_Count 
        FROM Hotels h
        LEFT JOIN Hotel_Chains hc ON h.Hotel_Chain_Code = hc.Hotel_Chain_Code
        LEFT JOIN Rooms r ON h.Hotel_ID = r.Hotel_ID
        GROUP BY h.Hotel_ID
    """
    return jsonify(query(sql))

@app.route("/api/rooms", methods=["GET"])
def get_rooms():
    sql = """
        SELECT r.*, h.Hotel_Name, rt.Description AS Room_Type, rt.Standard_Rate
        FROM Rooms r
        JOIN Hotels h ON r.Hotel_ID = h.Hotel_ID
        JOIN Room_Types rt ON r.Room_Type_Code = rt.Room_Type_Code
    """
    return jsonify(query(sql))

@app.route("/api/rooms/search", methods=["GET"])
def search_rooms():
    hotel_id = request.args.get("hotel_id")
    sql = """
        SELECT r.*, h.Hotel_Name, rt.Description AS Room_Type, rt.Standard_Rate
        FROM Rooms r
        JOIN Hotels h ON r.Hotel_ID = h.Hotel_ID
        JOIN Room_Types rt ON r.Room_Type_Code = rt.Room_Type_Code
    """
    if hotel_id:
        sql += f" WHERE r.Hotel_ID = {int(hotel_id)}"
    return jsonify(query(sql))

@app.route("/api/bookings", methods=["GET"])
def get_bookings():
    sql = """
        SELECT b.*, h.Hotel_Name, r.Room_Number, 
               CONCAT(c.First_Name, ' ', c.Last_Name) AS Guest_Name,
               bs.Description AS Status,
               ROUND(rt.Standard_Rate * DATEDIFF(b.Date_To, b.Date_From) * 1.1, 2) AS Total_Amount
        FROM Bookings b
        JOIN Customers c ON b.Customer_ID = c.Customer_ID
        JOIN Rooms r ON b.Room_ID = r.Room_ID
        JOIN Hotels h ON r.Hotel_ID = h.Hotel_ID
        JOIN Room_Types rt ON r.Room_Type_Code = rt.Room_Type_Code
        JOIN Booking_Status bs ON b.Booking_Status_Code = bs.Booking_Status_Code
    """
    return jsonify(query(sql))

@app.route("/api/bookings/my-history", methods=["GET"])
def my_bookings():
    # Fixed to Customer ID 1 for demonstration
    sql = """
        SELECT b.*, h.Hotel_Name, r.Room_Number, bs.Description AS Status,
               ROUND(rt.Standard_Rate * DATEDIFF(b.Date_To, b.Date_From) * 1.1, 2) AS Total_Amount
        FROM Bookings b
        JOIN Rooms r ON b.Room_ID = r.Room_ID
        JOIN Hotels h ON r.Hotel_ID = h.Hotel_ID
        JOIN Room_Types rt ON r.Room_Type_Code = rt.Room_Type_Code
        JOIN Booking_Status bs ON b.Booking_Status_Code = bs.Booking_Status_Code
        WHERE b.Customer_ID = 1
    """
    return jsonify(query(sql))

@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.json
    room_id = data.get("room_id")
    date_from = data.get("date_from")
    date_to = data.get("date_to")
    
    next_id_res = query("SELECT MAX(Booking_ID) AS max_id FROM Bookings", fetchone=True)
    next_id = (next_id_res["max_id"] or 0) + 1
    
    sql = """
        INSERT INTO Bookings (Booking_ID, Customer_ID, Room_ID, Booking_Status_Code, Date_From, Date_To)
        VALUES (%s, 1, %s, 'C', %s, %s)
    """
    try:
        query(sql, (next_id, room_id, date_from, date_to), commit=True)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/bookings/<int:id>/cancel", methods=["POST"])
def cancel_booking(id):
    sql = "UPDATE Bookings SET Booking_Status_Code = 'X' WHERE Booking_ID = %s"
    query(sql, (id,), commit=True)
    return jsonify({"success": True})

@app.route("/api/reception/desk", methods=["GET"])
def reception_desk():
    sql = """
        SELECT b.Booking_ID, CONCAT(c.First_Name, ' ', c.Last_Name) AS Guest_Name,
               r.Room_Number, rt.Description AS Room_Type, b.Date_From, bs.Description AS Status
        FROM Bookings b
        JOIN Customers c ON b.Customer_ID = c.Customer_ID
        JOIN Rooms r ON b.Room_ID = r.Room_ID
        JOIN Room_Types rt ON r.Room_Type_Code = rt.Room_Type_Code
        JOIN Booking_Status bs ON b.Booking_Status_Code = bs.Booking_Status_Code
        WHERE bs.Description IN ('Confirmed', 'Checked-In')
    """
    return jsonify(query(sql))

@app.route("/api/reception/booking/<int:id>/checkin", methods=["POST"])
def checkin_guest(id):
    query("UPDATE Bookings SET Booking_Status_Code = 'I' WHERE Booking_ID = %s", (id,), commit=True)
    return jsonify({"success": True})

@app.route("/api/reception/booking/<int:id>/checkout", methods=["POST"])
def checkout_guest(id):
    query("UPDATE Bookings SET Booking_Status_Code = 'O' WHERE Booking_ID = %s", (id,), commit=True)
    return jsonify({"success": True})

@app.route("/api/customers", methods=["GET"])
def get_customers():
    sql = """
        SELECT c.*, ci.City_Name, co.Country_Name, COUNT(b.Booking_ID) AS Booking_Count
        FROM Customers c
        LEFT JOIN City ci ON c.City_Code = ci.City_Code
        LEFT JOIN Country co ON ci.Country_Code = co.Country_Code
        LEFT JOIN Bookings b ON c.Customer_ID = b.Customer_ID
        GROUP BY c.Customer_ID
    """
    return jsonify(query(sql))

@app.route("/api/reports/dashboard", methods=["GET"])
def report_dashboard():
    total_rev = query("""
        SELECT ROUND(SUM(rt.Standard_Rate * DATEDIFF(b.Date_To, b.Date_From) * 1.1), 2) AS rev
        FROM Bookings b
        JOIN Rooms r ON b.Room_ID = r.Room_ID
        JOIN Room_Types rt ON r.Room_Type_Code = rt.Room_Type_Code
        WHERE b.Booking_Status_Code != 'X'
    """, fetchone=True)
    
    total_bookings = query("SELECT COUNT(*) AS cnt FROM Bookings", fetchone=True)
    active_guests = query("SELECT COUNT(DISTINCT Customer_ID) AS cnt FROM Bookings WHERE Booking_Status_Code='I'", fetchone=True)
    
    return jsonify({
        "total_revenue": total_rev["rev"] or 0,
        "total_bookings": total_bookings["cnt"] or 0,
        "active_guests": active_guests["cnt"] or 0
    })

# ─── SERVE FRONTEND ───────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    print("=" * 55)
    print("  AbHi Stay — Secure Hotel Backend System Loading...")
    print("  Running on http://localhost:5000")
    print("=" * 55)
    app.run(host="0.0.0.0", port=5000, debug=True)