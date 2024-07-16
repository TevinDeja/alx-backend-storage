#!/usr/bin/env python3
"""Module for retrieving documents from a MongoDB collection."""


def list_all(mongo_collection):
    """
    Retrieve all documents from a MongoDB collection.

    Args:
        mongo_collection (Collection): The pymongo collection object to query.

    Returns:
        List[dict]: A list containing all documents in the collection.
                    If the collection is empty, returns an empty list.
    """
    return [documents for documents in mongo_collection.find()]
