from __future__ import annotations

import logging
import os
import io
import sys
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeAlias

import pandas as pd
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSerializable
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from .generate_deck import main as generate_deck_main

# for typing purposes only
if TYPE_CHECKING:
    from pandas import DataFrame

ChainType: TypeAlias = RunnableSerializable[dict[Any, Any], Any]

# defining logging config
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def get_deck_name() -> str:
    if len(sys.argv) < 2:
        raise ValueError("No deck name")
    return sys.argv[1]

def get_api_key() -> str:
    if len(sys.argv) < 3:
        raise ValueError("No API key")
    return sys.argv[2]

def get_input_text() -> str:
    if len(sys.argv) < 4:
        raise ValueError("No input text")
    return sys.argv[3]

# defining path to dirs
deck_name = get_deck_name()
data_dir: Path = Path("data")
csv_file_path: Path = data_dir / f"{deck_name}.csv"

# llm params
MODEL: str = "gpt-4"
TEMPERATURE: float = 0.0

# datatype validation
class FlashCard(BaseModel):
    question: str = Field(description="The question for the flashcard")
    answer: str = Field(description="The answer for the flashcard")


class FlashCardArray(BaseModel):
    flashcards: list[FlashCard]


def llm_generate_flashcards(input: str, prompt: str) -> DataFrame:
    """
    Generates flashcards from the given input text,
    formats them based on the user's prompt,
    and saves the output to a CSV file in the data directory
    """

    llm: ChatOpenAI = ChatOpenAI(model=MODEL, temperature=TEMPERATURE, openai_api_key=get_api_key())

    logging.info("Creating model...")

    parser: PydanticOutputParser[FlashCardArray] = PydanticOutputParser(
        pydantic_object=FlashCardArray
    )

    logging.info("Creating parser...")

    llm_prompt: PromptTemplate = PromptTemplate(
        template=prompt,
        input_variables=["input_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    logging.info("Creating prompt...")

    chain: ChainType = llm_prompt | llm | parser

    logging.info("Parsing and validating input data...")

    output = chain.invoke({"input_text": input})
    list_of_flashcards: list[str] = [card.dict() for card in output.flashcards]
    return pd.DataFrame(list_of_flashcards)


def write_flashcards_to_csv(dataframe: DataFrame, csv_file_path: Path) -> None:
    logging.info("Writing to file...")
    if csv_file_path.is_file():
        dataframe.to_csv(csv_file_path, mode="a", header=False, index=False)
    else:
        dataframe.to_csv(csv_file_path, mode="w", header=False, index=False)


def main() -> None:
    try:
        input_text = get_input_text()
        user_prompt = Path("src/prompt.txt").read_text()

        df = llm_generate_flashcards(input_text, user_prompt)
        qa_list = list(df.to_records(index=False))
        
        generate_deck_main(get_deck_name(), qa_list)

        logging.info("Done \U0001f600")

    except Exception:
        logging.exception("Error occurred")
        return


if __name__ == "__main__":
    main()
