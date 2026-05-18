"""
Hotel Reservation & Room Booking System
Flask Backend — Group 01 (Absar 22P-9068 | Hina Rashid 22P-9198)

Requirements:
    pip install flask flask-cors mysql-connector-python

Run:
    python app.py
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


# ═══════════════════════════════════════════════════════════════
#  AUTH  & SIGNUP
# ═══════════════════════════════════════════════════════════════

@app.route("/api/login", methods=["POST"])
def login():
    data     = request.json
    username = data.get("username", "").strip().lower()
    password = data.get("password", "")           # demo: any password works
    
    if not username:
        return jsonify({"error": "Email is required"}), 400

    # 1. Admin aur Reception ki direct checking
    if username == "admin@abhistay.com":
        return jsonify({"role": "admin", "name": "System Admin"})
    elif username == "reception@abhistay.com":
        return jsonify({"role": "reception", "name": "Receptionist"})
    
    # 2. Guest Login - Database verification
    try:
        # Check if email exists in the Address column (where we saved it during signup)
        sql = "SELECT First_Name, Last_Name FROM Customers WHERE Address LIKE %s LIMIT 1"
        guest = query(sql, (f"%{username}%",), fetchone=True)
        
        if guest:
            full_name = f"{guest['First_Name']} {guest['Last_Name']}".strip()
            return jsonify({"role": "guest", "name": full_name})
        else:
            # Agar email database mein nahi hai toh error dega
            return jsonify({"error": "Invalid credentials. Account not found!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Signup Route to save new members to MySQL Database
@app.route("/api/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        full_name = data.get("name", "").strip().split(" ", 1)
        first_name = full_name[0]
        last_name = full_name[1] if len(full_name) > 1 else ""
        
        email = data.get("email", "")
        phone = data.get("phone", "")
        
        # Database mein Email/Phone column nahi hai, isliye Address field mein save kar rahe hain
        contact_info = f"Email: {email}, Phone: {phone}"
        
        sql = """INSERT INTO Customers (First_Name, Last_Name, Address) 
                 VALUES (%s, %s, %s)"""
        query(sql, (first_name, last_name, contact_info), commit=True)
        
        return jsonify({"success": True, "message": "Customer registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ═══════════════════════════════════════════════════════════════
#  COUNTRIES & CITIES
# ═══════════════════════════════════════════════════════════════

@app.route("/api/countries", methods=["GET"])
def get_countries():
    return jsonify(query("SELECT * FROM Country"))

@app.route("/api/cities", methods=["GET"])
def get_cities():
    country = request.args.get("country_code")
    if country:
        return jsonify(query("SELECT * FROM City WHERE Country_Code = %s", (country,)))
    return jsonify(query("SELECT * FROM City"))


# ═══════════════════════════════════════════════════════════════
#  HOTEL CHAINS
# ═══════════════════════════════════════════════════════════════

@app.route("/api/chains", methods=["GET"])
def get_chains():
    return jsonify(query("SELECT * FROM Hotel_Chains"))


# ═══════════════════════════════════════════════════════════════
#  HOTELS
# ═══════════════════════════════════════════════════════════════

@app.route("/api/hotels", methods=["GET"])
def get_hotels():
    sql = """
        SELECT h.Hotel_ID, h.Hotel_Name, h.Hotel_Address, h.Email_Address,
               h.Country_Code, h.Hotel_Chain_Code,
               c.Country_Name, hc.Hotel_Chain_Name,
               (SELECT COUNT(*) FROM Rooms r WHERE r.Hotel_ID = h.Hotel_ID) AS Room_Count
        FROM Hotels h
        LEFT JOIN Country c  ON c.Country_Code = h.Country_Code
        LEFT JOIN Hotel_Chains hc ON hc.Hotel_Chain_Code = h.Hotel_Chain_Code
    """
    return jsonify(query(sql))

@app.route("/api/hotels/<int:hotel_id>", methods=["GET"])
def get_hotel(hotel_id):
    sql = """
        SELECT h.*, c.Country_Name, hc.Hotel_Chain_Name
        FROM Hotels h
        LEFT JOIN Country c  ON c.Country_Code = h.Country_Code
        LEFT JOIN Hotel_Chains hc ON hc.Hotel_Chain_Code = h.Hotel_Chain_Code
        WHERE h.Hotel_ID = %s
    """
    return jsonify(query(sql, (hotel_id,), fetchone=True))

@app.route("/api/hotels", methods=["POST"])
def add_hotel():
    d = request.json
    sql = """INSERT INTO Hotels
             (Hotel_ID, Hotel_Name, Hotel_Address, Email_Address, Country_Code, Hotel_Chain_Code)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    lid = query(sql, (d["hotel_id"], d["hotel_name"], d["address"],
                      d["email"], d["country_code"], d["chain_code"]), commit=True)
    return jsonify({"success": True, "hotel_id": d["hotel_id"]}), 201

@app.route("/api/hotels/<int:hotel_id>/features", methods=["GET"])
def hotel_features(hotel_id):
    sql = """SELECT hf.Feature_Code, hf.Description
             FROM Specific_Hotel_Feature shf
             JOIN Hotel_Features hf ON hf.Feature_Code = shf.Feature_Code
             WHERE shf.Hotel_ID = %s"""
    return jsonify(query(sql, (hotel_id,)))


# ═══════════════════════════════════════════════════════════════
#  ROOM TYPES
# ═══════════════════════════════════════════════════════════════

@app.route("/api/room-types", methods=["GET"])
def get_room_types():
    return jsonify(query("SELECT * FROM Room_Types"))


# ═══════════════════════════════════════════════════════════════
#  ROOMS
# ═══════════════════════════════════════════════════════════════

@app.route("/api/rooms", methods=["GET"])
def get_rooms():
    hotel_id  = request.args.get("hotel_id")
    room_type = request.args.get("room_type")
    sql = """
        SELECT r.Room_ID, r.Room_Number, r.Room_Floor, r.Hotel_ID, r.Room_Type_Code,
               rt.Description AS Room_Type_Name, rt.Standard_Rate,
               h.Hotel_Name
        FROM Rooms r
        JOIN Room_Types rt ON rt.Room_Type_Code = r.Room_Type_Code
        JOIN Hotels h      ON h.Hotel_ID        = r.Hotel_ID
        WHERE 1=1
    """
    params = []
    if hotel_id:  sql += " AND r.Hotel_ID = %s";        params.append(hotel_id)
    if room_type: sql += " AND r.Room_Type_Code = %s";  params.append(room_type)
    return jsonify(query(sql, tuple(params)))

@app.route("/api/rooms/available", methods=["GET"])
def get_available_rooms():
    """
    Return rooms not booked between date_from and date_to.
    Query param: hotel_id (optional), date_from, date_to
    """
    date_from = request.args.get("date_from")
    date_to   = request.args.get("date_to")
    hotel_id  = request.args.get("hotel_id")

    if not date_from or not date_to:
        return jsonify({"error": "date_from and date_to required"}), 400

    sql = """
        SELECT r.Room_ID, r.Room_Number, r.Room_Floor, r.Hotel_ID,
               r.Room_Type_Code, rt.Description AS Room_Type_Name,
               rt.Standard_Rate, h.Hotel_Name
        FROM Rooms r
        JOIN Room_Types rt ON rt.Room_Type_Code = r.Room_Type_Code
        JOIN Hotels h      ON h.Hotel_ID        = r.Hotel_ID
        WHERE r.Room_ID NOT IN (
            SELECT b.Room_ID FROM Bookings b
            JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
            WHERE bs.Description NOT IN ('Cancelled', 'Checked-Out')
              AND NOT (b.Date_To <= %s OR b.Date_From >= %s)
        )
    """
    params = [date_from, date_to]
    if hotel_id:
        sql   += " AND r.Hotel_ID = %s"
        params.append(hotel_id)
    return jsonify(query(sql, tuple(params)))

@app.route("/api/rooms", methods=["POST"])
def add_room():
    d   = request.json
    sql = """INSERT INTO Rooms (Room_ID, Room_Number, Room_Floor, Hotel_ID, Room_Type_Code)
             VALUES (%s, %s, %s, %s, %s)"""
    query(sql, (d["room_id"], d["room_number"], d["floor"],
                d["hotel_id"], d["room_type_code"]), commit=True)
    return jsonify({"success": True}), 201

@app.route("/api/rooms/<int:room_id>/rate", methods=["GET"])
def get_room_rate(room_id):
    """Return daily rate: prefer Daily_Room_Rates table, fall back to Standard_Rate."""
    date = request.args.get("date")
    if date:
        row = query(
            "SELECT Daily_Room_Rate FROM Daily_Room_Rates WHERE Room_ID=%s AND Day_Date=%s",
            (room_id, date), fetchone=True
        )
        if row: return jsonify({"rate": float(row["Daily_Room_Rate"])})
    row = query(
        "SELECT rt.Standard_Rate FROM Rooms r JOIN Room_Types rt ON rt.Room_Type_Code=r.Room_Type_Code WHERE r.Room_ID=%s",
        (room_id,), fetchone=True
    )
    return jsonify({"rate": float(row["Standard_Rate"]) if row else 0})


# ═══════════════════════════════════════════════════════════════
#  ROOM AVAILABILITY
# ═══════════════════════════════════════════════════════════════

@app.route("/api/availability", methods=["GET"])
def get_availability():
    room_id = request.args.get("room_id")
    sql = "SELECT * FROM Room_Availability"
    params = []
    if room_id:
        sql += " WHERE Room_ID = %s"
        params.append(room_id)
    return jsonify(query(sql, tuple(params)))

@app.route("/api/availability", methods=["POST"])
def set_availability():
    d = request.json
    sql = """INSERT INTO Room_Availability (Room_ID, Day_Date, Status)
             VALUES (%s, %s, %s)
             ON DUPLICATE KEY UPDATE Status = VALUES(Status)"""
    query(sql, (d["room_id"], d["day_date"], d["status"]), commit=True)
    return jsonify({"success": True})


# ═══════════════════════════════════════════════════════════════
#  CUSTOMERS
# ═══════════════════════════════════════════════════════════════

@app.route("/api/customers", methods=["GET"])
def get_customers():
    search = request.args.get("search", "")
    sql    = """
        SELECT c.*, co.Country_Name, ci.City_Name,
               (SELECT COUNT(*) FROM Bookings b WHERE b.Customer_ID = c.Customer_ID) AS Booking_Count
        FROM Customers c
        LEFT JOIN Country co ON co.Country_Code = c.Country_Code
        LEFT JOIN City    ci ON ci.City_Code     = c.City_Code
    """
    params = []
    if search:
        sql   += " WHERE c.First_Name LIKE %s OR c.Last_Name LIKE %s"
        params += [f"%{search}%", f"%{search}%"]
    return jsonify(query(sql, tuple(params)))

@app.route("/api/customers/<int:cust_id>", methods=["GET"])
def get_customer(cust_id):
    sql = """SELECT c.*, co.Country_Name, ci.City_Name
             FROM Customers c
             LEFT JOIN Country co ON co.Country_Code = c.Country_Code
             LEFT JOIN City    ci ON ci.City_Code     = c.City_Code
             WHERE c.Customer_ID = %s"""
    return jsonify(query(sql, (cust_id,), fetchone=True))

@app.route("/api/customers", methods=["POST"])
def add_customer():
    d   = request.json
    sql = """INSERT INTO Customers
             (First_Name, Last_Name, Address, Age, Country_Code, City_Code)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    lid = query(sql, (d["first_name"], d["last_name"], d.get("address",""),
                      d.get("age"), d.get("country_code"), d.get("city_code")), commit=True)
    return jsonify({"success": True, "customer_id": lid}), 201

@app.route("/api/customers/<int:cust_id>", methods=["PUT"])
def update_customer(cust_id):
    d   = request.json
    sql = """UPDATE Customers SET First_Name=%s, Last_Name=%s, Address=%s,
             Age=%s, Country_Code=%s, City_Code=%s WHERE Customer_ID=%s"""
    query(sql, (d["first_name"], d["last_name"], d.get("address",""),
                d.get("age"), d.get("country_code"), d.get("city_code"), cust_id), commit=True)
    return jsonify({"success": True})


# ═══════════════════════════════════════════════════════════════
#  BOOKING STATUS
# ═══════════════════════════════════════════════════════════════

@app.route("/api/booking-statuses", methods=["GET"])
def get_booking_statuses():
    return jsonify(query("SELECT * FROM Booking_Status"))


# ═══════════════════════════════════════════════════════════════
#  BOOKINGS
# ═══════════════════════════════════════════════════════════════

@app.route("/api/bookings", methods=["GET"])
def get_bookings():
    customer_id = request.args.get("customer_id")
    status      = request.args.get("status")
    hotel_id    = request.args.get("hotel_id")

    sql = """
        SELECT b.Booking_ID, b.Date_From, b.Date_To, b.Booking_Status_Code,
               bs.Description AS Status_Name,
               b.Customer_ID,
               CONCAT(c.First_Name,' ',c.Last_Name) AS Customer_Name,
               b.Room_ID, r.Room_Number, r.Room_Floor,
               h.Hotel_ID, h.Hotel_Name,
               rt.Room_Type_Code, rt.Description AS Room_Type_Name,
               rt.Standard_Rate,
               DATEDIFF(b.Date_To, b.Date_From) AS Nights,
               ROUND(rt.Standard_Rate * DATEDIFF(b.Date_To, b.Date_From) * 1.1, 2) AS Total_Amount
        FROM Bookings b
        JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
        JOIN Customers c       ON c.Customer_ID          = b.Customer_ID
        JOIN Rooms r           ON r.Room_ID              = b.Room_ID
        JOIN Hotels h          ON h.Hotel_ID             = r.Hotel_ID
        JOIN Room_Types rt     ON rt.Room_Type_Code      = r.Room_Type_Code
        WHERE 1=1
    """
    params = []
    if customer_id:
        sql    += " AND b.Customer_ID = %s"; params.append(customer_id)
    if status:
        sql    += " AND bs.Description = %s"; params.append(status)
    if hotel_id:
        sql    += " AND h.Hotel_ID = %s"; params.append(hotel_id)
    sql += " ORDER BY b.Booking_ID DESC"
    return jsonify(query(sql, tuple(params)))

@app.route("/api/bookings/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    sql = """
        SELECT b.*, bs.Description AS Status_Name,
               CONCAT(c.First_Name,' ',c.Last_Name) AS Customer_Name,
               r.Room_Number, h.Hotel_Name, rt.Description AS Room_Type_Name,
               rt.Standard_Rate,
               DATEDIFF(b.Date_To, b.Date_From) AS Nights,
               ROUND(rt.Standard_Rate * DATEDIFF(b.Date_To, b.Date_From) * 1.1, 2) AS Total_Amount
        FROM Bookings b
        JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
        JOIN Customers c       ON c.Customer_ID          = b.Customer_ID
        JOIN Rooms r           ON r.Room_ID              = b.Room_ID
        JOIN Hotels h          ON h.Hotel_ID             = r.Hotel_ID
        JOIN Room_Types rt     ON rt.Room_Type_Code      = r.Room_Type_Code
        WHERE b.Booking_ID = %s
    """
    return jsonify(query(sql, (booking_id,), fetchone=True))

@app.route("/api/bookings", methods=["POST"])
def create_booking():
    d   = request.json
    sql = """INSERT INTO Bookings
             (Booking_ID, Customer_ID, Room_ID, Booking_Status_Code, Date_From, Date_To)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    query(sql, (d["booking_id"], d["customer_id"], d["room_id"],
                d.get("status_code","CNF"), d["date_from"], d["date_to"]), commit=True)
    # mark room as occupied in Room_Availability for each day
    from datetime import date, timedelta
    start = date.fromisoformat(d["date_from"])
    end   = date.fromisoformat(d["date_to"])
    day   = start
    while day < end:
        avail_sql = """INSERT INTO Room_Availability (Room_ID, Day_Date, Status)
                       VALUES (%s, %s, 'Occupied')
                       ON DUPLICATE KEY UPDATE Status='Occupied'"""
        query(avail_sql, (d["room_id"], str(day)), commit=True)
        day += timedelta(days=1)
    return jsonify({"success": True, "booking_id": d["booking_id"]}), 201

@app.route("/api/bookings/<int:booking_id>/status", methods=["PUT"])
def update_booking_status(booking_id):
    """
    Valid status transitions:
      CNF  → Confirmed
      CHI  → Checked-In
      CHO  → Checked-Out
      CNC  → Cancelled
    """
    d          = request.json
    status_code = d["status_code"]
    sql = "UPDATE Bookings SET Booking_Status_Code=%s WHERE Booking_ID=%s"
    query(sql, (status_code, booking_id), commit=True)
    return jsonify({"success": True})


# ═══════════════════════════════════════════════════════════════
#  REPORTS / ANALYTICS
# ═══════════════════════════════════════════════════════════════

@app.route("/api/reports/summary", methods=["GET"])
def report_summary():
    total_bookings = query("SELECT COUNT(*) AS cnt FROM Bookings", fetchone=True)["cnt"]
    active_guests  = query("""SELECT COUNT(*) AS cnt FROM Bookings b
                              JOIN Booking_Status bs ON bs.Booking_Status_Code=b.Booking_Status_Code
                              WHERE bs.Description='Checked-In'""", fetchone=True)["cnt"]
    total_rooms    = query("SELECT COUNT(*) AS cnt FROM Rooms", fetchone=True)["cnt"]
    revenue        = query("""
        SELECT ROUND(SUM(rt.Standard_Rate * DATEDIFF(b.Date_To, b.Date_From) * 1.1), 2) AS total
        FROM Bookings b
        JOIN Rooms r     ON r.Room_ID       = b.Room_ID
        JOIN Room_Types rt ON rt.Room_Type_Code = r.Room_Type_Code
        JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
        WHERE bs.Description IN ('Confirmed','Checked-In','Checked-Out')
    """, fetchone=True)["total"] or 0

    return jsonify({
        "total_bookings": total_bookings,
        "active_guests":  active_guests,
        "total_rooms":    total_rooms,
        "total_revenue":  float(revenue)
    })

@app.route("/api/reports/occupancy", methods=["GET"])
def report_occupancy():
    sql = """
        SELECT h.Hotel_Name,
               COUNT(r.Room_ID) AS Total_Rooms,
               SUM(CASE WHEN ra.Status='Occupied' THEN 1 ELSE 0 END) AS Occupied,
               ROUND(
                   SUM(CASE WHEN ra.Status='Occupied' THEN 1 ELSE 0 END) * 100.0 / COUNT(r.Room_ID),
               1) AS Occupancy_Pct
        FROM Hotels h
        JOIN Rooms r ON r.Hotel_ID = h.Hotel_ID
        LEFT JOIN Room_Availability ra ON ra.Room_ID = r.Room_ID AND ra.Day_Date = CURDATE()
        GROUP BY h.Hotel_ID, h.Hotel_Name
    """
    return jsonify(query(sql))

@app.route("/api/reports/top-customers", methods=["GET"])
def report_top_customers():
    sql = """
        SELECT c.Customer_ID,
               CONCAT(c.First_Name,' ',c.Last_Name) AS Name,
               COUNT(b.Booking_ID) AS Total_Bookings,
               ROUND(SUM(rt.Standard_Rate * DATEDIFF(b.Date_To, b.Date_From) * 1.1), 2) AS Total_Spent
        FROM Customers c
        JOIN Bookings b    ON b.Customer_ID    = c.Customer_ID
        JOIN Rooms r       ON r.Room_ID        = b.Room_ID
        JOIN Room_Types rt ON rt.Room_Type_Code = r.Room_Type_Code
        GROUP BY c.Customer_ID
        ORDER BY Total_Bookings DESC
        LIMIT 10
    """
    return jsonify(query(sql))

@app.route("/api/reports/revenue-by-type", methods=["GET"])
def report_revenue_by_type():
    sql = """
        SELECT rt.Description AS Room_Type,
               COUNT(b.Booking_ID) AS Bookings,
               ROUND(SUM(rt.Standard_Rate * DATEDIFF(b.Date_To, b.Date_From) * 1.1), 2) AS Revenue
        FROM Bookings b
        JOIN Rooms r       ON r.Room_ID         = b.Room_ID
        JOIN Room_Types rt ON rt.Room_Type_Code  = r.Room_Type_Code
        GROUP BY rt.Room_Type_Code, rt.Description
        ORDER BY Revenue DESC
    """
    return jsonify(query(sql))


# ═══════════════════════════════════════════════════════════════
#  SERVE FRONTEND
# ═══════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# ─── ENTRY POINT ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  AbHi Stay Hotel System — Flask API")
    print("  Group 01 | Absar (22P-9068) & Hina (22P-9198)")
    print("=" * 55)
    print("  Server: http://localhost:5000")
    print("  DB:     MySQL  →  database 'hotel'")
    print("=" * 55)
    app.run(debug=True, port=5000)