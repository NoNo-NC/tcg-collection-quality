from tcg.collection import CardCollection


def test_new_collection_is_empty():
    collection = CardCollection()

    assert collection.total_cards() == 0


def test_add_card():
    collection = CardCollection()

    collection.add_card("001", "Ember Dragon", "rare", 2)

    assert collection.find_card("001") == {
        "name": "Ember Dragon",
        "rarity": "rare",
        "quantity": 2,
    }


def test_add_existing_card_increases_quantity():
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare", 2)

    collection.add_card("001", "Ember Dragon", "rare", 3)

    assert collection.find_card("001")["quantity"] == 5


def test_find_unknown_card():
    collection = CardCollection()

    assert collection.find_card("unknown") is None


def test_remove_some_copies():
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare", 3)

    result = collection.remove_card("001", 1)

    assert result is True
    assert collection.find_card("001")["quantity"] == 2


def test_remove_last_copy():
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare")

    assert collection.remove_card("001") is True
    assert collection.find_card("001") is None


def test_remove_unknown_card():
    collection = CardCollection()

    assert collection.remove_card("unknown") is False


def test_total_cards():
    collection = CardCollection()
    collection.add_card("001", "Ember Dragon", "rare", 2)
    collection.add_card("002", "Forest Sprite", "common", 3)

    assert collection.total_cards() == 5


def test_collection_summary():
    collection = CardCollection()
    collection.add_card("001", "Forest Sprite", "common", 3)
    collection.add_card("002", "Ember Dragon", "rare", 2)
    collection.add_card("003", "Storm Guardian", "epic", 1)
    collection.add_card("004", "Ancient Phoenix", "legendary", 1)

    assert collection.collection_summary() == {
        "common": 3,
        "rare": 2,
        "epic": 1,
        "legendary": 1,
    }


def test_save_and_load(tmp_path):
    original = CardCollection()
    original.add_card("001", "Ember Dragon", "rare", 2)
    path = tmp_path / "collection.json"

    original.save(path)
    restored = CardCollection()

    assert restored.load(path) is True
    assert restored.find_card("001") == original.find_card("001")


def test_load_missing_file(tmp_path):
    collection = CardCollection()

    assert collection.load(tmp_path / "missing.json") is False


def test_load_invalid_json(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text("not valid json", encoding="utf-8")
    collection = CardCollection()

    assert collection.load(path) is False
