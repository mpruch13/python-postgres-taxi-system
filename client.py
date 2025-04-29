## Contains all of the methods for client-specific actions

import dbTier

def get_address():
    number = input("     Number: ")
    while not number.isnumeric():
        number = input("     Invalid address number. Try again: ")

    road = input("     Street: ")
    city = input("     City: ")
    return number, road, city

def register_client(conn):
    """Handles new client registration and initial address/card setup"""
    print("\nClient Registration:")
    email = input("   Enter your email: ")
    name  = input("   Enter your name: ")

    # Insert client record
    if not dbTier.insert_client(conn, email, name):
        print("\nRegistration failed: could not add client.")
        return

    print(f"\nClient {email} registered successfully.")

    # Prompt to add at least one address
    while True:
        print("   Enter Address Info")
        number, street, city = get_address()
        # Add address to Address table if it doesn't already exist
        dbTier.insert_address(conn, number, street, city)
        # Add to client addresses
        if dbTier.insert_client_address(conn, email, number, street, city):
            print(f"   Address {number} {street}, {city} added.")
        else:
            print("   Failed to add address. Client already registerd to address")
            continue # continue to make sure at least 1 address is valid
        next_addr = input("    Enter additional address (y/n)?")
        # Anything other than 'y' will just continue
        if next_addr.lower() != "y":
            break

    # Prompt to add at least one credit card
    while True:
        cc = input("   Enter a credit card number (or 'done' to finish): ")
        if cc.lower() == 'done':
            break
        print("   Enter payment address: ")
        number, street, city = get_address()
        dbTier.insert_address(conn, number, street, city)
        if dbTier.insert_credit_card(conn, cc, email, number, street, city):
            print(f"\nCredit card {cc} added to your profile.")
        else:
            print("\nFailed to add credit card. Card already in use")

    print("\nSetup complete. You can now log in as a client.")


def client_login(conn):
    """Handles client authentication and entry to client menu"""
    print("\nClient Login:")
    email = input("   Please enter your email: ")

    # Validate client exists
    client = dbTier.get_client(conn, email)
    if client is None:
        print("\nLogin failed: Client not found.")
        return

    print(f"\nWelcome {client[1]}! Please select an action:")
    client_menu(conn, email)


def client_menu(conn, email):
    """Sub-menu for client operations"""
    user_input = ''
    while user_input != 'x':
        print("\nClient actions:")
        print("   1. Add address")
        print("   2. Add credit card")
        print("   3. Search available models by date")
        print("   4. Book a rent")
        print("   5. View my rents")
        print("   6. Post a review")
        print("   x. Log out")

        user_input = input("Enter a command (1-6, or x to log out): ")
        match user_input:
            case '1':
                number, street, city = get_address()
                dbTier.insert_address(conn, number, street, city)
                if dbTier.insert_client_address(conn, email, number, street, city):
                    print(f"\nAddress {number} {street}, {city} added to your profile.")
                else:
                    print("   Failed to add address. Client already registerd to address")
            case '2':
                cc = input("   Enter credit card number: ")
                print("   Enter payment address: ")
                number, street, city = get_address()
                dbTier.insert_address(conn, number, street, city)
                if dbTier.insert_credit_card(conn, cc, email, number, street, city):
                    print(f"\nCredit card {cc} added to your profile.")
                else:
                    print("\nFailed to add credit card. Card already in use")
            case '3':
                date = input("   Enter date (YYYY-MM-DD) to search available models: ")
                models = dbTier.find_available_models(conn, date)
                print(f"\n{'Model ID':<10}{'Car ID':<10}{'Color':<10}{'Trans.':<10}{'Year':<6}")
                print('-' * 46)
                for mid, cid, color, trans, year in models:
                    print(f"{mid:<10}{cid:<10}{color:<10}{trans:<10}{year:<6}")
            case '4':
                rent_id = input("   Enter new rent ID: ")
                date = input("   Enter rent date (YYYY-MM-DD): ")
                model_id = input("   Enter model ID to book: ")
                if dbTier.book_rent(conn, rent_id, date, email, model_id):
                    print(f"\nRent {rent_id} successfully booked.")
                else:
                    print("\nFailed to book rent.")
            case '5':
                rents = dbTier.get_client_rents(conn, email)
                print(f"\n{'Rent ID':<10}{'Date':<12}{'Model':<10}{'Car':<10}{'Driver':<15}")
                print('-' * 57)
                for rid, d, mid, cid, color, trans, year, drv in rents:
                    print(f"{rid:<10}{d:<12}{mid:<10}{cid:<10}{drv:<15}")
            case '6':
                review_id = input("   Enter new review ID: ")
                driver = input("   Enter driver name to review: ")
                message = input("   Enter review message: ")
                rating = input("   Enter rating (0-5): ")
                if dbTier.insert_review(conn, review_id, email, driver, message, int(rating)):
                    print("\nReview submitted successfully.")
                else:
                    print("\nFailed to submit review.")
            case 'x':
                print("\nLogging out client...")
            case _:
                print("Unknown command, please try again")
