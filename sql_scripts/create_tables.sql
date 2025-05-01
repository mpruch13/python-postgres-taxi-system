-- Relationships: none
CREATE TABLE IF NOT EXISTS Manager(
    ssn CHAR(9),
    email text,
    name text,
    PRIMARY KEY(ssn)
);


-- Relationships:
   -- Address: Handled with new table (Rule 5)
   -- CreditCard: Adding foreign key to CreditCard (Rule 4)
CREATE TABLE IF NOT EXISTS  Client(
    email text,
    name text,
    PRIMARY KEY(email)
);


-- Relationships:
   -- Client: Handled with new table (Rule 5)
   -- Driver: Added foreign key to Driver (Rule 4)
   -- CreditCard: Added foreign key to CreditCard (Rule 4)
   -- Rent: Added foreign key to Rent (Rule 4)
CREATE TABLE IF NOT EXISTS Address(
    number int,
    road text,
    city text,
    PRIMARY KEY(number, road, city)
);


-- Relationships:
   -- Address: Added foreign key here (Rule 4)
      -- 0:N so no need to enforce any bounds on the address side
   -- Review: Review is weak entity so relationship is handled when defining it
   -- Model: Handled with new table "Drives" (Rule 5)
   -- Works: Added foreign key to Rent (Rule 4)
CREATE TABLE IF NOT EXISTS Driver(
    name text,
    number int,
    road text,
    city text,
    PRIMARY KEY(name),
    FOREIGN KEY(number, road, city) REFERENCES Address(number, road, city)
);




-- Relationships: Rule 4 applies to both (0/1:N to 1:1)
   -- Address: Added foreign key here (Rule 4) (O:N to 1:1)
   -- Client: Added foreign key here (Rule 4)  (1:N to 1:1)
      -- Can enforce client requiring 1 credit card in the application
      --(e.g., make clients enter a credit card when they register)
CREATE TABLE IF NOT EXISTS CreditCard(
    cc_number CHAR(16),
    client text,
    addr_number int,
    road text,
    city text,
    PRIMARY KEY(cc_number),
    FOREIGN KEY(client) REFERENCES client(email),
    FOREIGN KEY(addr_number, road, city) REFERENCES Address(number, road, city)
);




-- Relationships:
   -- Model: Model is weak entity so this is handled when defining model
CREATE TABLE IF NOT EXISTS Car(
    car_id CHAR(8),
    brand text,
    PRIMARY KEY(car_id)
);


-- Relationships:
   -- Car: is the defining relationship for this weak entity
   -- Driver: Handled with new table "Drives" (Rule 5)
CREATE TABLE IF NOT EXISTS Model(
    model_id CHAR(8) UNIQUE,
    car_id CHAR(8),
    color text,
    transmission text,
    year int,
    PRIMARY KEY(model_id, car_id),
    FOREIGN KEY(car_id) REFERENCES Car(car_id)
    ON DELETE CASCADE -- delete all models with car id when car is deleted
);


-- Relationships: I think all follow Rule 4 (0:N to 1:1), so
-- we just need to add foreign keys here for each relationship
   -- Client: foreign key
   -- Driver: foreign key
   -- Model: foreign key
CREATE TABLE IF NOT EXISTS Rent(
    rent_id CHAR(8),
    date date,
    -- Relationship attributes
    client text,
    driver text,
    model CHAR(8),
    PRIMARY KEY(rent_id),
    FOREIGN KEY(client) REFERENCES Client(email),
    -- Delete rent records when the referenced driver/model is deleted
    FOREIGN KEY(driver) REFERENCES Driver(name)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(model) REFERENCES Model(model_id) ON DELETE CASCADE
);


-- Relationships:
   -- Driver: is defining relationship for this weak entity
   -- Client: Added foreign key to Client (Rule 4)
      -- Can enforce client only being allowed to write 1 review per Driver in 
      --the application.
   -- Rent: Added foreign key to Rent (Rule 4)
CREATE TABLE IF NOT EXISTS Review(
    review_id CHAR(8) UNIQUE,
	driver text,
	client text,
    message text,
    rating int,
    PRIMARY KEY(review_id, driver),
    FOREIGN KEY(driver) REFERENCES Driver(name) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(client) REFERENCES Client(email)
);


-- Relationship Tables


-- Relationship between Client and Address
-- Rule 5: Client--1:N--(Has)--0:N--Address
-- Client must have at least 1 address, but we can enforce this lower bound in the
   --application (e.g,. make clients enter at least 1 address when they register,
  -- then save that address in this table)
CREATE TABLE IF NOT EXISTS ClientAddresses(
    client text,
    number int,
    road text,
    city text,
    PRIMARY KEY(client, number, road, city),
    FOREIGN KEY(client) REFERENCES Client(email),
    FOREIGN KEY(number, road, city) REFERENCES Address(number, road, city)
);


-- Relationship between Driver and car Model
-- Rule 5: Driver--0:N--(qualified_for)--0:N--Model
   -- No need to enforce any lower bounds in the app since it's 0:N on both sides
CREATE TABLE IF NOT EXISTS Drives(
    driver text,
    model CHAR(8),
    PRIMARY KEY (driver,model),
    -- Delete drives entries when the referenced driver or model is deleted 
    FOREIGN KEY(driver) REFERENCES Driver(name) 
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY(model) REFERENCES Model(model_id) ON DELETE CASCADE
);
