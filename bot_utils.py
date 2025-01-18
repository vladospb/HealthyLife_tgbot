"""Module with utils for the tg bot and its integration with the baseline"""

import logging
import os
from pathlib import Path

def parse_response_for_bot(response: list[dict[str, str]]) -> list[str]:
    """Get llama response, parse and format it for telegram.

    Args:
        response (list[dict{str:str}]): response from parse_deepseek_response.

    Returns:
        list[str]: blocks of text with len <= 4095, formatted for tg

    """
    blocks = [
        f"""<u><b>{x['main_text']}</b></u>:
        <blockquote expandable>{x['elaborate_text']}</blockquote>"""
        for x in response
    ]
    parsed_response = "\n\n".join(blocks)
    if len(parsed_response) <= 4095:
        return [parsed_response]

    large_blocks = [[]]
    cumlen = 0
    current_large_block = 0
    for block in blocks:
        block_len = len(block)
        if cumlen + block_len <= 4095:
            large_blocks[current_large_block].append(block)
            cumlen += block_len
        else:
            current_large_block += 1
            cumlen = block_len
            large_blocks.append([block])
    parsed_long_response = ["\n\n".join(x) for x in large_blocks]
    return parsed_long_response

def logging_start(filename: str = "templog") -> logging.Logger:
    """Start logging, print test log messages, get logger for future use.

    Args:
        filename (str): name of the .log file
            (without .log)

    Returns:
        logging.Logger: preformatted logger

    """
    cur_path = os.path.dirname(os.path.realpath(__file__))
    cur_dir_1_up = os.path.dirname(cur_path)
    intended_path = os.path.join(cur_dir_1_up, f"logs/{filename}.log")

    if not os.path.exists(os.path.dirname(intended_path)):
        os.makedirs(os.path.dirname(intended_path))

    logging.basicConfig(
        filename=intended_path,  # Use os.path.join for portability
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    handler = logging.FileHandler(
        "w",
        encoding="utf-8",
    )
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)

    # Log a test message
    start_message = "logging start"
    root_logger.debug(start_message)
    root_logger.info(start_message)
    root_logger.warning(start_message)
    root_logger.error(start_message)
    root_logger.critical(start_message)

    return root_logger
