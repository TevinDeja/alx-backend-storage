#!/usr/bin/env python3
"""Module for inserting a new document into a MongoDB collection."""
def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document in a collection based on kwargs.
    Args:
        mongo_collection (Collection): The pymongo collection object.
        **kwargs: Arbitrary keyword arguments representing the document fields.
    Returns:
        str: The new _id of the inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
