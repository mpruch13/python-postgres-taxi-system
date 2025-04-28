-- A SQL script for inserting some starting sample data.

-- So far just has some things for testing manager the manger functions I've started.
-- No entries for tables: ClientAddress, Drives, CreditCard, or Review


-- Manager
INSERT INTO Manager VALUES (222333444, 'bigbossboris@taxidrivers.com', 'Boris');

-- Car brands
INSERT INTO CAR VALUES('C1111111', 'Mercedes');
INSERT INTO CAR VALUES('C2222222', 'Ford');
INSERT INTO CAR VALUES('C3333333', 'Toyota');

-- Car Models
INSERT INTO Model VALUES('M1111111', 'black', 'automatic', 2020, 'C1111111');
INSERT INTO Model VALUES('M2334455', 'yellow', 'manual', 1977, 'C2222222');
INSERT INTO Model VALUES('M3445566', 'yellow', 'automatic', 2018, 'C2222222');
INSERT INTO Model VALUES('M4556677', 'silver', 'automatic', 2025, 'C3333333');
INSERT INTO Model VALUES('M5667788', 'silver', 'manual', 2025, 'C3333333');

-- Addresses
INSERT INTO Address VALUES(1234, 'Main St', 'Taxi Town');
INSERT INTO Address VALUES(4427, 'North Ave', 'Taxi Town');
INSERT INTO Address VALUES(2929, 'South Ave', 'Taxi Town');
INSERT INTO Address VALUES(5678, 'East Ave', 'Taxi Town');
INSERT INTO Address VALUES(9101, 'West Ave', 'Taxi Town');

-- Drivers
INSERT INTO Driver VALUES('Stanley', 1234, 'Main St', 'Taxi Town');
INSERT INTO Driver VALUES('Alice', 4427, 'North Ave', 'Taxi Town');
INSERT INTO Driver VALues('Charles', 2929, 'South Ave', 'Taxi Town');


-- Clients
INSERT INTO Client VALUES('maria45@gmail.com', 'Maria');
INSERT INTO Client VALUES('bobbyb33@hotmail.com', 'Bob');
INSERT INTO Client VALUES('juan77@gmail.com', 'Juan');

-- Rents
-- 4 rents for model M2334455
INSERT INTO Rent VALUES('R1111111', '4-14-2025', 'maria45@gmail.com', 'Stanley','M2334455');
INSERT INTO Rent VALUES('R2222222', '4-15-2025', 'maria45@gmail.com', 'Stanley','M2334455');
INSERT INTO Rent VALUES('R3333333', '4-16-2025', 'maria45@gmail.com', 'Stanley','M2334455');
INSERT INTO Rent VALUES('R4444444', '4-17-2025', 'maria45@gmail.com', 'Stanley','M2334455');

-- 5 rents for model M4556677
INSERT INTO Rent VALUES('R5555555', '4-14-2025', 'bobbyb33@hotmail.com', 'Alice','M4556677');
INSERT INTO Rent VALUES('R6666666', '4-15-2025', 'bobbyb33@hotmail.com', 'Alice','M4556677');
INSERT INTO Rent VALUES('R7777777', '4-16-2025', 'bobbyb33@hotmail.com', 'Alice','M4556677');
INSERT INTO Rent VALUES('R8888888', '4-17-2025', 'bobbyb33@hotmail.com', 'Alice','M4556677');
INSERT INTO Rent VALUES('R9999999', '4-18-2025', 'bobbyb33@hotmail.com', 'Alice','M4556677');

-- 3 rents for model M1111111
INSERT INTO Rent VALUES('R1234567', '4-14-2025', 'juan77@gmail.com', 'Charles','M1111111');
INSERT INTO Rent VALUES('R2345678', '4-15-2025', 'juan77@gmail.com', 'Charles','M1111111');
INSERT INTO Rent VALUES('R3456789', '4-16-2025', 'juan77@gmail.com', 'Charles','M1111111');