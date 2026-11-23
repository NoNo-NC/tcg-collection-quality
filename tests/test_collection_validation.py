"""Regression tests for quantities and collection loading."""

import json

import pytest

from tcg.collection import CardCollection


def test_add_negative_quantity_is_rejected():
    collection = CardCollection()

    with pytest.raises(ValueError):
        collection.add_card("001", "Ember Dragon", "rare", -2)

    assert collection.find_card("001") is None
    assert collection.total_cards() == 0


def test_remove_negative_quantity_is_rejected():
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare", 3)

    with pytest.raises(ValueError):
        collection.remove_card("001", -2)

    assert collection.find_card("001")["quantity"] == 3


def test_load_invalid_structure_preserves_collection(tmp_path):
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare", 3)

    path = tmp_path / "invalid_structure.json"
    path.write_text('["not", "a", "collection"]', encoding="utf-8")

    assert collection.load(path) is False
    assert collection.find_card("001")["quantity"] == 3
    assert collection.total_cards() == 3


@pytest.mark.parametrize("quantity", [0, 1.5, "2", None, True])
def test_add_invalid_quantity_preserves_existing_card(quantity):
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare", 3)

    with pytest.raises(ValueError):
        collection.add_card("001", "Ember Dragon", "rare", quantity)

    assert collection.find_card("001")["quantity"] == 3


@pytest.mark.parametrize("quantity", [0, 1.5, "2", None, True])
def test_remove_invalid_quantity_preserves_existing_card(quantity):
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare", 3)

    with pytest.raises(ValueError):
        collection.remove_card("001", quantity)

    assert collection.find_card("001")["quantity"] == 3


@pytest.mark.parametrize(
    "card",
    [
        None,
        [],
        {},
        {"name": 123, "rarity": "rare", "quantity": 1},
        {"name": "Ember Dragon", "rarity": 123, "quantity": 1},
        {"name": "Ember Dragon", "rarity": "rare", "quantity": "2"},
        {"name": "Ember Dragon", "rarity": "rare", "quantity": True},
        {"name": "Ember Dragon", "rarity": "rare", "quantity": 0},
        {"name": "Ember Dragon", "rarity": "rare", "quantity": -1},
    ],
)
def test_load_invalid_card_preserves_collection(tmp_path, card):
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare", 3)

    path = tmp_path / "invalid_card.json"
    path.write_text(json.dumps({"002": card}), encoding="utf-8")

    assert collection.load(path) is False
    assert collection.find_card("001")["quantity"] == 3
    assert collection.find_card("002") is None
    assert collection.total_cards() == 3


def test_load_empty_collection(tmp_path):
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare", 3)

    path = tmp_path / "empty.json"
    path.write_text("{}", encoding="utf-8")

    assert collection.load(path) is True
    assert collection.total_cards() == 0


def test_load_invalid_encoding_preserves_collection(tmp_path):
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare", 3)

    path = tmp_path / "invalid_encoding.json"
    path.write_bytes(b"\xff\xfe\xfa")

    assert collection.load(path) is False
    assert collection.find_card("001")["quantity"] == 3


def test_load_invalid_json_preserves_collection(tmp_path):
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare", 3)

    path = tmp_path / "malformed.json"
    path.write_text("{invalid json", encoding="utf-8")

    assert collection.load(path) is False
    assert collection.find_card("001")["quantity"] == 3
