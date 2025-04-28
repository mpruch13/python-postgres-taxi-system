-- Step 1: Translate Strong Entities and composite attributes.
-- Relationships: none
CREATE TABLE IF NOT EXISTS Manager (
    ssn CHAR(9),               -- Manager SSN Primary Key
    email TEXT NOT NULL,       -- Manager email
    name TEXT NOT NULL,        -- Manager name
    PRIMARY KEY(ssn)
);

-- Relationships:
-- Address: handled via ClientAddresses table
-- CreditCard: relates to Client via foreign key in CreditCard
CREATE TABLE IF NOT EXISTS Client (
    email TEXT,                -- Client email (Primary Key)
    name TEXT NOT NULL,        -- Client name
    PRIMARY KEY(email)
);

-- Relationships:
-- Client–Address (1:N) handled by ClientAddresses below
CREATE TABLE IF NOT EXISTS Address (
    address_id CHAR(8),        -- Unique address identifier
    number INT NOT NULL,       -- Street number
    road TEXT NOT NULL,        -- Road name
    city TEXT NOT NULL,        -- City name
    UNIQUE(number, road, city),-- Prevent duplicate addresses
    PRIMARY KEY(address_id)
);

-- Relationships:
-- Driver–Address is (1:1), so Address FK lives in Driver
CREATE TABLE IF NOT EXISTS Driver (
    name TEXT,                 -- Driver name (Primary Key)
    address_id CHAR(8) NOT NULL,-- FK to Address
    PRIMARY KEY(name),
    FOREIGN KEY(address_id) REFERENCES Address(address_id)
);

-- Relationships:
-- CreditCard–Client is (1:N), CreditCard–Address is (0/1:N to 1:1)
CREATE TABLE IF NOT EXISTS CreditCard (
    number CHAR(16),           -- Credit card number (Primary Key)
    client TEXT NOT NULL,      -- FK to Client
    payment_address CHAR(8) NOT NULL, -- FK to Address
    PRIMARY KEY(number),
    FOREIGN KEY(client) REFERENCES Client(email),
    FOREIGN KEY(payment_address) REFERENCES Address(address_id)
);

-- Relationships: none
CREATE TABLE IF NOT EXISTS Car (
    car_id CHAR(8),            -- Car ID (Primary Key)
    brand TEXT NOT NULL,       -- Car brand name
    PRIMARY KEY(car_id)
);

-- Step 2: Translate Weak Entities
-- Model is a weak entity under Car
CREATE TABLE IF NOT EXISTS Model (
    model_id CHAR(8),           -- Model identifier (unique per brand)
    car_id CHAR(8) NOT NULL,    -- FK to Car
    color TEXT NOT NULL,        -- Model color
    transmission TEXT NOT NULL, -- 'manual' or 'automatic'
    year INT NOT NULL,          -- Construction year
    PRIMARY KEY(model_id, car_id),
    FOREIGN KEY(car_id) REFERENCES Car(car_id)
);

-- Review is a weak entity under Driver, one review per (client, driver)
CREATE TABLE IF NOT EXISTS Review (
    review_id CHAR(8) UNIQUE,   -- Review identifier
    driver TEXT NOT NULL,       -- FK to Driver
    client TEXT NOT NULL,       -- FK to Client
    message TEXT,               -- Review message (anonymous allowed)
    rating INT                  -- Rating 0–5
        CHECK (rating >= 0 AND rating <= 5),
    PRIMARY KEY(review_id, driver),
    UNIQUE(client, driver),
    FOREIGN KEY(driver) REFERENCES Driver(name),
    FOREIGN KEY(client) REFERENCES Client(email)
);

-- Step 3: Translate Relationships
-- Client–Address mapping (1:N)
CREATE TABLE IF NOT EXISTS ClientAddresses (
    client TEXT NOT NULL,       -- FK to Client
    address_id CHAR(8) NOT NULL,-- FK to Address
    PRIMARY KEY(client, address_id),
    FOREIGN KEY(client) REFERENCES Client(email),
    FOREIGN KEY(address_id) REFERENCES Address(address_id)
);

-- Driver–Model qualification (0:N to 0:N)
CREATE TABLE IF NOT EXISTS Drives (
    driver TEXT NOT NULL,       -- FK to Driver
    model CHAR(8) NOT NULL,     -- FK to Model (by model_id)
    PRIMARY KEY(driver, model),
    FOREIGN KEY(driver) REFERENCES Driver(name),
    FOREIGN KEY(model) REFERENCES Model(model_id)
);

-- Rent links Client, Driver, and Model (all 1:1 on rent side, 0:N on others)
CREATE TABLE IF NOT EXISTS Rent (
    rent_id CHAR(8),            -- Rent identifier (Primary Key)
    date DATE NOT NULL,         -- Rent date (entire day)
    client TEXT NOT NULL,       -- FK to Client
    driver TEXT NOT NULL,       -- FK to Driver
    model CHAR(8) NOT NULL,     -- FK to Model (by model_id)
    PRIMARY KEY(rent_id),
    FOREIGN KEY(client) REFERENCES Client(email),
    FOREIGN KEY(driver) REFERENCES Driver(name),
    FOREIGN KEY(model) REFERENCES Model(model_id)
);
