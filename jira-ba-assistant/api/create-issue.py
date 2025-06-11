import json
import os
import requests
from requests.auth import HTTPBasicAuth

def handler(request):
    if request.method != 'POST':
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
        
        # Parse request body
        body = json.loads(request.get('body', '{}'))
        project_key = body.get('project_key')
        issue_type = body.get('issue_type')
        summary = body.get('summary')
        description = body.get('description')
        assignee = body.get('assignee')
        epic_link = body.get('epic_link')
        
        if not all([project_key, issue_type, summary, description]):
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing required fields'})
            }
        
        # Create issue in Jira
        url = f"{JIRA_BASE_URL}/rest/api/3/issue"
        auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        fields = {
            'project': {'key': project_key},
            'issuetype': {'name': issue_type},
            'summary': summary,
            'description': {
                'type': 'doc',
                'version': 1,
                'content': [
                    {
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': description
                            }
                        ]
                    }
                ]
            }
        }
        
        if assignee:
            fields['assignee'] = {'accountId': assignee}
        
        if epic_link and issue_type.lower() == 'story':
            fields['parent'] = {'key': epic_link}
        
        payload = {'fields': fields}
        
        response = requests.post(url, headers=headers, auth=auth, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'success': True, 'issue_key': result['key']})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'success': False, 'error': str(e)})
        }
