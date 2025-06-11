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
        requirements = body.get('requirements', '')
        context = body.get('context', '')
        
        if not requirements:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Requirements are required'})
            }
        
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate content
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
