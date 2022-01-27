# This file holds the TodoDB class, which is used for communicating with the cloud database.

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import time
import os

def cls():
    '''
    Cross platform clear screen.
    Seems to be a universal solution, but one source can be found here.
    https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    '''
    os.system('cls' if os.name=='nt' else 'clear')

def get_current_date() -> str:
    '''
    Get the current date.
    '''
    return datetime.datetime.now().strftime('%m-%d-%Y')


class TodoDB:
    
    def __init__(self) -> None:
        '''
        Initialize the db.
        Part of the initialization is to set up credentials for the cloud db.
        '''
        self.setup_credentials()
        self._username = None


    def setup_credentials(self) -> None:
        '''
        Set up the credentials with the provided service account
        Warn user of no credentials and exit app if FileNotFoundError
        '''
        cls()
        print('Connecting to database...')
        try:
            self._cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(self._cred)

            self._db = firestore.client()

        except FileNotFoundError:
            print('The service account key file was not found. Please see the README for instructions on how to create this file.')
            exit()
        cls()

    
    def ask_username(self) -> None:
        '''
        Get the username from the user.
        NOTE: Separate users are not secure from one another due to using an admin account.
        There would be no point in a password because it could just be queried by some simple python code
        But in case someone wants to keep their todo-lists separate, they can choose a username.
        '''
        cls()
        print('Please enter your username.')
        print('If the username does not exist, it will be created.')
        self._username = input('> ')
        cls()

    
    def refresh_list(self) -> None:
        '''
        Refresh the list of todo items from the cloud database.
        '''
        cls()
        print('Syncing...')
        if self._username is not None:
            self._todo_items = self._db.collection(self._username).get()
        else:
            raise ValueError('Username not set.')
        cls()


    def main_loop(self) -> None:
        '''
        Does the main loop of the program.
        '''
        while True:
            self.refresh_list()
            self.print_todo_items()
            self.print_main_menu()
            self.handle_user_input()

    
    def print_todo_items(self) -> None:
        '''
        Print out all the todo items.
        Format spacing is used for alignment.
        '''
        header = ('#', 'is completed', 'created', 'due', 'title', 'description')
        print(f'{header[0]:4}{header[1]:17}{header[2]:14}{header[3]:14}{header[4]:30}{header[5]}')
        print('------------------------------------------------------------------------------------------')
        for i, item in enumerate(self._todo_items):
            print(f'{str(i):4}{str(item.get("is_completed")):17}{item.get("created"):14}{item.get("due"):14}{item.get("title"):30}{item.get("desc")}')

    
    def print_main_menu(self) -> None:
        '''
        Print the main menu to the screen and show user their options.
        '''
        print('\n\nMain Menu')
        print('1. Add a new todo item')
        print('2. Toggle a todo item as completed')
        print('3. Refresh todo list')
        print('4. Delete a todo item')
        print('5. Modify a todo item')
        print('6. Exit')


    def handle_user_input(self) -> None:
        '''
        Handles user's input in the main menu.
        '''
        choice = input('> ')
        cls()

        if choice == '1':
            self.add_todo_item()
        elif choice == '2':
            self.toggle_todo_item()
        elif choice == '3':
            # List refreshes automatically when the user enters the main menu.
            return
        elif choice == '4':
            self.delete_todo_item()
        elif choice == '5':
            self.modify_todo_item()
        elif choice == '6':
            exit()


    def add_todo_item(self) -> None:
        '''
        Add a new todo item to the cloud database.
        '''
        print('Add a new todo item.')
        print('--------------------')
        title = input('Title> ')
        desc = input('Description> ')
        due = input('Due date (mm-dd-yyyy)> ')
        created = get_current_date()
        self._db.collection(self._username).document().set({
            'title': title,
            'desc': desc,
            'due': due,
            'is_completed': False,
            'created': created,
            'type': 'action'
        })


    
    def toggle_todo_item(self) -> None:
        '''
        Toggle a todo item as completed.
        '''
        invalid = True
        while invalid:

            cls()
            print('Toggle a todo item as completed.')
            print('---------------------------------')
            print('Enter the number of the todo item you want to toggle.')
            print('To cancel, enter "x"')

            self.print_todo_items()
            choice = input('> ')

            if choice == 'x':
                return

            try:
                item_id = self._todo_items[int(choice)].id
                if self._todo_items[int(choice)].get('is_completed'):
                    self._db.collection(self._username).document(item_id).update({
                        'is_completed': False
                    })
                else:
                    self._db.collection(self._username).document(item_id).update({
                        'is_completed': True
                    })
                invalid = False
            except (IndexError, ValueError):
                print('Invalid choice.')
                time.sleep(1)
        

    def delete_todo_item(self) -> None:
        '''
        Deletes an item from the todo-list.
        '''
        invalid = True
        while invalid:
            cls()
            print('Delete a todo item.')
            print('--------------------')
            print('Enter the number of the todo item you want to delete.')
            print('To cancel, enter "x"')
            self.print_todo_items()
            choice = input('> ')

            if choice == 'x':
                return

            try:
                item_id = self._todo_items[int(choice)].id
                self._db.collection(self._username).document(item_id).delete()
                invalid = False
            except (IndexError, ValueError):
                print('Invalid choice.')
                time.sleep(1)


    def modify_todo_item(self) -> None:
        '''
        Modifies an item in the todo-list.
        '''
        invalid = True
        while invalid:
            cls()
            print('Modify a todo item.')
            print('--------------------')
            print('Enter the number of the todo item you want to modify.')
            print('To cancel, enter "x"')
            self.print_todo_items()
            choice = input('> ')

            if choice == 'x':
                return

            try:
                item_id = self._todo_items[int(choice)].id
                chosen_item = self._todo_items[int(choice)]
                invalid = False
            except (IndexError, ValueError):
                print('Invalid choice.')
                time.sleep(1)
        
        cls()
        print('\n\nModify the following todo item:')
        print('-------------------------------')
        print(f'Title: {chosen_item.get("title")}')
        print(f'Description: {chosen_item.get("desc")}')
        print(f'Due date: {chosen_item.get("due")}')
        print(f'Date created: {chosen_item.get("created")}')
        print(f'Is complete: {chosen_item.get("is_completed")}\n')

        # User picks what they want to modify.
        print('What would you like to modify?')
        print('1. Title')
        print('2. Description')
        print('3. Due date')
        print('4. Cancel')

        choice = input('> ')
        print()

        # Modify the title.
        if choice == '1':
            title = input('Title> ')
            self._db.collection(self._username).document(item_id).update({
                'title': title
            })

        # Modify the description.
        elif choice == '2':
            desc = input('Description> ')
            self._db.collection(self._username).document(item_id).update({
                'desc': desc
            })

        # Modify the due date.  
        elif choice == '3':
            due = input('Due date (mm-dd-yyyy)> ')
            self._db.collection(self._username).document(item_id).update({
                'due': due
            })

        # Cancel.
        elif choice == '4':
            return
