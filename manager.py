## Contains all of the methods for manager-specific actions

import dbTier

def get_address():
    print("   Enter Address Info")
    number = input("     Number: ")
    while not number.isnumeric():
        number = input("     Invalid address number. Try again: ")
    street  = input("     Enter Street: ")
    city = input("     Enter City:")
    return number, street, city

def isvalid_ssn(ssn):
    """For input validation. Checks that an ssn is the correct format"""
    return (len(ssn) == 9 and ssn.isnumeric())


def display_models_rents(conn):
    """Generate and displays a list containing every car in the db
       model alongside the number of rents it has been used"""
    
    # dbTier returns list of tuples: (modle_id, car_id, color, transmission, rent_count))
    models_rents = dbTier.get_models_rents(conn)
    # Print the list 
    max_width = 9
    print("\nCar models and total rents:")
    print(f"{'Car ID':>{max_width}}{'Model ID':>{max_width+3}}{'Color':>{max_width}}{'Year':>{max_width}}{'Transmission':>{max_width+5}}{'Rents':>{max_width}}")
    print('-' * (((max_width) * 6)+8))
    for model_id, car_id, color, year, transmission, rent_count in models_rents:
        print(f"{model_id:>{max_width}}{car_id:>{max_width+3}}{color:>{max_width}}{year:>{max_width}}{transmission:>{max_width+5}}{rent_count:>{max_width}}")
    print()


def add_model(conn):
    """Allows the user to enter a new car model into the database"""

    ## Prompt user for manager info 
    print("\nNew Car Model Registration:")

    # Prompt User for existing Car ID
    car_id = input("   Enter an existing car ID: ")
    while len(car_id) != 8 and dbTier.get_car(conn, car_id) == None:
        if car_id.lower() == "x":
            return
        car_id = input("   Car ID is invalid or does not exist. Try again: ")

    # Prompt user for new Model ID
    model_id = input("   Enter an 8-character long model ID: ")
    while len(model_id) != 8:
        model_id = input("   Invalid id. Please enter exactly 8 characters, no spaces: ")

    # Prompt for color
    color = input("   Please enter a model color: ")

    # Prompt for Transmission
    transmission = input("   Please enter a transmission type (0 for manual, 1 for automatic): ")
    while transmission not in ("0", "1"):
        transmission = input("   Invalid input. Enter 0 for manual, or 1 for automatic: ")
    transmission = 'manual' if transmission == '0' else 'automatic'

    ## Prompt for Year
    year = input("   Please enter a model year: ")

    # Attempt to insert model into the database
    if(dbTier.insert_model(conn, model_id, color, transmission, year, car_id)):
        print("\nSuccessfully registered the new model")


def add_car(conn):
    """Allows the user to enter a new car table entry in the database"""

    ## Prompt user for manager info 
    print("\nNew Car Registration:")

    # Repeat prompt until user enters a valid 8-character ID
    car_id = input("   Please enter an 8-character long car ID: ")
    while len(car_id) != 8:
        car_id = input("   Invalid car id. Please enter an 8-character id: ")
    brand = input("   Please enter a brand name: ")

    # Attempt to insert car into the database
    if(dbTier.insert_car(conn, car_id, brand)):
        print("\nSuccessfully registered new car with ID:", car_id, "and Brand:", brand)


def add_driver(conn):
    """Allows the user to enter a new driver into the database.
    Automatically adds the driver's address to the address table if it does not
    already exist."""

    print("\nRegister New Driver:")
    name = input("   Enter driver name: ")
    number, street, city  = get_address()


    ## Attempt to insert address into table
    # Insert address is safe to call even if address already exits. It will just return false in that case.
    dbTier.insert_address(conn, number, street, city)

    if dbTier.insert_driver(conn, name, number, street, city):
        print(f"\nSuccessfully added driver {name}")
    else:
        print(f"\nFailed to add driver. Driver \"{name}\" already exists.")


def edit_cars(conn):
    """Sub-menu for managing cars and models"""
    user_input = ''
    while(user_input != 'x'):
        print("\nCar management actions:")
        print("   1. Register new car category/brand\n"\
              "   2. Register new car model\n"\
              "   3. Remove existing car model\n"\
              "   4. Remove car brand (will delete all models of that brand)\n"\
              "   5. Return to manager menu\n")
        user_input = input("\nEnter a command (1-5): ")
        match user_input:
            case "1":
                add_car(conn)
            case "2":
                add_model(conn)
            case "3":
                # Remove a car model
                model_id = input("   Enter the model_id to remove: ")
                ##removal validation
                confirm = input(f"   Are you sure you want to delete model {model_id}? (y/n): ")
                if confirm.lower() == 'y':
                    curr = conn.cursor()
                    try:
                        curr.execute("DELETE FROM Model WHERE model_id = %s", (model_id,))
                        conn.commit()
                        print(f"\nSuccessfully removed model {model_id}")
                    except Exception as e:
                        print("\nFailed to remove model: ", e)
                    finally:
                        curr.close()
                else:
                    print("Deletion cancelled.")
            case "4":
                # Remove a car and its models
                car_id = input("   Enter the car_id to remove: ")
                ##removal validation
                confirm = input(f"   Are you sure you want to delete car {car_id} and its models? (y/n): ")
                if confirm.lower() == 'y':
                    curr = conn.cursor()
                    try:
                        curr.execute("DELETE FROM Car WHERE car_id = %s", (car_id,))
                        conn.commit()
                        print(f"\nSuccessfully removed car {car_id} and its models")
                    except Exception as e:
                        print("\nFailed to remove car: ", e)
                    finally:
                        curr.close()
                else:
                    print("Deletion cancelled")
            case "5":
                user_input = 'x'
            case _:
                print("Unknown command, please try again")


def manage_drivers(conn):
    """Sub-menu for managing driver records"""
    user_input = ''
    while(user_input != 'x'):
        print("\nDriver management actions:")
        print("   1. Register new driver")
        print("   2. Remove existing driver")
        print("   3. Return to manager menu")
        user_input = input("Enter a command (1-3): ")
        match user_input:
            case "1":
                add_driver(conn)
            case "2":
                print("\nRemove Driver:")
                name = input("   Enter driver name to remove: ")
                ##added confirmation
                confirm = input(f"   Are you sure you want to delete driver {name}? (y/n): ")
                if confirm.lower() == 'y':
                    if dbTier.delete_driver(conn, name):
                        print(f"\nSuccessfully removed driver {name}")
                else:
                    print("Deletion Cancelled.")
            case "3":
                user_input = 'x'
            case _:
                print("Unknown command, please try again")


def manager_options(conn):
    """Main manager menu routing to specific actions"""
    user_input = ''
    while(user_input != 'x'):
        print("Manager actions:")
        print("   1. Manage Cars\n"\
              "   2. Manage Drivers\n"\
              "   3. List top clients\n"\
              "   4. List car information\n"\
              "   5. List driver information\n"\
              "   6. Client/Driver city search")
        user_input = input("\nEnter a command (1-6, or x to log out): ")
        match user_input:
            case "1":
                edit_cars(conn)
            case "2":
                manage_drivers(conn)
            case "3":
                # List top-k clients
                print("\nTop-k Clients:")
                k = input("   Enter value for k: ")
                while not k.isdigit():
                    k = input("   Invalid. Enter a numeric value for k: ")
                clients = dbTier.get_top_k_clients(conn, int(k))
                print(f"\n{'Email':<30}{'Name':<20}{'Rents':<6}")
                print("-" * 56)
                for email, name, count in clients:
                    print(f"{email:<30}{name:<20}{count:<6}")
                print()
            case "4":
                display_models_rents(conn)
            case "5":
                # List driver stats
                print("\nDriver Information (Total Rents, Avg Rating):")
                stats = dbTier.get_driver_stats(conn)
                print(f"\n{'Name':<20}{'Total Rents':<12}{'Avg Rating':<10}")
                print("-" * 42)
                for name, total, avg in stats:
                    print(f"{name:<20}{total:<12}{avg:<10.2f}")
                print()
            case "6":
                # Client/Driver city search
                print("\nClient/Driver City Search:")
                city1 = input("   Enter client city: ")
                city2 = input("   Enter driver city: ")
                results = dbTier.get_clients_by_cities(conn, city1, city2)
                print(f"\n{'Email':<30}{'Name':<20}")
                print("-" * 50)
                for email, name in results:
                    print(f"{email:<30}{name:<20}")
                print()
            case 'x':
                print("\nLogging out manager...")
            case _:
                print("Unknown command, please try again")


def manager_login(conn):
    """Handles manager authentication and entry to manager menu"""
    print("\nManager Login:")

    ssn = input("   Please enter your SSN: ")
    while not isvalid_ssn(ssn):
        ssn = input("   Invalid SSN. Please enter a 9-digit number: ")

    # Tuple of format: (ssn, email, name) or None if manager does not exist
    manager = dbTier.get_manager(conn, ssn)

    if manager != None:
        print(f"\nWelcome {manager[2]}. Please select an action:")
        manager_options(conn)
    else:
        print("\nLogin failed: Manager SSN not found")


def register_manager(conn):
    """Allows the user to register a new manager in the database"""

    ## Prompt user for manager info 
    print("\nManager Registration:")

    name  = input("   Enter a manager name: ")
    email = input("   Enter a manager email: ")

    # Repeat prompt until user enters a 9-digit number for ssn
    ssn = input("   Enter a 9-digit social security number: ")
    while not isvalid_ssn(ssn):
        ssn = input("   Invalid ssn. Please enter a 9-digit number: ")

    # Attempt to insert manager into the database
    if(dbTier.insert_manager(conn, ssn, email, name)):
        print(f"\nSuccessfully registered new manager: {name}")
