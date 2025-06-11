import requests
import os
import json
from requests.auth import HTTPBasicAuth

def handler(request):
    if request.method != 'GET':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Get configuration from environment
        JIRA_BASE_URL = os.environ.get('JIRA_BASE_URL')
        JIRA_EMAIL = os.environ.get('JIRA_EMAIL')
        JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN')
        
        if not all([JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Jira configuration missing'})
            }
        
        # Fetch projects from Jira
        url = f"{JIRA_BASE_URL}/rest/api/3/project"
        auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
        headers = {'Accept': 'application/json'}
        
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()
        
        projects = response.json()
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(projects)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
