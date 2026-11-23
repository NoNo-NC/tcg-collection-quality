"""Manage a trading card collection and JSON persistence."""

import json


class CardCollection:
    """Store cards indexed by their identifiers."""

    def __init__(self):
        self.cards = {}

    def add_card(self, card_id, name, rarity, quantity=1):
        """Add a card or increase the quantity of an existing card."""
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
        file = open(path, "w", encoding="utf-8")
        json.dump(self.cards, file, indent=2)
        file.close()

    def load(self, path):
        """Load a JSON collection, returning whether loading succeeded."""
        try:
            file = open(path, "r", encoding="utf-8")
            self.cards = json.load(file)
            file.close()
            return True
        except:
            return False
