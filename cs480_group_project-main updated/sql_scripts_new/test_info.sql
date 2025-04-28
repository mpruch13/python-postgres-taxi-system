-- A SQL script for inserting some starting sample data.

-- So far just has some things for testing manager the manger functions I've started.
-- No entries for tables: ClientAddress, Drives, CreditCard, or Review

-- Managers
INSERT INTO Manager VALUES
    ('222333444', 'bigbossboris@taxidrivers.com', 'Boris');

-- Clients
INSERT INTO Client VALUES
    ('maria45@gmail.com','Maria'),
    ('bobbyb33@hotmail.com','Bobby'),
    ('juan77@gmail.com','Juan');

-- Addresses
INSERT INTO Address VALUES
    ('A0000001', 100, 'Main St',    'Chicago'),
    ('A0000002', 200, 'Oak Ave',    'Chicago'),
    ('A0000003', 300, 'Pine Rd',    'Evanston'),
    ('A0000004', 400, 'Elm St',     'Naperville');

-- Client–Address relationships
INSERT INTO ClientAddresses VALUES
    ('maria45@gmail.com','A0000001'),
    ('maria45@gmail.com','A0000003'),
    ('bobbyb33@hotmail.com','A0000002'),
    ('juan77@gmail.com','A0000004');

-- Credit cards
INSERT INTO CreditCard VALUES
    ('4111222233334444','maria45@gmail.com','A0000001'),
    ('5555666677778888','bobbyb33@hotmail.com','A0000002'),
    ('9999000011112222','juan77@gmail.com','A0000004');

-- Cars
INSERT INTO Car VALUES
    ('C1111111','Mercedes'),
    ('C2222222','Ford'),
    ('C3333333','Toyota');

-- Models
INSERT INTO Model VALUES
    ('M1111111','C1111111','black',    'automatic',2020),
    ('M2334455','C2222222','silver',   'manual',   2019),
    ('M4556677','C3333333','white',    'automatic',2021);

-- Drivers
INSERT INTO Driver VALUES
    ('Stanley','A0000001'),
    ('Alice',  'A0000002'),
    ('Charles','A0000004');

-- Driver–Model qualifications
INSERT INTO Drives VALUES
    ('Stanley','M2334455'),
    ('Alice',  'M4556677'),
    ('Charles','M1111111');

-- Rents
INSERT INTO Rent VALUES
    ('R2222222','2025-04-15','maria45@gmail.com','Stanley','M2334455'),
    ('R3333333','2025-04-16','maria45@gmail.com','Stanley','M2334455'),
    ('R4444444','2025-04-17','maria45@gmail.com','Stanley','M2334455');

-- 5 rents of model M4556677
INSERT INTO Rent VALUES
    ('R5555555','2025-04-14','bobbyb33@hotmail.com','Alice','M4556677'),
    ('R6666666','2025-04-15','bobbyb33@hotmail.com','Alice','M4556677'),
    ('R7777777','2025-04-16','bobbyb33@hotmail.com','Alice','M4556677'),
    ('R8888888','2025-04-17','bobbyb33@hotmail.com','Alice','M4556677'),
    ('R9999999','2025-04-18','bobbyb33@hotmail.com','Alice','M4556677');

-- 3 rents of model M1111111
INSERT INTO Rent VALUES
    ('R1234567','2025-04-14','juan77@gmail.com','Charles','M1111111'),
    ('R2345678','2025-04-15','juan77@gmail.com','Charles','M1111111'),
    ('R3456789','2025-04-16','juan77@gmail.com','Charles','M1111111');

-- Reviews (one per client–driver after each has at least one rent)
INSERT INTO Review VALUES
    ('RVW0001','Stanley','maria45@gmail.com','Very smooth ride',         5),
    ('RVW0002','Alice',  'bobbyb33@hotmail.com','Friendly and punctual',4),
    ('RVW0003','Charles','juan77@gmail.com','Professional service',      5);
