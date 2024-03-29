import logging
import os
import random
from pathlib import Path

from genanki import Deck, Model, Note, Package

# defining logging config
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def create_anki_deck(deck_name: str, qa_list: list[tuple[str, str]]) -> Deck:
    model_id = random.randrange(1 << 30, 1 << 31)
    my_model = Model(
        model_id,
        "Simple Model",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
    )

    deck_id = random.randrange(1 << 30, 1 << 31)
    my_deck = Deck(deck_id, deck_name)

    for question, answer in qa_list:
        my_note = Note(model=my_model, fields=[question, answer])
        my_deck.add_note(my_note)

    return my_deck


def export_anki_deck(deck: Deck, output_file: Path) -> None:
    Package(deck).write_to_file(output_file)


def main(output_deck_name, qa_list) -> None:
    my_deck = create_anki_deck(output_deck_name, qa_list)

    # defining path to output
    deck_dir: Path = Path("./.")
    output_file_path: Path = deck_dir / f"{output_deck_name}.apkg"
    
    export_anki_deck(my_deck, output_file_path)
    logging.info(f"'{output_deck_name}' Anki deck created")


if __name__ == "__main__":
    main()
