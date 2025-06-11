import json
import os
import google.generativeai as genai

def handler(request):
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Get Gemini API key
        GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
        if not GEMINI_API_KEY:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Gemini API key not configured'})
            }
        
        # Parse request body
        body = json.loads(request.get('body', '{}'))
        theme = body.get('theme', '')
        objectives = body.get('objectives', '')
        
        if not theme:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Theme is required'})
            }
        
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate content
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
        
        response = model.generate_content(prompt)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'content': response.text})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
