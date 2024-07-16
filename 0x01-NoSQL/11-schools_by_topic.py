#!/usr/bin/env python3
"""Module for finding schools by topic in a MongoDB collection."""
def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.
    Args:
        mongo_collection (Collection): The pymongo collection object.
        topic (str): The topic to search for.
    Returns:
        list: A list of school documents that have the specified topic.
    """
    query = {"topics": topic}
    schools = list(mongo_collection.find(query))
    return schools
