#!/usr/bin/env python3
"""Script that provides stats about Nginx logs stored in MongoDB."""
from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    Args:
    mongo_collection: pymongo collection object

    Returns:
    List of students sorted by average score with an additional key 'averageScore'
    """
    top_student = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top_student
