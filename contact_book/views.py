"""
Module: view.py

This module defines the abstract and concrete view layers for the Contact Book application.
It provides a base interface for displaying various types of information (contacts, messages, birthdays)
and a concrete implementation for console output.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Dict


class AbstractView(ABC):
    """
    Abstract Base Class for the View Layer.
    Defines the interface for displaying various types of information.
    """

    @abstractmethod
    def display_contact_card(self, record: Any) -> None:
        """Displays a single contact card."""
        pass

    @abstractmethod
    def display_all_contacts(self, book: Any) -> None:
        """Displays all contacts in the address book."""
        pass

    @abstractmethod
    def display_help(self, commands: Dict[str, str]) -> None:
        """Displays a list of available commands."""
        pass

    @abstractmethod
    def display_message(self, message: str) -> None:
        """Displays a general message (success/error/info)."""
        pass

    @abstractmethod
    def display_upcoming_birthdays(self, upcoming: List[Dict[str, str]]) -> None:
        """Displays a list of upcoming birthdays."""
        pass


class ConsoleView(AbstractView):
    """
    Concrete implementation of the view layer for the console interface.
    """

    def display_contact_card(self, record: Any) -> None:
        """Displays a single contact card."""
        # The Record class has a __str__ method that returns full contact information
        self.display_message(str(record))

    def display_all_contacts(self, book: Any) -> None:
        """Displays all contacts in the address book."""
        # The AddressBook class has a __str__ method that returns all contact entries
        self.display_message(str(book))

    def display_help(self, commands: Dict[str, str]) -> None:
        """Displays a list of available commands."""
        self.display_message("Commands:")
        for command, description in commands.items():
            self.display_message(f"  {command} - {description}")

    def display_message(self, message: str) -> None:
        """Displays a general message (success/error/info)."""
        print(message)

    def display_upcoming_birthdays(self, upcoming: List[Dict[str, str]]) -> None:
        """Displays a list of upcoming birthdays."""
        if not upcoming:
            self.display_message("No upcoming birthdays.")
            return

        result = []
        for item in upcoming:
            result.append(
                f"{item['name']}: birthday {item['birthday']}, greet on {item['greet_date']}"
            )
        self.display_message("\n".join(result))
