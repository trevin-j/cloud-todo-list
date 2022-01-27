from todo_db import TodoDB


def main():
    '''
    Main function of the program.
    '''
    # Initialize db
    db = TodoDB()

    # Ask for username
    db.ask_username()

    # Main loop
    db.main_loop()


if __name__ == '__main__':
    # Catch KeyboardInterrupt to exit cleanly
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nExiting...')
        exit()