# FastAPI with MongoDB


## Description

User + Organization Relationship in FastAPI

## Features

- Create/List/Fetch User
- Create/List Organization
- Create/Update/Delete Permissions


## Installation

To use this project, follow these steps:

1. Clone the repository: `git clone https://github.com/jeffysam6/fastapi-with-mongodb.git`
2. Change directory: `cd fastapi-with-mongodb`
3. Create a Virtual Environment: `python -m venv venv`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the application: `python app/main.py `

## Directory Structure
.
├── __init__.py
├── main.py
└── server
    ├── app.py
    ├── database
    │   ├── __init__.py
    │   ├── organization.py
    │   ├── permission.py
    │   └── user.py
    ├── database.py
    ├── models
    │   ├── organization.py
    │   ├── permission.py
    │   └── user.py
    └── routes
        ├── organization.py
        ├── permission.py
        └── user.py

## Usage

Here's how you can use this project:

1. Try out the endpoints at http://localhost:8000/docs

