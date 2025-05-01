-- Final SQL file for creating project database tables.

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
   address_id CHAR(8),
   number int,
   road text,
   city text,
   UNIQUE(number, road, city),
   PRIMARY KEY(address_id)
);

-- Relationships:
  -- Address: Added foreign key here (Rule 4)
     -- 0:N so no need to enforce any bounds on the address side
  -- Review: Review is weak entity so relationship is handled when defining it
  -- Model: Handled with new table "Drives" (Rule 5)
  -- Works: Added foreign key to Rent (Rule 4)
CREATE TABLE IF NOT EXISTS Driver(
   name text,
   address_id CHAR(8),
   PRIMARY KEY(name),
   FOREIGN KEY(address_id) REFERENCES Address(address_id)
);

-- Relationships: Rule 4 applies to both (0/1:N to 1:1)
  -- Address: Added foreign key here (Rule 4) (O:N to 1:1)
  -- Client: Added foreign key here (Rule 4)  (1:N to 1:1)
     -- Can enforce client requiring 1 credit card in the application
     --(e.g., make clients enter a credit card when they register)
CREATE TABLE IF NOT EXISTS CreditCard(
   number CHAR(16),
   payment_address CHAR(8),
   client text,
   PRIMARY KEY(number),
   FOREIGN KEY(payment_address) REFERENCES Address(address_id),
   FOREIGN KEY(client) REFERENCES Client(email)
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
   color text,
   transmission text,
   year int,
   car_id CHAR(8),
   PRIMARY KEY(model_id, car_id),
   FOREIGN KEY(car_id) REFERENCES Car(car_id)
);

-- All follow Rule 4 (0:N to 1:1), so
-- we just need to add foreign keys here for each relationship
  -- Client: foreign key
  -- Driver: foreign key
  -- Model: foreign key
CREATE TABLE IF NOT EXISTS Rent(
   rent_id CHAR(8),
   date date,
   client text,
   driver text,
   model CHAR(8),
   PRIMARY KEY(rent_id),
   FOREIGN KEY(client) REFERENCES Client(email),
   FOREIGN KEY(driver) REFERENCES Driver(name),
   FOREIGN KEY(model) REFERENCES Model(model_id)
);

-- Relationships:
  -- Driver: is defining relationship for this weak entity
  -- Client: Added foreign key to Client (Rule 4)
     -- enforce client writing one review per driver with unique constraint
CREATE TABLE IF NOT EXISTS Review(
   review_id CHAR(8) UNIQUE,
   message text,
   rating int,
   driver text,
   client text,
   PRIMARY KEY(review_id, driver),
   UNIQUE(client,driver),
   FOREIGN KEY(driver) REFERENCES Driver(name),
   FOREIGN KEY(client) REFERENCES Client(email)
);

-- Relationship Tables --

-- Relationship between Client and Address
-- Rule 5: Client--1:N--(Has)--0:N--Address
-- Client must have at least 1 address, but we can enforce this lower bound in the
  --application (e.g,. make clients enter at least 1 address when they register,
 -- then save that address in this table)
CREATE TABLE IF NOT EXISTS ClientAddresses(
   client text,
   address_id CHAR(8),
   PRIMARY KEY(client, address_id),
   FOREIGN KEY(client) REFERENCES Client(email),
   FOREIGN KEY(address_id) REFERENCES Address(address_id)
);

-- Relationship between Driver and car Model
-- Rule 5: Driver--0:N--(qualified_for)--0:N--Model
  -- No need to enforce any lower bounds in the app since it's 0:N on both sides
CREATE TABLE IF NOT EXISTS Drives(
   driver text,
   model CHAR(8),
   PRIMARY KEY (driver,model),
   FOREIGN KEY(driver) REFERENCES driver(name),
   FOREIGN KEY(model) REFERENCES Model(model_id)
);
