# 🏨 Hotel Reservation & Room Booking System

## Group Information

| | |
|---|---|
| **Group Number** | 01 |
| **Member 1** | Absar — 22P-9068 |
| **Member 2** | Hina Rashid — 22P-9198 |
| **Course** | Database Systems Lab |
| **Institute** | FAST-NUCES, Karachi |

---

## Project Description

A full-stack Hotel Reservation & Room Booking System that allows guests to search and book rooms, receptionists to manage check-in/check-out, and admins to manage hotels, rooms, customers, and view analytics reports.

**Three user roles:**
- 🧳 **Guest** — Search rooms, make bookings, cancel reservations
- 🏨 **Reception** — Check-in / Check-out, walk-in bookings, room availability
- ⚙️ **Admin** — CRUD for hotels/rooms/customers, revenue dashboard, reports

---

## GitHub Repository

🔗 **https://github.com/YOUR_USERNAME/hotel-reservation-system**

> Replace with your actual GitHub link before submitting.

---

## Technologies Used

| Layer | Technology |
|---|---|
| Database | MySQL 8.x |
| Backend | Python 3.x + Flask |
| Frontend | HTML5, CSS3, JavaScript |
| DB Connector | mysql-connector-python |
| Version Control | Git & GitHub |

---

## Project Files

```
hotel-reservation-system/
├── index.html          ← Frontend (open in browser)
├── app.py              ← Python Flask backend
├── hotel_complete.sql  ← Database script
└── README.md           ← This file
```

---

# ▶️ HOW TO RUN ON WINDOWS (Step by Step)

---

## ✅ OPTION A — Run Frontend Only (Easiest, No Install Needed)

> Best for demo and viva. Everything works directly in the browser.

1. Find the file **`index.html`** in your project folder
2. **Double-click** it — it opens in Chrome or Edge automatically
3. Done ✅

Login with:

| Role | Email |
|---|---|
| Guest | guest@luxestay.com |
| Reception | reception@luxestay.com |
| Admin | admin@luxestay.com |

Password: type anything and press **Sign In**

---

## ✅ OPTION B — Full Stack (Frontend + Python Flask + MySQL)

### STEP 1 — Install MySQL

1. Download **MySQL Installer** from: https://dev.mysql.com/downloads/installer/
2. Run installer → choose **"Developer Default"**
3. Set a **root password** — write it down, you will need it later
4. Finish installation

To verify, open **Command Prompt** and type:
```
mysql -u root -p
```
Enter your password. If you see `mysql>` it is working ✅

---

### STEP 2 — Import the Database

**Using MySQL Workbench (Recommended):**
1. Open **MySQL Workbench** and connect
2. Go to **File → Open SQL Script**
3. Select `hotel_complete.sql` from your project folder
4. Press **Ctrl + Shift + Enter** to run the whole script
5. Refresh the left panel — you will see the `hotel` database ✅

**Using Command Prompt:**
```
mysql -u root -p < C:\path\to\your\hotel_complete.sql
```

---

### STEP 3 — Install Python

1. Download from: https://www.python.org/downloads/
2. Run the installer
3. ⚠️ **IMPORTANT:** At the bottom, tick the checkbox **"Add Python to PATH"**
4. Click **Install Now**

Verify in Command Prompt:
```
python --version
```
Should show `Python 3.x.x` ✅

---

### STEP 4 — Install Required Libraries

Open **Command Prompt** and run:
```
pip install flask flask-cors mysql-connector-python
```
Wait until you see `Successfully installed` ✅

---

### STEP 5 — Set Your MySQL Password in app.py

1. Open `app.py` in Notepad or VS Code
2. Find this block near the top:

```python
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",       # ← put your MySQL password here
    "database": "hotel",
    "autocommit": True
}
```

3. Add your password inside the quotes, save the file (**Ctrl+S**)

---

### STEP 6 — Start the Backend

Open **Command Prompt**, go to your project folder:
```
cd C:\Users\YourName\Desktop\hotel-reservation-system
```
Run:
```
python app.py
```
You will see:
```
* Running on http://localhost:5000
```
✅ Backend is running — do not close this window.

---

### STEP 7 — Open the App

Open Chrome or Edge and visit:
```
http://localhost:5000
```
The full application loads with live MySQL data ✅

---

## 🔐 Login Credentials

| Role | Email | Password |
|---|---|---|
| 🧳 Guest | guest@luxestay.com | anything |
| 🏨 Reception | reception@luxestay.com | anything |
| ⚙️ Admin | admin@luxestay.com | anything |

---

## 📋 CRUD Operations

| Operation | Where in App | SQL |
|---|---|---|
| **CREATE** | Book a room, Add customer, Add hotel | `INSERT INTO ...` |
| **READ** | Search rooms, booking list, dashboard | `SELECT ... JOIN ...` |
| **UPDATE** | Check-In / Check-Out changes status | `UPDATE Bookings SET ...` |
| **DELETE** | Cancel a booking | Status set to `Cancelled` |

---

## ⚠️ Common Errors & Fixes on Windows

| Error | Fix |
|---|---|
| `python is not recognized` | Reinstall Python and tick **"Add to PATH"** |
| `pip is not recognized` | Run CMD as Administrator → `python -m ensurepip` |
| `Access denied for user root` | Wrong password in `app.py` DB_CONFIG |
| `ModuleNotFoundError: flask` | Run `pip install flask flask-cors mysql-connector-python` again |
| `Unknown database hotel` | Run `hotel_complete.sql` in MySQL Workbench first |
| `Port 5000 already in use` | Change `port=5000` to `port=5001` in the last line of `app.py` |

---

## 🗄️ Database Tables (12 Total)

| Table | Purpose |
|---|---|
| `Country`, `City` | Geographic reference data |
| `Hotel_Chains`, `Hotels` | Hotel properties and chains |
| `Room_Types`, `Rooms` | Room inventory and pricing |
| `Customers` | Guest records |
| `Bookings`, `Booking_Status` | Reservation management |
| `Room_Availability` | Daily room status tracking |
| `Daily_Room_Rates` | Dynamic pricing per day |
| `Hotel_Features`, `Specific_Hotel_Feature` | Hotel amenities |

---

*Group 01 — Database Systems Lab — FAST-NUCES Karachi*
