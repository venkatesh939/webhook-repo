from flask import Blueprint, json, request
from app.extensions import insert_document, print_all_documents
from flask import render_template

# Create a new Blueprint named 'Webhook' for handling webhook-related routes
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=['POST'])
def api_github_record():
    # Ensure that the request's content type is JSON
    if request.headers['Content-Type'] == 'application/json':
        # Parse JSON data from the request
        my_data = request.json

        # Extract relevant information from the GitHub webhook payload
        document = extract_info_from_github_webhook(my_data)

        # Insert the extracted document into the database
        insert_document(document)

    # Return a response indicating that the data has been inserted
    return "inserted to collection"

@webhook.route('/', methods=['GET'])
def print_collection():
    # Retrieve all documents from the database and format them for display
    res = print_all_documents()
    
    # Render the 'base.html' template with the documents
    return render_template('base.html', documents=res)

# Extract required fields from the GitHub webhook payload
def extract_info_from_github_webhook(data):
    # Determine the type of GitHub event based on the payload structure
    if 'ref' in data:
        event_type = 'push'
    elif 'pull_request' in data:
        # Check if the pull request event is a merge
        if 'action' in data and data['action'] == 'closed' and data['pull_request'].get('merged'):
            event_type = 'merge'
        else:
            event_type = 'pull_request'
    else:
        event_type = 'unknown'
    
    # Print the detected event type for debugging purposes
    print(f"Event type detected: {event_type}")
    
    result = {}

    if event_type == 'push':
        # Extract and format information for a push event
        result['event_type'] = 'push'
        result['author'] = data['pusher']['name']
        result['from_branch'] = data['ref'].split('/')[-1]
        result['to_branch'] = 'N/A'  # Push event doesn't have a 'to_branch'
        result['timestamp'] = data['commits'][0]['timestamp'] if data['commits'] else 'N/A'
    
    elif event_type == 'pull_request':
        # Extract and format information for a pull request event
        result['event_type'] = 'pull_request'
        pr = data['pull_request']
        result['author'] = pr['user']['login']
        result['from_branch'] = pr['head']['ref']
        result['to_branch'] = pr['base']['ref']
        result['timestamp'] = pr['created_at']
    
    elif event_type == 'merge':
        # Extract and format information for a merge event
        result['event_type'] = 'merge'
        pr = data['pull_request']
        result['author'] = pr['user']['login']
        result['from_branch'] = pr['head']['ref']
        result['to_branch'] = pr['base']['ref']
        result['timestamp'] = pr['merged_at']
    
    else:
        # Handle unsupported event types
        print(f"Unsupported event type: {event_type}")
        raise ValueError(f"Unsupported event type: {event_type}")

    return result
