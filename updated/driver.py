## Contains all of the methods for driver-specific actions

import dbTier

def get_address():
    print("   Enter Address Info")
    number = input("     Number: ")
    while not number.isnumeric():
        number = input("     Invalid address number. Try again: ")

    road = input("     Street: ")
    city = input("     City: ")
    return number, road, city

def driver_login(conn):
    """Handles driver authentication and entry to driver menu"""
    print("\nDriver Login:")
    name = input("   Please enter your driver name: ")

    # Validate driver exists
    driver = dbTier.get_driver(conn, name)
    if driver is None:
        print("\nLogin failed: Driver not found")
        return
    
    print(f"\nWelcome {name}. Please select an action:")
    driver_menu(conn, name)

def qualify_driver(conn, name):
    model_id = input("   Enter model ID to declare: ")
    while len(model_id) != 8:
        if model_id.lower() == 'x':
            print("\nCancelling driver update...")
            return
        model_id = input("     Invlaid Model ID (must be 8 characters). Try again: ")
    # Print message based on result
    qualifies_return = dbTier.qualify_driver_for_model(conn, name, model_id)
    if qualifies_return == 0:
        print(f"\nDriver {name} now qualified for model {model_id}")
    elif qualifies_return == 1:
        print("\nDeclaration Failed: Driver already drives model")
    elif qualifies_return == 2:
        print(f"\nDeclaration failed: Model ID may not exist.")

def driver_menu(conn, name):
    """Sub-menu for driver operations"""
    user_input = ''
    while user_input != 'x':
        print("\nDriver actions:")
        print("   1. Change my address")
        print("   2. List all car models")
        print("   3. Declare I can drive a model")
        print("   x. Log out")

        user_input = input("Enter a command (1-3, or x to log out): ")
        match user_input:
            case '1':
                number, street, city = get_address()

                # Insert address to Address table if it does not exist
                dbTier.insert_address(conn, number, street, city)
                # Update Address in Driver table
                if dbTier.update_driver_address(conn, name, number, street, city):
                    print(f"\nAddress updated to {number} {street}, {city}")
                ## validation
                else:
                    print(f"\nFailed to update Address.")
            case '2':
                models = dbTier.get_all_models(conn)
                print(f"\n{'Model ID':<10}{'Car ID':<10}{'Color':<10}{'Trans.':<10}{'Year':<6}")
                print('-' * 46)
                for mid, cid, color, trans, year in models:
                    print(f"{mid:<10}{cid:<10}{color:<10}{trans:<10}{year:<6}")
            case '3':
                qualify_driver(conn, name)
            case 'x':
                print("\nLogging out driver...")
            case _:
                print("Unknown command, please try again")
