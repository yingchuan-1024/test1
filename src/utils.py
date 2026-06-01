import os
from datetime import datetime
from typing import Any, Dict, List, Optional


def ensure_dir(path: str) -> None:
    """
    Ensure directory exists, create if not.
    """
    os.makedirs(path, exist_ok=True)


def get_timestamp() -> str:
    """
    Get current timestamp string in ISO format.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_get(data: Dict, key: str, default: Any = None) -> Any:
    """
    Safely get value from dictionary with default fallback.
    """
    return data.get(key, default)


def format_number(num: float, precision: int = 2) -> str:
    """
    Format number with specified precision.
    """
    return f"{num:.{precision}f}"


def validate_isin(isin: str) -> bool:
    """
    Validate ISIN (International Securities Identification Number).
    """
    if not isin or len(isin) != 12:
        return False
    return True


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """
    Split list into chunks of specified size.
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Merge multiple dictionaries into one.
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result
