## Initializes the database connection and runs the main menu loop

import psycopg2
import manager
import re
import sys

def open_db():
    """Reads database info from file \"dbinfo.txt\" and 
       attempts to open a new dabase connection
       
       Returns:
        Conn: A psycopg2 database connection object"""
    
    with open("dbinfo.txt") as input_file:
        try:
            input_text = input_file.read()
        except Exception as e:
            print("Could not get db info from file:", e)
            sys.exit()

    # Process file text and split into lines
    # (I know this is extra but I had the code already from a different project)
    input_text = re.sub("#.*", "", input_text)
    input_text = re.sub("\n\s*\n", "\n", input_text)
    input_text = re.sub("^\n", "", input_text)
    input_text = re.sub("\n*$", "", input_text)
    lines = [line.strip() for line in input_text.split('\n')]

    # Get info from file lines
    db = lines[0]
    host = lines[1]
    user = lines[2]
    pw = lines[3]
    port = lines[4]

    ## Attempt to create database connection
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

    ## Main menu loop. Runs until user enter's 'x' to quit
    user_input = ''
    while(user_input != 'x'):
        ## Print prompt
        print("\nPlease select an action:")
        print("   1. Manager login\n" \
                "   2. Driver login\n" \
                "   3. Client login\n" \
                "   4. Register new manager\n" \
                "   5. Register new client\n")
        ## 
        user_input = input("Enter a command (1-5, or x to exit): ")
        match user_input:
            case "1":
                manager.manager_login(conn)
            case "2":
                print("TODO: Implement Driver features")
            case "3":
                print("TODO: Implement Client features")
            case '4':
                manager.register_manager(conn)
            case '5':
                print("TODO: Implement client registration")
            case'x':
                pass
            case default:
                print("\nUnknown command, please try again\n")
    # End of while loop: close db connection
    conn.close()

if __name__ == "__main__":
    main()
    











