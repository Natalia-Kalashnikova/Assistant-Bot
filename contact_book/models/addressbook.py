"""This module defines the AddressBook class for managing contact records."""

from collections import UserDict
from datetime import timedelta, date

class AddressBook(UserDict):
    """Stores and manages contact records (Record instances)"""
    def add_record(self, record):
        """Add a new contact record to the address book."""
        self.data[record.name.value] = record

    def find(self, name):
        """Find and return a record by name"""
        return self.data.get(name)

    def delete(self, name):
        """Delete a record by name"""
        if name in self.data:
            del self.data[name]

    def adjust_for_weekend(self, birthday):
        """
        Shift birthday to next Monday if it falls on a weekend.
        """
        if birthday.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            days_to_monday = 7 - birthday.weekday()
            birthday += timedelta(days=days_to_monday)
        return birthday

    def get_upcoming_birthdays(self):
        """Return list of contacts with birthdays in the next 7 days including today,
        adjusting birthdays falling on weekends to next Monday."""
        today = date.today()
        end_date = today + timedelta(days=6)  # 7 days including today

        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday = record.birthday.value
            # Create birthday date for current year
            bday_this_year = bday.replace(year=today.year)

            # If birthday already passed this year, check next year
            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)

            # Check if birthday is within next 7 days
            if today <= bday_this_year <= end_date:
                # Adjust for weekend using the dedicated function
                congratulation_date = self.adjust_for_weekend(bday_this_year)

                upcoming.append({
                    "name": record.name.value,
                    "birthday": bday.strftime("%d.%m.%Y"),
                    "greet_date": congratulation_date.strftime("%d.%m.%Y")
                })

        return upcoming

    def __str__(self):
        """String representation of the entire address book"""
        if not self.data:
            return "AddressBook is empty."
        return "\n".join(str(record) for record in self.data.values())
