# HBnB Project

## Table of Contents
- [HBnB Project](#hbnb-project)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Project Structure](#project-structure)
    - [Directory and files breakdown:](#directory-and-files-breakdown)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Testing](#testing)
  - [Configuration](#configuration)
  - [Author](#author)

## Overview

The **HBnB** project is a modular web application designed with a clean architecture following the Facade pattern. It organizes the codebase into three main layers: Presentation, Business Logic, and Persistence. The project provides a foundation for creating and managing RESTful APIs with initial support for in-memory data storage, extendable to database-backed solutions.

## Project Structure

The project is organized into several directories to maintain a clear modular structure:

```bash
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── amenities.py
│   │       ├── auth.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── users.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── amenity.py
│   │   ├── baseclass.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── user.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
├── instance/
│   ├── your_database.db
├── SQL/
│   ├── schema.sql
│   ├── seed.sql
├── static/
│   ├── script.js
│   ├── styles.css
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── place.html
├── config.py
├── extensions.py
├── mermaid_diagram.mmd
├── README.md
├── requirements.txt
├── run.py
```

### Directory and files breakdown:

```bash
hbnb/
├── app/
│   ├── __init__.py               # Initializes the app package and creates the Flask app instance
│   ├── api/                      # Handles all API-related functionalities
│   │   ├── __init__.py           # Initializes the API package
│   │   ├── v1/                   # Version 1 of the API
│   │       ├── __init__.py       # Initializes the v1 package
│   │       ├── amenities.py      # Endpoints for managing amenities
│   │       ├── auth.py           # Handles user authentication and authorization
│   │       ├── places.py         # Endpoints for managing places
│   │       ├── reviews.py        # Endpoints for managing reviews
│   │       ├── users.py          # Endpoints for managing users
│   ├── models/                   # Contains core business logic and data models
│   │   ├── __init__.py           # Initializes the models package
│   │   ├── baseclass.py          # Base class for other models
│   │   ├── amenity.py            # Represents the Amenity model
│   │   ├── place.py              # Represents the Place model
│   │   ├── review.py             # Represents the Review model
│   │   ├── user.py               # Represents the User model
│   ├── persistence/              # Handles data storage and management
│   │   ├── __init__.py           # Initializes the persistence package
│   │   ├── repository.py         # Implements an in-memory repository
│   ├── services/                 # Implements business logic and coordination
│   │   ├── __init__.py           # Initializes the services package
│   │   ├── facade.py             # Facade pattern for interaction between layers
├── instance/
│   ├── your_database.db          # Example database file (if applicable)
├── SQL/
│   ├── schema.sql                # Database schema
│   ├── seed.sql                  # Sample data for the database
├── static/
│   ├── script.js                 # JavaScript for frontend functionality
│   ├── styles.css                # CSS for styling the application
├── templates/
│   ├── index.html                # Homepage template
│   ├── login.html                # Login page template
│   ├── place.html                # Place details template
├── config.py                     # Configuration settings for the application
├── extensions.py                 # Extensions and additional integrations
├── mermaid_diagram.mmd           # Mermaid.js diagrams for visual documentation
├── README.md                     # Project documentation
├── requirements.txt              # List of dependencies
├── run.py                        # Entry point to start the application
```

## Requirements

Ensure the following software is installed:
- Python 3.x
- Flask and Flask-RESTx (installed via `requirements.txt`)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Zetrayo/Holberton-school-HBNB.git
cd hbnb
```

1. Create and activate a virtual environment:

``` bash
python3 -m venv venv
source venv/bin/activate
```

1. Install dependencies:

``` bash
pip install -r requirements.txt
```

## Running the Application

Launch the application with:

```bash
python run.py
```
The application will run with debugging enabled for development purposes.

## Testing

Run all test cases using:

```bash
python -m unittest discover -s tests
```
This ensures the codebase meets functionality and reliability standards.

## Configuration

All settings are stored in `config.py`. Customize them based on your environment:
- `DevelopmentConfig`: Debug mode for local testing.
- `ProductionConfig`: For deployment with optimizations.

Key variables include:
- `SECRET_KEY`: Secures sessions and tokens.
- `SQLALCHEMY_DATABASE_URI`: Database connection string (if applicable).

## Author

- **Anne-Cécile [Arc] Besse**
- **José Puertas**
