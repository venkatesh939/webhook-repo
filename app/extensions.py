from flask import Flask, jsonify
from flask_pymongo import PyMongo
import logging

app = Flask(__name__)

# Setup MongoDB connection
mongo = PyMongo()

def initialize_mongo(app):
    """
    Initialize the PyMongo instance with the Flask app.
    
    Sets up the MongoDB URI and configures PyMongo to work with the Flask app.
    """
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_history"
    mongo.init_app(app)

def insert_document(document):
    """
    Insert a document into the MongoDB collection.
    
    Args:
        document (dict): The document to be inserted into the database.
        
    Returns:
        ObjectId: The ID of the inserted document.
    """
    try:
        # Insert the document into the 'records' collection
        inserted_id = mongo.db.records.insert_one(document)
        print(f"Document inserted with _id: {inserted_id}")
        return inserted_id
    except Exception as e:
        # Log any errors that occur during the insertion
        logging.error(f"Error inserting document: {e}")

def print_all_documents():
    """
    Retrieve and format all documents from the MongoDB collection.
    
    Queries the 'records' collection, formats each document based on its event type, and returns the results.
    
    Returns:
        list: A list of dictionaries containing the document ID and formatted string.
    """
    data = mongo.db.records.find()
    res = []
    for document in data:
        # Convert MongoDB ObjectId to string for JSON serialization
        document['_id'] = str(document['_id'])
        
        # Determine and format the event type
        if document.get('event_type') == 'push':
            formatted_doc = format_push_document(document)
        elif document.get('event_type') == 'pull_request':
            formatted_doc = format_pull_request_document(document)
        elif document.get('event_type') == 'merge':
            formatted_doc = format_merge_document(document)
        else:
            formatted_doc = "Unsupported event type"

        # Append the formatted document to the result list
        res.append({'_id': document['_id'], 'formatted_doc': formatted_doc})
    return res

def format_push_document(data):
    """
    Format a push event document into a human-readable string.
    
    Args:
        data (dict): The document containing push event details.
        
    Returns:
        str: A formatted string describing the push event.
    """
    # Extract push request details from the data
    author = data.get('author', 'Unknown Author')
    from_branch = data.get('from_branch', 'Unknown Branch')
    timestamp = data.get('timestamp', 'Unknown Time')
    
    # Format the string
    formatted_string = f'"{author}" pushed to "{from_branch}" on {timestamp}'
    return formatted_string

def format_pull_request_document(data):
    """
    Format a pull request event document into a human-readable string.
    
    Args:
        data (dict): The document containing pull request event details.
        
    Returns:
        str: A formatted string describing the pull request event.
    """
    # Extract pull request details from the data
    author = data.get('author', 'Unknown Author')
    from_branch = data.get('from_branch', 'N/A')
    to_branch = data.get('to_branch', 'N/A')
    timestamp = data.get('timestamp', 'Unknown Time')
    
    # Format the string
    return f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'

def format_merge_document(data):
    """
    Format a merge event document into a human-readable string.
    
    Args:
        data (dict): The document containing merge event details.
        
    Returns:
        str: A formatted string describing the merge event.
    """
    # Extract merge details from the data
    author = data.get('author', 'Unknown Author')
    from_branch = data.get('from_branch', 'N/A')
    to_branch = data.get('to_branch', 'N/A')
    timestamp = data.get('timestamp', 'Unknown Time')
    
    # Format the string
    return f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
