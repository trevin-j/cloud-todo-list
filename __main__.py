import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# See db_layout.txt to see the layout of the database.



def cls():
    '''
    Cross platform clear screen.
    Seems to be a universal solution, but one source can be found here.
    https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    '''
    os.system('cls' if os.name=='nt' else 'clear')


def print_todo_items(todo_items):
    '''
    Print out all the todo items from the passed list of documents.
    '''
    header = ('#', 'is completed', 'created', 'due', 'title', 'description')
    print(f'{header[0]:4}{header[1]:17}{header[2]:10}{header[3]:10}{header[4]:30}{header[5]}')
    print('--------------------------------------------------------------------------------')
    for i, item in enumerate(todo_items):
        print(f'{str(i):4}{str(item.get("is_completed")):17}{item.get("created"):10}{item.get("due"):10}{item.get("title"):30}{item.get("desc")}')



def main():
    cls()
    print('Connecting to database...')

    # Set up the credentials with the provided service account
    # Warn user of no credentials and exit app if FileNotFoundError
    try:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred)

        db = firestore.client()

    except FileNotFoundError:
        print('The service account key file was not found. Please see the README for instructions on how to create this file.')
        exit()

    cls()

    # Get username from user
    # NOTE: The database is NOT secure from this program due to using firebase_admin
    # There would be no point in a password because it could just be queried by some simple python code
    # But in case someone wants to keep their todo-lists separate, they can choose a username.
    print('Please enter your username.')
    print('If the username does not exist, it will be created.')
    username = input('> ')

    # Retrieve all todo items from the database
    todo_items = db.collection(username).get()

    cls()

    # Main loop
    while True:

        cls()

        # Print out all the todo items
        print_todo_items(todo_items)

        # Print main menu
        print('\n\nMain Menu')
        print('1. Add a new todo item')
        print('2. Toggle a todo item as completed')
        print('3. Refresh todo list')
        print('4. Delete a todo item')
        print('5. Modify a todo item')
        print('6. Exit')

        # Get user input
        choice = input('> ')

        cls()

        # Add a new todo item
        if choice == '1':
            print('Add a new todo item')
            print('-------------------')
            title = input('Title> ')
            desc = input('Description> ')
            due = input('Due date> ')
            created = input('Today\'s date> ')

            data = {
                'title': title,
                'desc': desc,
                'due': due,
                'created': created,
                'is_completed': False,
                'type': 'action'
            }

            # Create a new document with the provided info, but auto assign the document id
            db.collection(username).document().set(data)

            # Refresh the todo items automatically after adding a new item
            todo_items = db.collection(username).get()


        # Toggle a todo item as completed
        elif choice == '2':
            cls()
            print('Toggle a todo item as completed')
            print('----------------------------')
            print('Enter the number of the todo item you want to toggle.')
            print()
            print_todo_items(todo_items)
            todo_item_num = int(input('> '))

            # Toggle the todo item as completed
            item_id = todo_items[todo_item_num].id
            if todo_items[todo_item_num].get('is_completed'):
                db.collection(username).document(item_id).update({'is_completed': False})
            else:
                db.collection(username).document(item_id).update({'is_completed': True})

            # Refresh the todo items automatically after toggling a todo item
            todo_items = db.collection(username).get()

        

        elif choice == '3':
            # Refresh the todo list
            todo_items = db.collection(username).get()


        # Delete a todo item
        elif choice == '4':
            cls()
            print('Delete a todo item')
            print('-------------------')
            print('Enter the number of the todo item you want to delete.')
            print()
            print_todo_items(todo_items)
            todo_item_num = int(input('> '))

            # Delete the todo item
            item_id = todo_items[todo_item_num].id
            db.collection(username).document(item_id).delete()

            # Refresh the todo items automatically after deleting a todo item
            todo_items = db.collection(username).get()

        
        # Modify a todo item
        elif choice == '5':
            cls()
            print('Modify a todo item')
            print('-------------------')
            print('Enter the number of the todo item you want to modify.')
            print()
            print_todo_items(todo_items)
            todo_item_num = int(input('> '))

            # Get the id of the todo item
            item_id = todo_items[todo_item_num].id

            

            # Loop until user decides to finish editing
            while True:
                
                cls()
                # Print the chosen todo item and its data
                print('\n\nModify the following todo item:')
                print('-------------------------------')
                print(f'Title: {todo_items[todo_item_num].get("title")}')
                print(f'Description: {todo_items[todo_item_num].get("desc")}')
                print(f'Due date: {todo_items[todo_item_num].get("due")}')
                print(f'Date created: {todo_items[todo_item_num].get("created")}')
                print(f'Is complete: {todo_items[todo_item_num].get("is_completed")}')

                print()
                # Have user decide what to modify
                print('What do you want to modify?')
                print('1. Title')
                print('2. Description')
                print('3. Due date')
                print('4. Finish editing')

                choice = input('> ')
                print()

                # Modify the title
                if choice == '1':
                    title = input('Enter the new title> ')
                    db.collection(username).document(item_id).update({'title': title})

                # Modify the description
                elif choice == '2':
                    desc = input('Enter the new description> ')
                    db.collection(username).document(item_id).update({'desc': desc})

                # Modify the due date
                elif choice == '3':
                    due = input('Enter the new due date> ')
                    db.collection(username).document(item_id).update({'due': due})

                # Finish editing
                elif choice == '4':
                    break

                # Refresh the todo items automatically after modifying a todo item
                todo_items = db.collection(username).get()
                




        elif choice == '6':
            print('Exiting...')
            exit()





if __name__ == '__main__':
    main()