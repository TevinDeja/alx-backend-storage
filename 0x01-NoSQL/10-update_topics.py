#!/usr/bin/env python3
"""Module for updating topics of a school document in a MongoDB collection."""
def update_topics(mongo_collection, name, topics):
    """
    Change all topics of a school document based on the name.
    Args:
        mongo_collection (Collection): The pymongo collection object.
        name (str): The school name to update.
        topics (list of str): The list of topics approached in the school.
    Returns:
        int: The number of documents updated.
    """
    result = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
    return result.modified_count
