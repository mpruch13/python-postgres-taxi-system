## Initializes the database connection and runs the main menu loop

import psycopg2
import manager
import driver
import client
import re
import sys


def open_db():
    """Reads database info from file "dbinfo.txt" and attempts to open a new database connection"""
    with open("dbinfo.txt") as input_file:
        try:
            input_text = input_file.read()
        except Exception as e:
            print("Could not get db info from file:", e)
            sys.exit()

    # Process file text and remove comments and blank lines
    input_text = re.sub(r"#.*", "", input_text)
    input_text = re.sub(r"\n\s*\n", "\n", input_text)
    input_text = re.sub(r"^\n", "", input_text)
    input_text = re.sub(r"\n*$", "", input_text)
    lines = [line.strip() for line in input_text.split('\n')]

    # Assign connection parameters
    db, host, user, pw, port = lines

    try:
        conn = psycopg2.connect(database=db,
                                host=host,
                                user=user,
                                password=pw,
                                port=port)
        return conn
    except Exception as e:
        print("Could not create connection to database:", e)
        sys.exit()


def main():
    # Open db connection and print welcome message
    conn = open_db()
    print("\nWelcome to the taxi rental management app!")

    user_input = ''
    while user_input != 'x':
        # Display main menu options
        print("\nPlease select an action:")
        print("   1. Manager login\n" \
              "   2. Driver login\n" \
              "   3. Client login\n" \
              "   4. Register new manager\n" \
              "   5. Register new client\n")
        user_input = input("Enter a command (1-5, or x to exit): ")
        match user_input:
            case "1":
                manager.manager_login(conn)
            case "2":
                driver.driver_login(conn)
            case "3":
                client.client_login(conn)
            case '4':
                manager.register_manager(conn)
            case '5':
                client.register_client(conn)
            case 'x':
                pass
            case _:
                print("\nUnknown command, please try again\n")
    # Close the database connection before exiting
    conn.close()


if __name__ == "__main__":
    main()
