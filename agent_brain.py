import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class AgentBrain:
    """
    The Reasoning Engine. 
    It takes raw data and turns it into a professional audit report.
    """
    def __init__(self):
        # Using Gemini 1.5 Flash for the free tier
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_audit_report(self, user_query, data):
        prompt = f"""
        You are FiscalPulse, a professional Autonomous Tax Auditor.
        
        USER REQUEST: {user_query}
        
        FACTS (From Postgres):
        {data['transactions']}
        
        KNOWLEDGE (From Tax Policy):
        {data['rules']}
        
        INSTRUCTIONS:
        - Compare each transaction to the policy rules.
        - Identify which items are 100% deductible.
        - Flag any items that are 'Personal' or exceed the limits.
        - Provide a final total for suggested deductions.
        - Be precise and professional.
        """
        
        response = self.model.generate_content(prompt)
        return response.text