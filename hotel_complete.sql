-- ════════════════════════════════════════════════════════════════
--  Hotel Reservation & Room Booking System
--  Group 01 — Absar (22P-9068) | Hina Rashid (22P-9198)
--  Complete SQL: Schema + Sample Data + Analytical Queries
-- ════════════════════════════════════════════════════════════════

-- ─── 0. DATABASE ─────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS hotel;
USE hotel;

-- ─── 1. SCHEMA ───────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS Country (
    Country_Code     VARCHAR(18)  PRIMARY KEY,
    Country_Name     VARCHAR(100),
    Country_Currency VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS City (
    City_Code    VARCHAR(18)  PRIMARY KEY,
    City_Name    VARCHAR(100),
    Country_Code VARCHAR(18),
    FOREIGN KEY (Country_Code) REFERENCES Country(Country_Code)
);

CREATE TABLE IF NOT EXISTS Hotel_Chains (
    Hotel_Chain_Code VARCHAR(50) PRIMARY KEY,
    Hotel_Chain_Name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Hotels (
    Hotel_ID         INT          PRIMARY KEY,
    Hotel_Name       VARCHAR(100),
    Hotel_Address    VARCHAR(200),
    Email_Address    VARCHAR(100),
    Country_Code     VARCHAR(18),
    Hotel_Chain_Code VARCHAR(50),
    FOREIGN KEY (Country_Code)     REFERENCES Country(Country_Code),
    FOREIGN KEY (Hotel_Chain_Code) REFERENCES Hotel_Chains(Hotel_Chain_Code)
);

CREATE TABLE IF NOT EXISTS Room_Types (
    Room_Type_Code VARCHAR(18)    PRIMARY KEY,
    Description    VARCHAR(100),
    Standard_Rate  DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS Rooms (
    Room_ID        INT         PRIMARY KEY,
    Room_Number    INT,
    Room_Floor     INT,
    Hotel_ID       INT,
    Room_Type_Code VARCHAR(18),
    FOREIGN KEY (Hotel_ID)       REFERENCES Hotels(Hotel_ID),
    FOREIGN KEY (Room_Type_Code) REFERENCES Room_Types(Room_Type_Code)
);

CREATE TABLE IF NOT EXISTS Customers (
    Customer_ID INT          AUTO_INCREMENT PRIMARY KEY,
    First_Name  VARCHAR(100),
    Last_Name   VARCHAR(100),
    Address     VARCHAR(200),
    Age         INT,
    Country_Code VARCHAR(18),
    City_Code    VARCHAR(18),
    FOREIGN KEY (Country_Code) REFERENCES Country(Country_Code),
    FOREIGN KEY (City_Code)    REFERENCES City(City_Code)
);

CREATE TABLE IF NOT EXISTS Booking_Status (
    Booking_Status_Code VARCHAR(18)  PRIMARY KEY,
    Description         VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Bookings (
    Booking_ID          INT         PRIMARY KEY,
    Customer_ID         INT,
    Room_ID             INT,
    Booking_Status_Code VARCHAR(18),
    Date_From           DATE,
    Date_To             DATE,
    FOREIGN KEY (Customer_ID)         REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Room_ID)             REFERENCES Rooms(Room_ID),
    FOREIGN KEY (Booking_Status_Code) REFERENCES Booking_Status(Booking_Status_Code)
);

CREATE TABLE IF NOT EXISTS Room_Availability (
    Room_ID  INT,
    Day_Date DATE,
    Status   VARCHAR(50),
    PRIMARY KEY (Room_ID, Day_Date),
    FOREIGN KEY (Room_ID) REFERENCES Rooms(Room_ID)
);

CREATE TABLE IF NOT EXISTS Daily_Room_Rates (
    Hotel_ID       INT,
    Room_ID        INT,
    Day_Date       DATE,
    Daily_Room_Rate DECIMAL(10,2),
    PRIMARY KEY (Hotel_ID, Room_ID, Day_Date),
    FOREIGN KEY (Hotel_ID) REFERENCES Hotels(Hotel_ID),
    FOREIGN KEY (Room_ID)  REFERENCES Rooms(Room_ID)
);

CREATE TABLE IF NOT EXISTS Hotel_Features (
    Feature_Code VARCHAR(18)  PRIMARY KEY,
    Description  VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Specific_Hotel_Feature (
    Hotel_ID     INT,
    Feature_Code VARCHAR(18),
    PRIMARY KEY (Hotel_ID, Feature_Code),
    FOREIGN KEY (Hotel_ID)     REFERENCES Hotels(Hotel_ID),
    FOREIGN KEY (Feature_Code) REFERENCES Hotel_Features(Feature_Code)
);


-- ════════════════════════════════════════════════════════════════
--  2. SAMPLE DATA
-- ════════════════════════════════════════════════════════════════

-- Countries
INSERT INTO Country VALUES
('PK', 'Pakistan',     'PKR'),
('AE', 'UAE',          'AED'),
('GB', 'United Kingdom','GBP'),
('US', 'United States','USD'),
('SA', 'Saudi Arabia', 'SAR');

-- Cities
INSERT INTO City VALUES
('KHI', 'Karachi',   'PK'),
('LHR', 'Lahore',    'PK'),
('ISB', 'Islamabad', 'PK'),
('DXB', 'Dubai',     'AE'),
('LDN', 'London',    'GB'),
('NYC', 'New York',  'US');

-- Hotel Chains
INSERT INTO Hotel_Chains VALUES
('LUXE',   'LuxeStay Group'),
('PEARL',  'Pearl Hotels International'),
('SERENA', 'Serena International'),
('AVARI',  'Avari Hotels');

-- Hotels
INSERT INTO Hotels VALUES
(1, 'Grand Luxe Hotel',     'Clifton Block 4, Karachi',             'info@grandluxe.pk',    'PK', 'LUXE'),
(2, 'Pearl Continental',    'Shahrah-e-Quaid-e-Azam, Lahore',       'res@pc-lahore.pk',     'PK', 'PEARL'),
(3, 'Serena Heights',       'Khayaban-e-Suhrwardy, Islamabad',      'bookings@serena.pk',   'PK', 'SERENA'),
(4, 'Avari Towers',         'Fatima Jinnah Road, Karachi',          'info@avari-khi.pk',    'PK', 'AVARI'),
(5, 'Pearl Dubai',          'Sheikh Zayed Road, Dubai',             'res@pearldubai.ae',    'AE', 'PEARL');

-- Room Types
INSERT INTO Room_Types VALUES
('ECO', 'Economy Single',     75.00),
('STD', 'Standard Twin',     120.00),
('DLX', 'Deluxe King',       220.00),
('STE', 'Executive Suite',   480.00),
('PRS', 'Presidential Suite',950.00);

-- Rooms (Hotel 1 — Grand Luxe)
INSERT INTO Rooms VALUES
(101, 101, 1, 1, 'ECO'),
(102, 102, 1, 1, 'STD'),
(103, 103, 1, 1, 'STD'),
(104, 104, 2, 1, 'DLX'),
(105, 105, 2, 1, 'DLX'),
(106, 106, 3, 1, 'STE'),
(107, 107, 3, 1, 'STE'),
(108, 108, 5, 1, 'PRS'),
-- Hotel 2 — Pearl Continental
(201, 201, 1, 2, 'ECO'),
(202, 202, 1, 2, 'STD'),
(203, 203, 2, 2, 'DLX'),
(204, 204, 3, 2, 'STE'),
(205, 205, 5, 2, 'PRS'),
-- Hotel 3 — Serena Heights
(301, 301, 1, 3, 'STD'),
(302, 302, 2, 3, 'DLX'),
(303, 303, 3, 3, 'STE'),
-- Hotel 4 — Avari
(401, 401, 1, 4, 'ECO'),
(402, 402, 2, 4, 'DLX'),
-- Hotel 5 — Pearl Dubai
(501, 501, 1, 5, 'DLX'),
(502, 502, 2, 5, 'STE'),
(503, 503, 5, 5, 'PRS');

-- Customers
INSERT INTO Customers (Customer_ID, First_Name, Last_Name, Address, Age, Country_Code, City_Code) VALUES
(1,  'Ahmed',   'Khan',      'House 12, Block A, DHA Karachi',         32, 'PK', 'KHI'),
(2,  'Sara',    'Ali',       'Gulberg III, Lahore',                     28, 'PK', 'LHR'),
(3,  'Omar',    'Siddiqui',  'F-7/2, Islamabad',                       45, 'PK', 'ISB'),
(4,  'Fatima',  'Malik',     'JBR, Dubai Marina',                      35, 'AE', 'DXB'),
(5,  'Bilal',   'Chaudhry',  'Clifton, Karachi',                       40, 'PK', 'KHI'),
(6,  'Aisha',   'Raza',      'Model Town, Lahore',                     29, 'PK', 'LHR'),
(7,  'Zaid',    'Hassan',    'Blue Area, Islamabad',                   38, 'PK', 'ISB'),
(8,  'Hina',    'Rashid',    'Cantt, Karachi',                         26, 'PK', 'KHI'),
(9,  'Absar',   'Ahmed',     'FAST-NUCES, Karachi',                    22, 'PK', 'KHI'),
(10, 'John',    'Smith',     '10 Downing St, London',                  55, 'GB', 'LDN');

-- Booking Status Codes
INSERT INTO Booking_Status VALUES
('CNF', 'Confirmed'),
('CHI', 'Checked-In'),
('CHO', 'Checked-Out'),
('CNC', 'Cancelled'),
('PND', 'Pending');

-- Bookings
INSERT INTO Bookings VALUES
(1001, 1,  104, 'CHO', '2025-04-01', '2025-04-04'),
(1002, 2,  202, 'CHO', '2025-04-05', '2025-04-07'),
(1003, 3,  204, 'CHO', '2025-04-10', '2025-04-13'),
(1004, 4,  502, 'CHO', '2025-04-15', '2025-04-18'),
(1005, 5,  104, 'CHO', '2025-04-20', '2025-04-22'),
(1006, 6,  302, 'CHO', '2025-04-25', '2025-04-28'),
(1007, 7,  106, 'CHI', '2025-05-10', '2025-05-13'),
(1008, 1,  203, 'CHI', '2025-05-11', '2025-05-14'),
(1009, 8,  301, 'CNF', '2025-05-15', '2025-05-17'),
(1010, 9,  102, 'CNF', '2025-05-15', '2025-05-16'),
(1011, 10, 501, 'CNF', '2025-05-20', '2025-05-25'),
(1012, 2,  303, 'CNF', '2025-05-22', '2025-05-24'),
(1013, 5,  108, 'CNC', '2025-05-01', '2025-05-03'),
(1014, 3,  205, 'CNC', '2025-04-30', '2025-05-02'),
(1015, 4,  105, 'CHO', '2025-03-15', '2025-03-18');

-- Room Availability (sample — today's snapshot)
INSERT INTO Room_Availability VALUES
(104, CURDATE(), 'Occupied'),
(106, CURDATE(), 'Occupied'),
(203, CURDATE(), 'Occupied'),
(108, CURDATE(), 'Available'),
(501, CURDATE(), 'Available'),
(303, CURDATE(), 'Available'),
(301, CURDATE(), 'Available'),
(102, CURDATE(), 'Available');

-- Daily Room Rates (weekend premium for suites)
INSERT INTO Daily_Room_Rates VALUES
(1, 106, '2025-05-17', 550.00),
(1, 106, '2025-05-18', 550.00),
(2, 204, '2025-05-17', 530.00),
(5, 502, '2025-05-17', 520.00);

-- Hotel Features
INSERT INTO Hotel_Features VALUES
('POOL',   'Swimming Pool'),
('GYM',    'Fitness Center'),
('SPA',    'Luxury Spa'),
('REST',   'Fine Dining Restaurant'),
('CONF',   'Conference Rooms'),
('PARK',   'Parking Facility'),
('WIFI',   'High-Speed Wi-Fi'),
('BAR',    'Rooftop Bar'),
('BEACH',  'Private Beach Access'),
('BUTLER', 'Butler Service');

-- Specific Hotel Features
INSERT INTO Specific_Hotel_Feature VALUES
(1,'POOL'),(1,'GYM'),(1,'SPA'),(1,'REST'),(1,'WIFI'),(1,'BAR'),
(2,'GYM'),(2,'REST'),(2,'CONF'),(2,'WIFI'),(2,'PARK'),
(3,'SPA'),(3,'REST'),(3,'WIFI'),(3,'CONF'),
(4,'POOL'),(4,'GYM'),(4,'REST'),(4,'WIFI'),
(5,'POOL'),(5,'SPA'),(5,'BEACH'),(5,'BUTLER'),(5,'BAR');


-- ════════════════════════════════════════════════════════════════
--  3. ANALYTICAL QUERIES  (Course Requirements)
-- ════════════════════════════════════════════════════════════════

-- ── Q1: All hotels with their chain name and room count ────────
SELECT
    h.Hotel_ID,
    h.Hotel_Name,
    h.Hotel_Address,
    hc.Hotel_Chain_Name,
    c.Country_Name,
    COUNT(r.Room_ID) AS Total_Rooms
FROM Hotels h
JOIN Hotel_Chains hc ON hc.Hotel_Chain_Code = h.Hotel_Chain_Code
JOIN Country c       ON c.Country_Code      = h.Country_Code
LEFT JOIN Rooms r    ON r.Hotel_ID          = h.Hotel_ID
GROUP BY h.Hotel_ID, h.Hotel_Name, h.Hotel_Address, hc.Hotel_Chain_Name, c.Country_Name
ORDER BY h.Hotel_ID;

-- ── Q2: Available rooms between two dates ─────────────────────
-- (Replace dates as needed)
SELECT
    r.Room_ID,
    r.Room_Number,
    r.Room_Floor,
    h.Hotel_Name,
    rt.Description    AS Room_Type,
    rt.Standard_Rate  AS Rate_Per_Night
FROM Rooms r
JOIN Hotels     h  ON h.Hotel_ID        = r.Hotel_ID
JOIN Room_Types rt ON rt.Room_Type_Code = r.Room_Type_Code
WHERE r.Room_ID NOT IN (
    SELECT b.Room_ID
    FROM Bookings b
    JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
    WHERE bs.Description NOT IN ('Cancelled','Checked-Out')
      AND NOT (b.Date_To <= '2025-05-15' OR b.Date_From >= '2025-05-20')
)
ORDER BY rt.Standard_Rate;

-- ── Q3: Full booking details with guest & room info ───────────
SELECT
    b.Booking_ID,
    CONCAT(c.First_Name,' ',c.Last_Name)   AS Guest_Name,
    c.Age,
    h.Hotel_Name,
    r.Room_Number,
    rt.Description                          AS Room_Type,
    b.Date_From,
    b.Date_To,
    DATEDIFF(b.Date_To, b.Date_From)        AS Nights,
    rt.Standard_Rate,
    ROUND(rt.Standard_Rate * DATEDIFF(b.Date_To,b.Date_From), 2) AS Subtotal,
    ROUND(rt.Standard_Rate * DATEDIFF(b.Date_To,b.Date_From) * 1.10, 2) AS Total_With_Tax,
    bs.Description                          AS Status
FROM Bookings b
JOIN Customers    c  ON c.Customer_ID         = b.Customer_ID
JOIN Rooms        r  ON r.Room_ID             = b.Room_ID
JOIN Hotels       h  ON h.Hotel_ID            = r.Hotel_ID
JOIN Room_Types   rt ON rt.Room_Type_Code     = r.Room_Type_Code
JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
ORDER BY b.Booking_ID;

-- ── Q4: Currently checked-in guests ──────────────────────────
SELECT
    b.Booking_ID,
    CONCAT(c.First_Name,' ',c.Last_Name) AS Guest_Name,
    h.Hotel_Name,
    r.Room_Number,
    rt.Description AS Room_Type,
    b.Date_From    AS Check_In_Date,
    b.Date_To      AS Check_Out_Date,
    DATEDIFF(b.Date_To, CURDATE()) AS Nights_Remaining
FROM Bookings b
JOIN Customers    c  ON c.Customer_ID = b.Customer_ID
JOIN Rooms        r  ON r.Room_ID = b.Room_ID
JOIN Hotels       h  ON h.Hotel_ID = r.Hotel_ID
JOIN Room_Types   rt ON rt.Room_Type_Code = r.Room_Type_Code
JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
WHERE bs.Description = 'Checked-In';

-- ── Q5: Revenue per hotel ─────────────────────────────────────
SELECT
    h.Hotel_Name,
    COUNT(b.Booking_ID)                                              AS Total_Bookings,
    ROUND(SUM(rt.Standard_Rate * DATEDIFF(b.Date_To, b.Date_From)), 2) AS Gross_Revenue,
    ROUND(SUM(rt.Standard_Rate * DATEDIFF(b.Date_To, b.Date_From)) * 1.10, 2) AS Revenue_With_Tax
FROM Hotels h
JOIN Rooms r       ON r.Hotel_ID        = h.Hotel_ID
JOIN Bookings b    ON b.Room_ID         = r.Room_ID
JOIN Room_Types rt ON rt.Room_Type_Code = r.Room_Type_Code
JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
WHERE bs.Description IN ('Confirmed','Checked-In','Checked-Out')
GROUP BY h.Hotel_ID, h.Hotel_Name
ORDER BY Gross_Revenue DESC;

-- ── Q6: Occupancy rate per hotel today ───────────────────────
SELECT
    h.Hotel_Name,
    COUNT(r.Room_ID)                                                   AS Total_Rooms,
    SUM(CASE WHEN ra.Status = 'Occupied' THEN 1 ELSE 0 END)            AS Occupied_Rooms,
    ROUND(
        SUM(CASE WHEN ra.Status = 'Occupied' THEN 1 ELSE 0 END) * 100.0
        / COUNT(r.Room_ID), 1
    )                                                                   AS Occupancy_Pct
FROM Hotels h
JOIN Rooms r ON r.Hotel_ID = h.Hotel_ID
LEFT JOIN Room_Availability ra ON ra.Room_ID = r.Room_ID AND ra.Day_Date = CURDATE()
GROUP BY h.Hotel_ID, h.Hotel_Name;

-- ── Q7: Top 5 customers by number of bookings ────────────────
SELECT
    c.Customer_ID,
    CONCAT(c.First_Name,' ',c.Last_Name) AS Customer_Name,
    c.Age,
    co.Country_Name,
    COUNT(b.Booking_ID)                  AS Total_Bookings,
    ROUND(SUM(rt.Standard_Rate * DATEDIFF(b.Date_To, b.Date_From) * 1.1), 2) AS Total_Spent
FROM Customers c
JOIN Bookings b    ON b.Customer_ID     = c.Customer_ID
JOIN Rooms r       ON r.Room_ID         = b.Room_ID
JOIN Room_Types rt ON rt.Room_Type_Code = r.Room_Type_Code
JOIN Country co    ON co.Country_Code   = c.Country_Code
GROUP BY c.Customer_ID, c.First_Name, c.Last_Name, c.Age, co.Country_Name
ORDER BY Total_Bookings DESC
LIMIT 5;

-- ── Q8: Revenue breakdown by room type ───────────────────────
SELECT
    rt.Description AS Room_Type,
    COUNT(b.Booking_ID)                                                          AS Bookings,
    ROUND(SUM(rt.Standard_Rate * DATEDIFF(b.Date_To,b.Date_From)), 2)           AS Gross_Revenue,
    ROUND(AVG(DATEDIFF(b.Date_To,b.Date_From)), 1)                              AS Avg_Stay_Nights
FROM Room_Types rt
LEFT JOIN Rooms r    ON r.Room_Type_Code = rt.Room_Type_Code
LEFT JOIN Bookings b ON b.Room_ID        = r.Room_ID
GROUP BY rt.Room_Type_Code, rt.Description
ORDER BY Gross_Revenue DESC;

-- ── Q9: Booking history for a specific customer ───────────────
-- (Change Customer_ID as needed)
SELECT
    b.Booking_ID,
    h.Hotel_Name,
    r.Room_Number,
    rt.Description                                                      AS Room_Type,
    b.Date_From, b.Date_To,
    DATEDIFF(b.Date_To,b.Date_From)                                    AS Nights,
    ROUND(rt.Standard_Rate*DATEDIFF(b.Date_To,b.Date_From)*1.1, 2)   AS Amount,
    bs.Description                                                      AS Status
FROM Bookings b
JOIN Rooms r       ON r.Room_ID          = b.Room_ID
JOIN Hotels h      ON h.Hotel_ID         = r.Hotel_ID
JOIN Room_Types rt ON rt.Room_Type_Code  = r.Room_Type_Code
JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
WHERE b.Customer_ID = 1
ORDER BY b.Date_From DESC;

-- ── Q10: Rooms with their features per hotel ─────────────────
SELECT
    h.Hotel_Name,
    GROUP_CONCAT(hf.Description ORDER BY hf.Description SEPARATOR ', ') AS Features
FROM Hotels h
JOIN Specific_Hotel_Feature shf ON shf.Hotel_ID     = h.Hotel_ID
JOIN Hotel_Features hf          ON hf.Feature_Code  = shf.Feature_Code
GROUP BY h.Hotel_ID, h.Hotel_Name;

-- ── Q11: Monthly booking trend ───────────────────────────────
SELECT
    DATE_FORMAT(b.Date_From, '%Y-%m')  AS Month,
    COUNT(b.Booking_ID)                AS Bookings,
    ROUND(SUM(rt.Standard_Rate * DATEDIFF(b.Date_To,b.Date_From)*1.1),2) AS Revenue
FROM Bookings b
JOIN Rooms r       ON r.Room_ID        = b.Room_ID
JOIN Room_Types rt ON rt.Room_Type_Code = r.Room_Type_Code
GROUP BY DATE_FORMAT(b.Date_From,'%Y-%m')
ORDER BY Month;

-- ── Q12: Rooms that have never been booked ────────────────────
SELECT
    r.Room_ID, r.Room_Number, h.Hotel_Name, rt.Description AS Room_Type
FROM Rooms r
JOIN Hotels     h  ON h.Hotel_ID        = r.Hotel_ID
JOIN Room_Types rt ON rt.Room_Type_Code = r.Room_Type_Code
WHERE r.Room_ID NOT IN (SELECT DISTINCT Room_ID FROM Bookings);

-- ── Q13: Average stay duration per room type ─────────────────
SELECT
    rt.Description                           AS Room_Type,
    ROUND(AVG(DATEDIFF(b.Date_To,b.Date_From)),1) AS Avg_Nights,
    COUNT(b.Booking_ID)                      AS Total_Bookings
FROM Bookings b
JOIN Rooms r       ON r.Room_ID          = b.Room_ID
JOIN Room_Types rt ON rt.Room_Type_Code  = r.Room_Type_Code
GROUP BY rt.Room_Type_Code, rt.Description;

-- ── Q14: Cancellation rate per hotel ──────────────────────────
SELECT
    h.Hotel_Name,
    COUNT(b.Booking_ID)                                           AS Total_Bookings,
    SUM(CASE WHEN bs.Description='Cancelled' THEN 1 ELSE 0 END)  AS Cancelled,
    ROUND(SUM(CASE WHEN bs.Description='Cancelled' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS Cancellation_Pct
FROM Hotels h
JOIN Rooms r ON r.Hotel_ID = h.Hotel_ID
JOIN Bookings b ON b.Room_ID = r.Room_ID
JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
GROUP BY h.Hotel_ID, h.Hotel_Name;

-- ── Q15: Upcoming check-ins (next 7 days) ────────────────────
SELECT
    b.Booking_ID,
    CONCAT(c.First_Name,' ',c.Last_Name) AS Guest,
    h.Hotel_Name,
    r.Room_Number,
    rt.Description AS Room_Type,
    b.Date_From    AS Check_In,
    b.Date_To      AS Check_Out
FROM Bookings b
JOIN Customers    c  ON c.Customer_ID = b.Customer_ID
JOIN Rooms        r  ON r.Room_ID = b.Room_ID
JOIN Hotels       h  ON h.Hotel_ID = r.Hotel_ID
JOIN Room_Types   rt ON rt.Room_Type_Code = r.Room_Type_Code
JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
WHERE bs.Description = 'Confirmed'
  AND b.Date_From BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
ORDER BY b.Date_From;

-- ════════════════════════════════════════════════════════════════
--  4. STORED PROCEDURE: Book a Room
-- ════════════════════════════════════════════════════════════════

DELIMITER $$

CREATE PROCEDURE IF NOT EXISTS sp_CreateBooking(
    IN  p_booking_id  INT,
    IN  p_customer_id INT,
    IN  p_room_id     INT,
    IN  p_date_from   DATE,
    IN  p_date_to     DATE,
    OUT p_result      VARCHAR(100)
)
BEGIN
    DECLARE v_conflict INT DEFAULT 0;

    -- Check for conflicting bookings
    SELECT COUNT(*) INTO v_conflict
    FROM Bookings b
    JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
    WHERE b.Room_ID = p_room_id
      AND bs.Description NOT IN ('Cancelled','Checked-Out')
      AND NOT (b.Date_To <= p_date_from OR b.Date_From >= p_date_to);

    IF v_conflict > 0 THEN
        SET p_result = 'ERROR: Room not available for selected dates.';
    ELSE
        INSERT INTO Bookings (Booking_ID, Customer_ID, Room_ID, Booking_Status_Code, Date_From, Date_To)
        VALUES (p_booking_id, p_customer_id, p_room_id, 'CNF', p_date_from, p_date_to);
        SET p_result = CONCAT('SUCCESS: Booking #', p_booking_id, ' created.');
    END IF;
END$$

DELIMITER ;

-- Example call:
-- CALL sp_CreateBooking(2001, 1, 105, '2025-06-01', '2025-06-04', @result);
-- SELECT @result;


-- ════════════════════════════════════════════════════════════════
--  5. VIEWS
-- ════════════════════════════════════════════════════════════════

-- View: Active bookings with full details
CREATE OR REPLACE VIEW vw_Active_Bookings AS
SELECT
    b.Booking_ID,
    CONCAT(c.First_Name,' ',c.Last_Name)    AS Guest_Name,
    h.Hotel_Name,
    r.Room_Number,
    rt.Description                           AS Room_Type,
    b.Date_From, b.Date_To,
    DATEDIFF(b.Date_To, b.Date_From)         AS Nights,
    ROUND(rt.Standard_Rate*DATEDIFF(b.Date_To,b.Date_From)*1.1, 2) AS Total_Amount,
    bs.Description                           AS Status
FROM Bookings b
JOIN Customers    c  ON c.Customer_ID = b.Customer_ID
JOIN Rooms        r  ON r.Room_ID = b.Room_ID
JOIN Hotels       h  ON h.Hotel_ID = r.Hotel_ID
JOIN Room_Types   rt ON rt.Room_Type_Code = r.Room_Type_Code
JOIN Booking_Status bs ON bs.Booking_Status_Code = b.Booking_Status_Code
WHERE bs.Description IN ('Confirmed','Checked-In');

-- View: Hotel occupancy summary
CREATE OR REPLACE VIEW vw_Hotel_Occupancy AS
SELECT
    h.Hotel_Name,
    COUNT(r.Room_ID) AS Total_Rooms,
    SUM(CASE WHEN ra.Status='Occupied' THEN 1 ELSE 0 END) AS Occupied_Today,
    ROUND(
        SUM(CASE WHEN ra.Status='Occupied' THEN 1 ELSE 0 END)*100.0/COUNT(r.Room_ID), 1
    ) AS Occupancy_Pct
FROM Hotels h
JOIN Rooms r ON r.Hotel_ID = h.Hotel_ID
LEFT JOIN Room_Availability ra ON ra.Room_ID = r.Room_ID AND ra.Day_Date = CURDATE()
GROUP BY h.Hotel_ID, h.Hotel_Name;

-- ════════════════════════════════════════════════════════════════
-- END OF SCRIPT
-- ════════════════════════════════════════════════════════════════
