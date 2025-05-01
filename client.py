## Contains all of the methods for client-specific actions

import dbTier
from datetime import datetime
import re

def increment_id(id):
    """Automatically increments the id by one so the client
      doesn't have to manually enter a new id for new rents and reviews"""
    if id[2].isalpha():
        prefix = id[:3]
        number = int(id[3:]) + 1
        new_id = f"{prefix}{number:05d}"
    else:
        prefix = id[0]
        number = int(id[1:]) + 1
        new_id = f"{prefix}{number:07d}"
    return new_id

def is_valid_date(date_str):
    """Checks that a date is valid
    
    Returns True if valid, false otherwise"""
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(date_pattern, date_str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_card(cc):
    return len(cc) == 16 and cc.isnumeric()

def get_address():
    """Prompts user for an address
    
    Returns tuple of strings (number, street, city)"""
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
    if not dbTier.insert_client(conn, email, name, commit=False):
        print("\nRegistration failed: client email already in use.")
        return

    print(f"\nClient {email} registered successfully.")

    one_addr = False
    one_cc = False

    print("\nNew client address registration:")
    # Prompt to add at least one address
    while True:
        print("   Enter Address Info")
        number, street, city = get_address()
        # Add address to Address table if it doesn't already exist
        dbTier.insert_address(conn, number, street, city, commit=False)
        # Add to client addresses
        if dbTier.insert_client_address(conn, email, number, street, city, commit=False):
            print(f"   Address {number} {street}, {city} added.")
            one_addr = True
        else:
            print("   Failed to add address. The Client is already registered to this address.")
            if not one_addr:
                continue # continue to make sure at least 1 address is valid
        next_addr = input("    Enter additional address (y/n)?")
        # Anything other than 'y' will break
        if next_addr.lower() != "y":
            break

    print("\nNew client payment registration:")
    # Prompt to add at least one credit card
    while True:
        cc = input("   Enter Credit Card Number: ")
        while not is_valid_card(cc):
            cc = input("   Invlalid card. Please try again: ")

        print("   Payment address:")
        number, street, city = get_address()
        # Add address to Address table if it doesn't already exist
        dbTier.insert_address(conn, number, street, city, commit=False)
        # Add to client addresses
        if dbTier.insert_credit_card(conn, cc, email, number, street, city, commit=False):
            print(f"\nCredit card {cc} added to your profile.")
            one_cc = True
        else:
            print("\n   Failed to add credit card. Card already in use.")
            if not one_cc:
                continue # continue to make sure at least 1 address is valid
        next_addr = input("    Enter additional credit card (y/n)?")
        # Anything other than 'y' will break
        if next_addr.lower() != "y":
            break


    # Only commit changes if at least 1 address and credit card have been added
    if one_addr and one_cc:
        print("\nSetup complete. You can now log in as a client.")
        conn.commit()
    ## If something went wrong and there is not at least 1 credit card and 1 address, discard changes
    else:
        print("\nClient setup failed. Discarding new client information.")
        conn.rollback()


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
                while not is_valid_card(cc):
                    cc = input("   Invlalid card. Please try again: ")
                print("   Enter payment address: ")
                number, street, city = get_address()
                dbTier.insert_address(conn, number, street, city)
                if dbTier.insert_credit_card(conn, cc, email, number, street, city):
                    print(f"\nCredit card {cc} added to your profile.")
                else:
                    print("\nFailed to add credit card. Card already in use")
            case '3':
                date = input("   Enter date (YYYY-MM-DD) to search available models: ")
                while not is_valid_date(date):
                    date = input("Invalid date. Please try again: ")

                models = dbTier.find_available_models(conn, date)
                print(f"\n{'Model ID':<10}{'Car ID':<10}{'Color':<10}{'Trans.':<10}{'Year':<6}")
                print('-' * 46)
                for mid, cid, color, trans, year in models:
                    print(f"{mid:<10}{cid:<10}{color:<10}{trans:<10}{year:<6}")
            case '4':
                # New: Automatically create new Rent_id
                rent_id = increment_id(dbTier.get_latest_rent_id(conn))

                date = input("   Enter rent date (YYYY-MM-DD): ")
                while not is_valid_date(date):
                    date = input("Invalid date. Please try again: ")

                model_id = input("   Enter model ID to book: ")

                if dbTier.book_rent(conn, rent_id, date, email, model_id):
                    print(f"\nRent {rent_id} successfully booked.")
                else:
                    print("\nFailed to book rent.")
            case '5':
                rents = dbTier.get_client_rents(conn, email)
                print(f"\n{'Rent ID':<10}{'Date':<12}{'Model':<10}{'Car':<10}{'Driver':<15}")
                print('-' * 57)
                for rid, date, mid, cid, color, trans, year, drv in rents:
                    # New: Have to cast data as a str to get it to print properly for some reason
                    print(f"{rid:<10}{str(date):<12}{mid:<10}{cid:<10}{drv:<15}")
            case '6':
                driver = input("   Enter driver name to review: ")

                # Check if client has reviewed this driver before, if so, ask if they'd like to update their review
                has_reviewed = dbTier.has_reviewed(conn, email, driver)
                if has_reviewed:
                    update = input("   You have already review this driver. Would you like to update your review (y/n)?")
                    if not update.lower() == 'y':
                        print("\nCancelling review.")
                        return

                # Prompt for message and rating
                message = input("   Enter review message: ")
                rating = input("   Enter rating (0-5): ")
                while not (rating.isnumeric() and int(rating) >= 0 and int(rating) <= 5):
                    rating = input("   Invalid rating. Try again: ")

                # Update or submit new review if 
                if has_reviewed:
                    successful = dbTier.update_review(conn, email, driver, message, rating)
                else:
                    review_id = increment_id(dbTier.get_latest_review_id(conn))       
                    successful = dbTier.insert_review(conn, review_id, email, driver, message, int(rating))
                
                if successful:
                    print("\nReview submitted successfully.")
                else:
                    print("\nFailed to submit review.")
            case 'x':
                print("\nLogging out client...")
            case _:
                print("Unknown command, please try again")
