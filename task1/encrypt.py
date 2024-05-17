import logging
import os
import sys

from sys import argv

from constants import ALPHABET, PATHS

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from util import json_reader, txt_reader, txt_writer, json_writer

SHIFT_NUMBER = int(argv[1])
logging.basicConfig(level=logging.INFO)


def encryption(shift: int, path: str) -> str:
    """
    Encrypt text using Caesar algorithm
    :param shift: number shift for every letter of the string
    :param path: path of the input file
    :return: encrypted string shift every letter on input number of shift
    """

    encrypted = ""

    try:
        input_text = txt_reader(path)

        for letter in input_text:
            encrypted += ''.join((symbol for symbol, code in ALPHABET.items()
                                  if code == (ALPHABET[letter] + shift) % 33))
        return encrypted
    except Exception as ex:
        logging.error(f"Error in encryption or file can't be open or was not found: {ex}\n")


def write_result(input_text: str, shift: int, path_encrypt: str, path_key: str, path_input: str) -> None:
    """
    Write encrypted text and keyword in file
    :param input_text: string input text
    :param shift: number shift for every letter of the string
    :param path_input: path of the file with input text
    :param path_key: path of the file with a key
    :param path_encrypt: path of the file with encrypted text
    :return: None
    """
    try:
        txt_writer(path_encrypt, encryption(shift, path_input))
        dict_result = {key: letter for (key, letter) in zip(input_text, encryption(shift, path_input))}
        json_writer(path_key, dict_result)
    except Exception as ex:
        logging.error(f"Error in encryption or file can't be open or was not found: {ex}\n")


if __name__ == "__main__":
    paths = json_reader(PATHS)
    try:
        write_result(txt_reader(os.path.join(paths["folder"], paths["input"])), SHIFT_NUMBER,
                     os.path.join(paths["folder"], paths["encrypt"]), os.path.join(paths["folder"], paths["key"]),
                     os.path.join(paths["folder"], paths["input"]))
        logging.info(f"Text successfully encrypted and saved to file")
    except Exception as ex:
        logging.error(f"Error in encryption or file can't be open or was not found: {ex}\n")
