"""This module defines the Field base class and specific field types such as Name and Phone."""
from datetime import datetime

class Field:
    """ Base class for all fields (e.g. name, phone)"""
    def __init__(self, value):
        self.value = value  # Store raw field value

    def __str__(self):
        return str(self.value)  # String representation of the field


class Name(Field):
    """ Represents the name of a contact (mandatory field) """
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)  # Initialize the base class


class Phone(Field):
    """ Represents a phone number with validation """
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            # Validate that phone number is exactly 10 digits
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)# Initialize the base class


class Birthday(Field):
    """ Represents a birthday date with validation """
    def __init__(self, value):
        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date_obj)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
