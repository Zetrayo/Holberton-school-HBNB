from extensions import db
from abc import ABC, abstractmethod

class Repository(ABC):
    """Abstract base class for repository pattern. Defines common methods for CRUD operations."""
    
    @abstractmethod
    def add(self, obj):
        """Add a new object to the database."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its unique ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects of a particular model."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an existing object in the database."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object from the database by its ID."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute and its value."""
        pass


class SQLAlchemyRepository(Repository):
    """Concrete implementation of the Repository pattern using SQLAlchemy."""
    
    def __init__(self, model):
        """Initialize with a SQLAlchemy model."""
        self.model = model  # Model associated with the repository

    def add(self, obj):
        """Add a new object to the session and commit it to the database."""
        db.session.add(obj)  # Add the object to the session
        db.session.commit()  # Commit the session to the database

    def get(self, obj_id):
        """Retrieve an object by its ID."""
        return self.model.query.get(obj_id)  # Query the model to fetch the object by ID

    def get_all(self):
        """Retrieve all objects of the model."""
        return self.model.query.all()  # Return all records from the table

    def update(self, obj_id, data):
        """Update an object with new data."""
        obj = self.get(obj_id)  # Get the object by ID
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)  # Set the updated values on the object
            db.session.commit()  # Commit the changes to the database

    def delete(self, obj_id):
        """Delete an object from the database by its ID."""
        obj = self.get(obj_id)  # Get the object by ID
        if obj:
            db.session.delete(obj)  # Delete the object from the session
            db.session.commit()  # Commit the changes to the database

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute and value."""
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()
        # Filter records by attribute and return the first match
