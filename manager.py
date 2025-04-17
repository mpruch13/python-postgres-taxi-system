## Contains all of the methods for manager-specific actions

import psycopg2
import dbTier

def isvalid_ssn(ssn):
    """For input validation. Checks that an ssn is the correct format"""
    return (len(ssn) == 9 and ssn.isnumeric())


def display_models_rents(conn):
    """Generate and displays a list containing every car in the db
       model alongside the number of rents it has been used"""
    
    # dbTier returns list of tuples: (model_id, color, transmission, rent_count))
    models_rents = dbTier.get_models_rents(conn)
    # Print the list 
    max_width = 9
    print("\nCar models and total rents:")
    print(f"{'Model ID':>{max_width}}{'Color':>{max_width}}{'Year':>{max_width}}{'Transmission':>{max_width+5}}{'Rents':>{max_width}}")
    print('-' * (((max_width) * 5)+5))
    for model_id, color, year, transmission, rent_count in models_rents:
        print(f"{model_id:>{max_width}}{color:>{max_width}}{year:>{max_width}}{transmission:>{max_width+5}}{rent_count:>{max_width}}")
    print()


def add_model(conn):
    """Allows the user to enter a new car model into the database"""

    ## Prompt user for manager info 
    print("\nNew Car Model Registration:")

    # Repeat prompt until user enters a 9-digit number for ssn
    model_id = input("   Please enter an 8-character long model ID: ")
    while len(model_id) != 8:
        model_id = input("   Invalid id. Please enter exactly 8 characters, no spaces: ")
    color = input("   Please enter a model color: ")
    transmission = input("   Please enter a transmission type (0 for manual, 1 for automatic): ")
    while transmission != "0" and transmission != "1":
        transmission = input("   Invalid input. Enter 0 for manual, or 1 for automatic: ")
    if transmission == "0":
        transmission = 'manual'
    else:
        transmission = 'automatic'
    year = input("   Please enter a model year: ")
    car_id = input("    Please enter the car_id of the category/brand this model belongs to: ")

    # Attempt to insert manager into the database
    if(dbTier.insert_model(conn, model_id, color, transmission, year, car_id)):
        print("\nSuccessfully registered the new model")

def add_car(conn):
    """Allows the user to enter a new car table entry in the database"""

    ## Prompt user for manager info 
    print("\nNew Car Registration:")

    # Repeat prompt until user enters a 9-digit number for ssn
    car_id = input("   Please enter an 8-character long car ID: ")
    while len(car_id) != 8:
        car_id = input("   Invalid car id. Please enter an 8-character id: ")
    brand = input("   Please enter a brand name: ")

    # Attempt to insert manager into the database
    if(dbTier.insert_car(conn, car_id, brand)):
        print("\nSuccessfully registered new car with ID:", car_id, "and Brand:", brand)


def edit_cars(conn):
    user_input = ''
    while(user_input != 'x'):
    ## Print prompt
        print("\nCar management actions:")
        print("   1. Register new car category/brand\n"\
              "   2. Register new car model\n"
              "   3. Remove existing car models\n"\
              "   4. Remove car brand (will delete all models of that brand)\n"
              "   5. Return to manager menu\n")
        ## Get input
        user_input = input("\nEnter a command (1-5): ")
        match user_input:
            case "1":
                add_car(conn)
            case "2":
                add_model(conn)
            case "3":
                print()
            case "4":
                print()
            case "5":
                user_input = "x"
            case default:
                print("Unknown command, please try again") 


def manager_options(conn):
    user_input = ''
    while(user_input != 'x'):
        ## Print prompt
        print("Manager actions:")
        print("   1. Manage Cars\n" \
              "   2. Manage Drivers\n"
              "   3. List top clients\n" \
              "   4. List car information\n" \
              "   5. List driver information\n"
              "   6. Client/Driver city search") # idk what to call this option yet 
        ## Get input
        user_input = input("\nEnter a command (1-6, or x to log out): ")
        match user_input:
            case "1":
                edit_cars(conn)
            case "2":
                print("TODO: Implement adding/removing drivers and driver info\n")
            case "3":
                print("TODO: Implement top-k client list\n")
            case '4':
                display_models_rents(conn)
            case '5':
                print("TODO: Implement driver list\n")
            case '6':
                print("TODO: Implement client/driver city search thing\n")
            case'x':
                print("\nLogging out manager...")
                pass
            case default:
                print("Unknown command, please try again") 


def manager_login(conn):
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
        print("Login failed: Manager SSN not found")


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
        print("\nSuccessfully registered new manager:", name)
   