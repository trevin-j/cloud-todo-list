# Overview

My goal for this software is to create a fully functioning program that stores to-do list items for the user in the cloud. These items are stored in the cloud so that the user can access them from any device that can run this program. To develop this program, I learned a lot about using NoSQL cloud databases and how they work.

This software integrates with Google's Firestore database, which is a part of Firebase. Each user can have their own data stored separate from other users.

In order to use this software, the user must create their own database using Google Firebase and Firestore. The user must then download the .json file for the service account for the database, and put it in the project folder. Then, rename the .json file to "serviceAccountKey.json". After that, the requirements must be installed. Those requirements are found under the "Development Environment" section.

Once this is done, this program has full access to the user's Firestore database, and the user can begin to use this program. The program uses a simple interface in the console. When the program is launched, any name may be entered. If the name already exists in the database, information from that username will be synced. If the name does not exist, it will be created. Usage is simple, the user can simply follow the on-screen information.

[Software Demo Video](https://youtu.be/SX3tfP5jgow)

# Cloud Database

The cloud database used in this program is Google Firestore. The layout is pretty simple, and is explained below.

Each collection in the database represents a user, and as such, is named as the user's name. Each document represents 1 to-do item. The ID of each item is auto-assigned so that many similar to-do items may be stored under one user. Each item uses the following structure:

```
{
    'type': 'action',
    'title': 'TITLE HERE',
    'desc': 'DESCRIPTION HERE',
    'due': 'DATE TO BE COMPLETED',
    'created': 'DATE CREATED',
    'is_complete': True
}
```

* `'type'` represents the type of item. Currently there is only action, but more types of to-do items are planned.
* `'title'` holds the title of the to-do item.
* `'desc'` holds the description of the item.
* `'due'` holds the user-specified due date of the item.
* `'created'` holds the date that the item was created. It is automatically set when the item is created.
* `'is_complete'` holds a boolean value that represents if the item has been completed or not.

# Development Environment

* Visual Studio Code
* Python 3.9.4 64-bit (Most versions of Python 3 should work)
* venv virtual environment

### Built-in modules:

* datetime
* time
* os

### Required modules:

* firebase_admin (Install with `pip install firebase_admin`)

# Useful Websites

* [Google Firebase Console](https://console.firebase.google.com/)
* [Google Firebase Admin SDK - Python](https://firebase.google.com/docs/reference/admin/python)

# Future Work

* Add local cache/storage to allow offline usage, and temporary storage in case of disconnection.
* Add support for more types of to-do items. Example: project, which functions as a collection of related action items.
* Use Firebase REST API, or Pyrebase, or switch languages so support individual authentication with Google. This would allow shipping this software with the key built in, and use the same database, but do so securely. Users would stay separate, and each would only have access to their own data.