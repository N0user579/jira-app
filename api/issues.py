import requests
import os
import json
from requests.auth import HTTPBasicAuth
from urllib.parse import parse_qs

def handler(request):
    if request.method != 'GET':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse query parameters
        query_string = request.get('QUERY_STRING', '')
        params = parse_qs(query_string)
        project_key = params.get('project', [None])[0]
        issue_type = params.get('type', [None])[0]
        
        if not project_key:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Project key required'})
            }
        
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
        
        # Build JQL query
        jql = f"project = {project_key}"
        if issue_type:
            jql += f" AND issuetype = {issue_type}"
        jql += " ORDER BY created DESC"
        
        # Fetch issues from Jira
        url = f"{JIRA_BASE_URL}/rest/api/3/search"
        auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
        headers = {'Accept': 'application/json'}
        params = {
            'jql': jql,
            'maxResults': 50,
            'fields': 'summary,description,assignee,status,issuetype,created'
        }
        
        response = requests.get(url, headers=headers, auth=auth, params=params)
        response.raise_for_status()
        
        issues = response.json()
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(issues)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
