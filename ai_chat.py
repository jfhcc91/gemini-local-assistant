import os
from openai import OpenAI
from google import genai
from dotenv import load_dotenv

# Load credentials from the secure environment file
load_dotenv()

def generate_openai_response(prompt, system_instruction):
    """Handles logic for OpenAI Models"""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Error: {str(e)}"

def generate_gemini_response(prompt, system_instruction):
    """Handles logic for Google Gemini Models"""
    try:
        # Client automatically reads GEMINI_API_KEY from environment variables
        client = genai.Client()
        
        # Combine instructions using standard Gemini syntax
        full_content = f"System Instruction: {system_instruction}\n\nUser Request: {prompt}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Blazing fast and cheap for business use
            contents=full_content
        )
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

def run_assistant(prompt, system_instruction="You are a helpful business assistant."):
    """Orchestrates which AI provider to use based on configuration"""
    provider = os.getenv("AI_PROVIDER", "openai").lower().strip()
    
    if provider == "gemini":
        return generate_gemini_response(prompt, system_instruction)
    else:
        return generate_openai_response(prompt, system_instruction)

# Testing Sandbox
if __name__ == "__main__":
    current_provider = os.getenv("AI_PROVIDER", "openai").upper()
    print(f"🤖 AI Assistant Initialized using [{current_provider}]...")
    
    sample_email = "Your software is lagging and my team is losing hours. Fix this or we want a refund."
    prompt = f"Draft a polite and reassuring response to this client email: '{sample_email}'"
    system_role = "You are an expert customer success manager."
    
    print("\n--- Generating Email Draft ---")
    draft = run_assistant(prompt, system_role)
    print(draft)