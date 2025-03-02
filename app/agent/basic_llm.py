"""
This module provides a SnippetGenerator class for generating snippets based on grant information and user queries.

The SnippetGenerator uses a BaseClient to interact with an LLM and generate relevant snippets.
It also handles concurrent snippet generation for improved performance.

Classes:
    SnippetGenerator: Main class for generating snippets based on grant information and queries.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Tuple
import re
import os
import logging
from dotenv import load_dotenv
from agent.clients import BaseClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load configuration from environment variables
MAX_WORKERS = int(os.getenv('MAX_WORKERS', 64))
TEMPERATURE = int(os.getenv('TEMPERATURE', 0.5))


def get_answer(query: str, client: BaseClient, model_name: str) -> str:
    messages = [
        {"role": "user", "content": query}
    ]
    response = client.chat(model=model_name, messages=messages, temperature=TEMPERATURE)
    print(response)
    return response