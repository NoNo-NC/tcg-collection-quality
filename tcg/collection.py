"""Manage a trading card collection and JSON persistence."""

import json


class CardCollection:
    """Store cards indexed by their identifiers."""

    def __init__(self):
        self.cards = {}

    @staticmethod
    def _validate_quantity(quantity):
        """Require a strictly positive integer quantity."""
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

    def add_card(self, card_id, name, rarity, quantity=1):
        """Add a card or increase the quantity of an existing card."""
        self._validate_quantity(quantity)

        if card_id in self.cards:
            self.cards[card_id]["quantity"] += quantity
        else:
            self.cards[card_id] = {
                "name": name,
                "rarity": rarity,
                "quantity": quantity,
            }

    def find_card(self, card_id):
        """Return a card, or None if its identifier is unknown."""
        return self.cards.get(card_id)

    def remove_card(self, card_id, quantity=1):
        """Remove copies of a card and delete empty entries."""
        self._validate_quantity(quantity)

        if card_id not in self.cards:
            return False

        self.cards[card_id]["quantity"] -= quantity

        if self.cards[card_id]["quantity"] <= 0:
            del self.cards[card_id]

        return True

    def total_cards(self):
        """Return the total number of card copies."""
        total = 0
        for card in self.cards.values():
            total += card["quantity"]
        return total

    def collection_summary(self):
        """Return a summary grouped by rarity."""
        summary = {
            "common": 0,
            "rare": 0,
            "epic": 0,
            "legendary": 0,
        }

        for card in self.cards.values():
            if card["rarity"] == "common":
                summary["common"] += card["quantity"]
            elif card["rarity"] == "rare":
                summary["rare"] += card["quantity"]
            elif card["rarity"] == "epic":
                summary["epic"] += card["quantity"]
            elif card["rarity"] == "legendary":
                summary["legendary"] += card["quantity"]

        return summary

    def save(self, path):
        """Save the collection to a JSON file."""
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.cards, file, indent=2)

    @staticmethod
    def _is_valid_card(card):
        """Check the required fields of a stored card."""
        if not isinstance(card, dict):
            return False

        return (
            isinstance(card.get("name"), str)
            and isinstance(card.get("rarity"), str)
            and type(card.get("quantity")) is int
            and card["quantity"] > 0
        )

    def load(self, path):
        """Load valid data, preserving the current collection on failure."""
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            return False

        if not isinstance(data, dict):
            return False

        if not all(self._is_valid_card(card) for card in data.values()):
            return False

        self.cards = data
        return True
