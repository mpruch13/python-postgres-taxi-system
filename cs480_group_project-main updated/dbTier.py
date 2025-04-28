## Contains all of the database queries 

# Querying the database with psycopg2:
# Get cursor object from the connection: curr = conn.cursor()
# Use execute() on cursor object to execute a query (takes 1 or 2 args):
#   First argument is the main query string e.g., "SELECT * FROM ..."
#   Second argument is a tuple of variables that will replace any placeholders in the string
# Use curr.fetchone() or curr.fetchall() after execute to get results of the query (fetchone returns 1 tuple with query results, fetchall() returns list of tuples)
# If inserting/deleting, use `conn.commit()` to save changes to the db
# call curr.close() when finished

import psycopg2

### Manager Options ###

def get_models_rents(conn:psycopg2.extensions.connection):
    """
    Gets a list of all car models alongside the number of times each
    has been rented.

    Parameters:
        conn: The database connection

    Returns: 
        A list of tuples. Each tuple takes the form: (model_id, color, year, transmission, rent_count)
    """
    dbQuery = """SELECT m.model_id, m.color, m.year, m.transmission,
                        COUNT(r.rent_id) AS rent_count
                 FROM Model m LEFT JOIN Rent r
                 ON m.model_id = r.model
                 GROUP BY m.model_id, m.color, m.year, m.transmission
                 ORDER BY rent_count DESC;
              """
    curr = conn.cursor()
    curr.execute(dbQuery)
    models = curr.fetchall()
    curr.close()
    return models

# New: Get top-k clients by number of rents
def get_top_k_clients(conn:psycopg2.extensions.connection, k):
    """
    Returns the top k clients along with their rent counts.

    Parameters:
        conn: The database connection
        k: Number of top clients to retrieve

    Returns:
        List of tuples: (email, name, rent_count)
    """
    dbQuery = """SELECT c.email, c.name, COUNT(r.rent_id) AS rent_count
                 FROM Client c JOIN Rent r ON c.email = r.client
                 GROUP BY c.email, c.name
                 ORDER BY rent_count DESC
                 LIMIT %s;"""
    curr = conn.cursor()
    curr.execute(dbQuery, (k,))
    results = curr.fetchall()
    curr.close()
    return results

# New: Get driver statistics (total rents and average rating)
def get_driver_stats(conn:psycopg2.extensions.connection):
    """
    Retrieves each driver with total number of rents and average rating.

    Parameters:
        conn: The database connection

    Returns:
        List of tuples: (name, total_rents, avg_rating)
    """
    dbQuery = """SELECT d.name,
                        COUNT(r.rent_id) AS total_rents,
                        COALESCE(ROUND(AVG(rv.rating)::numeric,2),0) AS avg_rating
                 FROM Driver d
                 LEFT JOIN Rent r ON d.name = r.driver
                 LEFT JOIN Review rv ON d.name = rv.driver
                 GROUP BY d.name
                 ORDER BY d.name;"""
    curr = conn.cursor()
    curr.execute(dbQuery)
    results = curr.fetchall()
    curr.close()
    return results

# New: Get clients with address in city1 and rents with drivers in city2
def get_clients_by_cities(conn:psycopg2.extensions.connection, city1, city2):
    """
    Retrieves clients who have at least one address in city1
    and have booked a rent with a driver whose address is in city2.

    Parameters:
        conn: The database connection
        city1: Client address city filter
        city2: Driver address city filter

    Returns:
        List of tuples: (email, name)
    """
    dbQuery = """SELECT DISTINCT c.email, c.name
                 FROM Client c
                 JOIN ClientAddresses ca ON c.email = ca.client
                 JOIN Address a1 ON ca.address_id = a1.address_id
                 JOIN Rent r ON c.email = r.client
                 JOIN Driver d ON r.driver = d.name
                 JOIN Address a2 ON d.address_id = a2.address_id
                 WHERE a1.city = %s AND a2.city = %s;"""
    curr = conn.cursor()
    curr.execute(dbQuery, (city1, city2))
    results = curr.fetchall()
    curr.close()
    return results

### Driver Options ###

def insert_driver(conn:psycopg2.extensions.connection, name, address_id):
    """
    Inserts a new driver into the database.
    Prints an error message if insertion fails.

    Parameters:
        conn: The database connection
        name: Driver name (Primary Key)
        address_id: Address identifier FK

    Returns:
        True if insertion successful, False otherwise
    """
    is_successful = False
    dbQuery = "INSERT INTO Driver (name, address_id) VALUES (%s, %s)"
    curr = conn.cursor()
    try:
        curr.execute(dbQuery, (name, address_id))
        conn.commit()
        is_successful = True
    except Exception as e:
        print("\nFailed to add new driver: ", e)
    finally:
        curr.close()
    return is_successful


def delete_driver(conn:psycopg2.extensions.connection, name):
    """
    Deletes a driver by name.

    Parameters:
        conn: The database connection
        name: Driver name to delete

    Returns:
        True if deletion successful, False otherwise
    """
    is_successful = False
    dbQuery = "DELETE FROM Driver WHERE name = %s"
    curr = conn.cursor()
    try:
        curr.execute(dbQuery, (name,))
        conn.commit()
        is_successful = True
    except Exception as e:
        print("\nFailed to delete driver: ", e)
    finally:
        curr.close()
    return is_successful


def update_driver_address(conn:psycopg2.extensions.connection, name, new_address_id):
    """
    Updates a driver's address.

    Parameters:
        conn: The database connection
        name: Driver name
        new_address_id: New address identifier

    Returns:
        True if update successful, False otherwise
    """
    is_successful = False
    dbQuery = "UPDATE Driver SET address_id = %s WHERE name = %s"
    curr = conn.cursor()
    try:
        curr.execute(dbQuery, (new_address_id, name))
        conn.commit()
        is_successful = True
    except Exception as e:
        print("\nFailed to update driver address: ", e)
    finally:
        curr.close()
    return is_successful


def get_all_models(conn:psycopg2.extensions.connection):
    """
    Retrieves all car models in the system.

    Parameters:
        conn: The database connection

    Returns:
        List of tuples: (model_id, car_id, color, transmission, year)
    """
    dbQuery = "SELECT model_id, car_id, color, transmission, year FROM Model ORDER BY model_id"
    curr = conn.cursor()
    curr.execute(dbQuery)
    models = curr.fetchall()
    curr.close()
    return models


def qualify_driver_for_model(conn:psycopg2.extensions.connection, name, model_id):
    """
    Qualifies a driver for a specific model.

    Parameters:
        conn: The database connection
        name: Driver name
        model_id: Model identifier

    Returns:
        True if insertion successful, False otherwise
    """
    is_successful = False
    dbQuery = "INSERT INTO Drives (driver, model) VALUES (%s, %s)"
    curr = conn.cursor()
    try:
        curr.execute(dbQuery, (name, model_id))
        conn.commit()
        is_successful = True
    except Exception as e:
        print("\nFailed to qualify driver for model: ", e)
    finally:
        curr.close()
    return is_successful

### Client Options ###

def insert_client(conn:psycopg2.extensions.connection, email, name):
    """
    Inserts a new client into the database.

    Parameters:
        conn: The database connection
        email: Client email (Primary Key)
        name: Client name

    Returns:
        True if insertion successful, False otherwise
    """
    is_successful = False
    dbQuery = "INSERT INTO Client (email, name) VALUES (%s, %s)"
    curr = conn.cursor()
    try:
        curr.execute(dbQuery, (email, name))
        conn.commit()
        is_successful = True
    except Exception as e:
        print("\nFailed to add client: ", e)
    finally:
        curr.close()
    return is_successful


def insert_client_address(conn:psycopg2.extensions.connection, email, address_id):
    """
    Associates a client with an address.

    Parameters:
        conn: The database connection
        email: Client email
        address_id: Address identifier

    Returns:
        True if insertion successful, False otherwise
    """
    is_successful = False
    dbQuery = "INSERT INTO ClientAddresses (client, address_id) VALUES (%s, %s)"
    curr = conn.cursor()
    try:
        curr.execute(dbQuery, (email, address_id))
        conn.commit()
        is_successful = True
    except Exception as e:
        print("\nFailed to add client address: ", e)
    finally:
        curr.close()
    return is_successful


def insert_credit_card(conn:psycopg2.extensions.connection, number, email, payment_address):
    """
    Inserts a new credit card for a client.

    Parameters:
        conn: The database connection
        number: Credit card number
        email: Client email
        payment_address: Address identifier for payment

    Returns:
        True if insertion successful, False otherwise
    """
    is_successful = False
    dbQuery = "INSERT INTO CreditCard (number, client, payment_address) VALUES (%s, %s, %s)"
    curr = conn.cursor()
    try:
        curr.execute(dbQuery, (number, email, payment_address))
        conn.commit()
        is_successful = True
    except Exception as e:
        print("\nFailed to add credit card: ", e)
    finally:
        curr.close()
    return is_successful

# New: Find available models for a given date
def find_available_models(conn:psycopg2.extensions.connection, date):
    """
    Retrieves all models available on a specific date.
    A model is available if:
      1) It is not rented on that date.
      2) There exists at least one qualified driver not booked that date.

    Parameters:
        conn: The database connection
        date: date to check availability

    Returns:
        List of tuples: (model_id, car_id, color, transmission, year)
    """
    dbQuery = """
        SELECT DISTINCT m.model_id, m.car_id, m.color, m.transmission, m.year
        FROM Model m
        WHERE m.model_id NOT IN (
            SELECT r.model FROM Rent r WHERE r.date = %s
        )
        AND EXISTS (
            SELECT 1 FROM Drives d
            LEFT JOIN Rent r2 ON d.driver = r2.driver AND r2.date = %s
            WHERE d.model = m.model_id AND r2.rent_id IS NULL
        )
        ORDER BY m.model_id;
    """
    curr = conn.cursor()
    curr.execute(dbQuery, (date, date))
    models = curr.fetchall()
    curr.close()
    return models

# New: Book a rent, auto-assigning an available driver
def book_rent(conn:psycopg2.extensions.connection, rent_id, date, client, model_id):
    """
    Books a new rent for a client and model on a given date.
    Automatically assigns the first available driver qualified for the model.

    Parameters:
        conn: The database connection
        rent_id: New rent identifier
        date: Rent date
        client: Client email
        model_id: Model identifier

    Returns:
        True if booking successful, False otherwise
    """
    curr = conn.cursor()
    # Find an available driver for the model on that date
    driver_query = """
        SELECT d.driver
        FROM Drives d
        LEFT JOIN Rent r ON d.driver = r.driver AND r.date = %s
        WHERE d.model = %s AND r.rent_id IS NULL
        LIMIT 1;
    """
    curr.execute(driver_query, (date, model_id))
    row = curr.fetchone()
    if not row:
        print("\nNo available driver for model on this date.")
        curr.close()
        return False
    driver = row[0]

    # Insert the new rent
    insert_query = "INSERT INTO Rent (rent_id, date, client, driver, model) VALUES (%s, %s, %s, %s, %s)"
    try:
        curr.execute(insert_query, (rent_id, date, client, driver, model_id))
        conn.commit()
    except Exception as e:
        print("\nFailed to book rent: ", e)
        curr.close()
        return False

    curr.close()
    return True

# New: Get a client's rent history
def get_client_rents(conn:psycopg2.extensions.connection, client):
    """
    Retrieves all rents booked by a given client.

    Parameters:
        conn: The database connection
        client: Client email

    Returns:
        List of tuples: (rent_id, date, model_id, car_id, color, transmission, year, driver)
    """
    dbQuery = """
        SELECT r.rent_id, r.date, m.model_id, m.car_id, m.color, m.transmission, m.year, r.driver
        FROM Rent r
        JOIN Model m ON r.model = m.model_id
        WHERE r.client = %s
        ORDER BY r.date;
    """
    curr = conn.cursor()
    curr.execute(dbQuery, (client,))
    rents = curr.fetchall()
    curr.close()
    return rents

# New: Insert a review if client has rented from that driver
def insert_review(conn:psycopg2.extensions.connection, review_id, client, driver, message, rating):
    """
    Inserts a review for a driver by a client, only if the client has a prior rent with that driver.

    Parameters:
        conn: The database connection
        review_id: New review identifier
        client: Client email
        driver: Driver name
        message: Review message
        rating: Integer rating (0-5)

    Returns:
        True if insertion successful, False otherwise
    """
    curr = conn.cursor()
    # Verify the client-driver rent relationship
    check_query = "SELECT 1 FROM Rent WHERE client = %s AND driver = %s LIMIT 1"
    curr.execute(check_query, (client, driver))
    if not curr.fetchone():
        print("\nCannot review: no rent found between client and driver.")
        curr.close()
        return False

    insert_query = "INSERT INTO Review (review_id, driver, client, message, rating) VALUES (%s, %s, %s, %s, %s)"
    try:
        curr.execute(insert_query, (review_id, driver, client, message, rating))
        conn.commit()
    except Exception as e:
        print("\nFailed to add review: ", e)
        curr.close()
        return False

    curr.close()
    return True
