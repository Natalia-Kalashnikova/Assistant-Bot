"""This module provides functions for saving and loading the AddressBook
using pickle serialization to persist data between sessions.
"""
import pickle
from models.addressbook import AddressBook

def save_data(book, filename="addressbook.pkl"):
    """
    Serializes and saves the AddressBook instance to a file using pickle.
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """
    Loads and deserializes the AddressBook instance from a file using pickle.
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
