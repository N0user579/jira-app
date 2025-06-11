# Jira Business Analyst Assistant

A Flask-based web application that helps business analysts create user stories and epics using AI-powered content generation with Google Gemini, integrated with Jira for seamless project management.

## Features

- **AI-Powered Content Generation**: Use Google Gemini to generate detailed user stories and epics
- **Jira Integration**: Create issues directly in your Jira projects
- **Project Management**: View and manage multiple Jira projects
- **User Assignment**: Assign stories and epics to team members
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: See recently created issues and project status

## Setup Instructions

### Prerequisites

- Python 3.8+
- Jira account with API access
- Google Gemini API key

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Set up environment variables**:
   Copy `.env.example` to `.env` and fill in your credentials:
   \`\`\`bash
   cp .env.example .env
   \`\`\`

   Edit `.env` with your actual values:
   \`\`\`
   JIRA_BASE_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@company.com
   JIRA_API_TOKEN=your-jira-api-token
   GEMINI_API_KEY=your-gemini-api-key
   FLASK_SECRET_KEY=your-secret-key-here
   \`\`\`

### Getting API Credentials

#### Jira API Token
1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a label and copy the generated token
4. Use your Jira email and this token for authentication

#### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key for use in your environment variables

### Running the Application

1. **Start the Flask server**:
   \`\`\`bash
   python app.py
   \`\`\`

2. **Access the application**:
   Open your browser and go to `http://localhost:5000`

## Usage

### Creating User Stories

1. Select a project from the dashboard
2. Click "Generate User Story" in the AI Assistant panel
3. Provide requirements and context
4. Click "Generate" to get AI-powered content
5. Review and edit the generated content
6. Click "Use This Content" to create the story in Jira

### Creating Epics

1. Select a project from the dashboard
2. Click "Generate Epic" in the AI Assistant panel
3. Provide theme and business objectives
4. Click "Generate" to get AI-powered content
5. Review and edit the generated content
6. Click "Use This Content" to create the epic in Jira

### Manual Creation

You can also create stories and epics manually using the "Create User Story" and "Create Epic" buttons in the project header.

## Project Structure

\`\`\`
jira-ba-assistant/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── style.css     # Application styles
│   └── js/
│       └── main.js       # Frontend JavaScript
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Dashboard page
    └── project.html      # Project management page
\`\`\`

## API Endpoints

- `GET /` - Main dashboard
- `GET /project/<project_key>` - Project dashboard
- `POST /generate-story` - Generate user story with AI
- `POST /generate-epic` - Generate epic with AI
- `POST /create-issue` - Create issue in Jira
- `GET /api/projects` - Get all projects
- `GET /api/users/<project_key>` - Get project users

## Troubleshooting

### Common Issues

1. **"No Projects Found"**
   - Check your Jira credentials
   - Ensure your Jira user has access to projects
   - Verify the Jira base URL format

2. **"Error generating content"**
   - Check your Gemini API key
   - Ensure you have API quota available
   - Check internet connectivity

3. **"Failed to create issue"**
   - Verify Jira permissions
   - Check if the project allows the issue type
   - Ensure required fields are provided

### Debug Mode

To enable debug mode, set `FLASK_ENV=development` in your `.env` file. This will provide detailed error messages and auto-reload on code changes.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
