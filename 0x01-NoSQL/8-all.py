#!/usr/bin/env python3
"""Module for listing all documents in a MongoDB collection."""

from pymongo.collection import Collection
from typing import List


def list_all(mongo_collection: Collection) -> List[dict]:
    """
    List all documents in a MongoDB collection.

    Args:
        mongo_collection (Collection): The pymongo collection object.

    Returns:
        List[dict]: A list of all documents in the collection.
                    Returns an empty list if no documents are found.
    """
    return list(mongo_collection.find())
