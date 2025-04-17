## Contains all of the database queries 

# Querying the database with psycopg2:
# Get cursor object from the connection: curr = conn.cursor()
# Use execute() on cursor object to execute a query (takes 1 or 2 args):
    # First argument is the main query string e.g., "SELECT * FROM ..."
    # Second argument is a tuple of variables that will replace any placeholers in the string
# Use curr.fetchone() or curr.fetchall() after execute to get results of the query (fetchone returns 1 tuple with query results, fetchall() returns list of tuples)
# If inserting/deleting, use `conn.commit() to save changes to the db
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
                        COUNT(rent_id) AS rent_count
                 FROM Model m LEFT JOIN Rent r
                 ON m.model_id = r.model
                 GROUP BY m.model_id, m.color, m.year, m.transmission
                 ORDER BY rent_count DESC;
              """
    curr = conn.cursor()
    curr.execute(dbQuery)
    # returns list of tuples [(model_id, color, transmission, count(rents)), ...)]
    models = curr.fetchall()
    curr.close()
    return models

def insert_model(conn:psycopg2.extensions.connection, model_id, color, transmission, year, car_id):
    """
    Inserts a new car model entry into the database.
    Prints an error message if the insert fails.

    Parameters:
        car_id: An 8 digit primary key
        brand: The brand name of the car
    Returns: 
        True if insertion was successful, False if not.
    """
    is_successful = False
    dbQuery = "INSERT INTO Model VALUES(%s, %s, %s, %s, %s)"
    curr = conn.cursor()
    try:
        curr.execute(dbQuery, (model_id, color, transmission, year, car_id))
        conn.commit()
        is_successful = True
    except Exception as e:
        print("\nFailed to add new model: ", e)
    finally:
        curr.close()
    return is_successful

def insert_car(conn:psycopg2.extensions.connection, car_id, brand):
    """
    Inserts a new car model entry into the database.
    Prints an error message if the insert fails.

    Parameters:
        car_id: An 8 digit primary key
        brand: The brand name of the car

    Returns:
        Bool: True if insertion was successful, False if not
    """
    is_successful = False
    dbQuery = "INSERT INTO Car VALUES(%s, %s)"
    curr = conn.cursor()
    try:
        curr.execute(dbQuery, (car_id, brand))
        conn.commit()
        is_successful = True
    except Exception as e:
        print("\nFailed to add new car: ", e)
    finally:
        curr.close()

    return is_successful

# For manager registration
def insert_manager(conn:psycopg2.extensions.connection, ssn, email, name):
    """
    Inserts a new manager entry in the database.
    Prints an error message if the insert fails.

    Parameters:
        ssn: The new manager's social security number (primary key)
        email: The manager's email address
        name: The new manager's name

    Returns: 
        Bool: True if insertion was successful, False if not
    """
    is_successful = False
    dbQuery = "INSERT INTO Manager VALUES(%s, %s, %s)"
    curr = conn.cursor()
    try:
        curr.execute(dbQuery, (ssn, email, name))
        conn.commit()
        is_successful = True
    except Exception as e:
        print("\nFailed to add manager to database: ", e)
    finally:
        curr.close()

    return is_successful

# For logging in a manager
def get_manager(conn:psycopg2.extensions.connection, ssn):
    """
    Searches the database for a manager with a matching ssn.

    Parameters:
        conn: The database connection
        ssn: A 9-digit social security number

    Returns:
        Manager(tuple): A tuple containing manager info (ssn, email, name),
        or None if no match was found.
    """
    dbQuery = """SELECT * FROM Manager
                 WHERE ssn = %s"""
    curr = conn.cursor()
    curr.execute(dbQuery, (ssn,))
    manager = curr.fetchone()
    curr.close()
    return manager

### Driver Options ###




### Client Options ###

