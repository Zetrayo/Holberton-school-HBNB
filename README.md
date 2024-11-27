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
  - [Configuration](#configuration)
  - [Author](#author)


## Overview

The **HBnB** project is a modular web application designed with a clean architecture following the Facade pattern to organize the code into Presentation, Business Logic, and Persistence layers. This project sets up an API structure for future implementations, starting with an in-memory repository for data storage, and will eventually integrate a database-backed solution.

## Project Structure

The project is organized into several directories to maintain a modular structure:

```bash
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── basemodel.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

### Directory and files breakdown:

This section outlines the purpose of each directory and file in the project:

- **hbnb/**: The root directory of the project.

  - **app/**: Contains the core application code.
  
    - **__init__.py**: Initializes the app package and creates the Flask application instance.
    
    - **api/**: Houses the API endpoints, organized by version (v1/).
    
      - **__init__.py**: Initializes the api package.
      
      - **v1/**: Contains version 1 of the API.
      
        - **__init__.py**: Initializes the v1 package.
        
        - **users.py**: Handles API endpoints related to user operations.
        
        - **places.py**: Manages API endpoints for place-related operations.
        
        - **reviews.py**: Contains API endpoints for handling reviews.
        
        - **amenities.py**: Manages API endpoints related to amenities.
        
    - **models/**: Contains the business logic classes.
    
      - **__init__.py**: Initializes the models package.
      
      - **basemodel.py**: Defines the basemodel class from whitch every other class will inherits.
      
      - **user.py**: Defines the user class and its methods.
      
      - **place.py**: Defines the place class and its methods.
      
      - **review.py**: Defines the review class and its methods.
      
      - **amenity.py**: Defines the amenity class and its methods.
      
    - **services/**: Contains service classes that implement business logic.
    
      - **__init__.py**: Initializes the services package.
      
      - **facade.py**: Implements the Facade pattern to manage interactions between layers.
      
    - **persistence/**: Contains the repository implementation.
    
      - **__init__.py**: Initializes the persistence package.
      
      - **repository.py**: Implements the in-memory repository for temporary object storage and management.
      
  - **run.py**: The entry point for running the Flask application.

  - **config.py**: Contains configuration settings for the application, including environment variables.

  - **requirements.txt**: Lists all the Python packages needed for the project.

  - **README.md**: Provides an overview of the project, including setup instructions and descriptions of the project structure.


## Requirements

To set up and run the HBnB project, you need the following:

- **Python 3.x**
- **Flask** and **Flask-RESTx**

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/hbnb.git
cd hbnb
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the Flask application locally, use the following command:

```bash
python run.py
```

The application will start with `debug=True` by default for the development environment.

## Configuration

The configuration settings are managed via `config.py`. By default, the project uses `DevelopmentConfig` to enable debug mode. You can configure the environment by setting the `SECRET_KEY` and other relevant settings.

## Author

Anne-Cécile [Arc] Besse, José Puertas

