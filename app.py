from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import requests
import json
import os
from datetime import datetime
import google.generativeai as genai
from requests.auth import HTTPBasicAuth
import base64

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here')

# Configuration
JIRA_BASE_URL = os.environ.get('JIRA_BASE_URL')
JIRA_EMAIL = os.environ.get('JIRA_EMAIL')
JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Initialize Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

class JiraAPI:
    def __init__(self):
        self.base_url = JIRA_BASE_URL
        self.auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def get_projects(self):
        """Get all accessible projects"""
        try:
            url = f"{self.base_url}/rest/api/3/project"
            response = requests.get(url, headers=self.headers, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return []
    
    def get_project_users(self, project_key):
        """Get users who can be assigned issues in a project"""
        try:
            url = f"{self.base_url}/rest/api/3/user/assignable/search"
            params = {'project': project_key}
            response = requests.get(url, headers=self.headers, auth=self.auth, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
    
    def get_issue_types(self, project_key):
        """Get available issue types for a project"""
        try:
            url = f"{self.base_url}/rest/api/3/project/{project_key}"
            response = requests.get(url, headers=self.headers, auth=self.auth)
            response.raise_for_status()
            project_data = response.json()
            return project_data.get('issueTypes', [])
        except Exception as e:
            print(f"Error fetching issue types: {e}")
            return []
    
    def create_issue(self, project_key, issue_type, summary, description, assignee=None, epic_link=None):
        """Create a new issue in Jira"""
        try:
            url = f"{self.base_url}/rest/api/3/issue"
            
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
            
            response = requests.post(url, headers=self.headers, auth=self.auth, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error creating issue: {e}")
            return None
    
    def get_issues(self, project_key, issue_type=None):
        """Get issues from a project"""
        try:
            jql = f"project = {project_key}"
            if issue_type:
                jql += f" AND issuetype = {issue_type}"
            jql += " ORDER BY created DESC"
            
            url = f"{self.base_url}/rest/api/3/search"
            params = {
                'jql': jql,
                'maxResults': 50,
                'fields': 'summary,description,assignee,status,issuetype,created'
            }
            
            response = requests.get(url, headers=self.headers, auth=self.auth, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching issues: {e}")
            return {'issues': []}

jira_api = JiraAPI()

def generate_with_gemini(prompt):
    """Generate content using Gemini AI"""
    try:
        if not GEMINI_API_KEY:
            return "Gemini API key not configured"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error with Gemini: {e}")
        return f"Error generating content: {str(e)}"

@app.route('/')
def index():
    """Main dashboard"""
    projects = jira_api.get_projects()
    return render_template('index.html', projects=projects)

@app.route('/project/<project_key>')
def project_dashboard(project_key):
    """Project-specific dashboard"""
    project_name = request.args.get('name', project_key)
    users = jira_api.get_project_users(project_key)
    issue_types = jira_api.get_issue_types(project_key)
    issues = jira_api.get_issues(project_key)
    
    return render_template('project.html', 
                         project_key=project_key, 
                         project_name=project_name,
                         users=users, 
                         issue_types=issue_types,
                         issues=issues.get('issues', []))

@app.route('/generate-story', methods=['POST'])
def generate_story():
    """Generate user story using Gemini"""
    data = request.json
    requirements = data.get('requirements', '')
    context = data.get('context', '')
    
    prompt = f"""
    As a business analyst, create a detailed user story based on the following requirements:
    
    Requirements: {requirements}
    Context: {context}
    
    Please provide:
    1. A clear user story in the format: "As a [user type], I want [functionality] so that [benefit]"
    2. Acceptance criteria (3-5 bullet points)
    3. Definition of done
    4. Any assumptions or dependencies
    
    Format the response clearly with headers for each section.
    """
    
    generated_content = generate_with_gemini(prompt)
    return jsonify({'content': generated_content})

@app.route('/generate-epic', methods=['POST'])
def generate_epic():
    """Generate epic using Gemini"""
    data = request.json
    theme = data.get('theme', '')
    objectives = data.get('objectives', '')
    
    prompt = f"""
    As a business analyst, create a comprehensive epic based on the following:
    
    Theme: {theme}
    Business Objectives: {objectives}
    
    Please provide:
    1. Epic title and description
    2. Business value and objectives
    3. Success criteria
    4. High-level user stories that would be part of this epic (3-5 stories)
    5. Estimated timeline considerations
    6. Key stakeholders
    
    Format the response clearly with headers for each section.
    """
    
    generated_content = generate_with_gemini(prompt)
    return jsonify({'content': generated_content})

@app.route('/create-issue', methods=['POST'])
def create_issue():
    """Create issue in Jira"""
    data = request.json
    
    result = jira_api.create_issue(
        project_key=data['project_key'],
        issue_type=data['issue_type'],
        summary=data['summary'],
        description=data['description'],
        assignee=data.get('assignee'),
        epic_link=data.get('epic_link')
    )
    
    if result:
        return jsonify({'success': True, 'issue_key': result['key']})
    else:
        return jsonify({'success': False, 'error': 'Failed to create issue'})

@app.route('/api/projects')
def api_projects():
    """API endpoint for projects"""
    projects = jira_api.get_projects()
    return jsonify(projects)

@app.route('/api/users/<project_key>')
def api_users(project_key):
    """API endpoint for project users"""
    users = jira_api.get_project_users(project_key)
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
