## Contains all of the methods for driver-specific actions

import dbTier


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
                new_addr = input("   Enter new address ID: ")
                if dbTier.update_driver_address(conn, name, new_addr):
                    print(f"\nAddress updated to {new_addr}")
            case '2':
                models = dbTier.get_all_models(conn)
                print(f"\n{'Model ID':<10}{'Car ID':<10}{'Color':<10}{'Trans.':<10}{'Year':<6}")
                print('-' * 46)
                for mid, cid, color, trans, year in models:
                    print(f"{mid:<10}{cid:<10}{color:<10}{trans:<10}{year:<6}")
            case '3':
                model_id = input("   Enter model ID to declare: ")
                if dbTier.qualify_driver_for_model(conn, name, model_id):
                    print(f"\nDriver {name} now qualified for model {model_id}")
            case 'x':
                print("\nLogging out driver...")
            case _:
                print("Unknown command, please try again")
