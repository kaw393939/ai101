#!/usr/bin/env python3
"""
Simple Chat with GPT-4
A bare-bones chat interface for instructional purposes.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

def main():
    """Main chat function."""
    
    # Get API key and org ID from environment
    api_key = os.getenv("OPENAI_API_KEY")
    org_id = os.getenv("OPENAI_ORG_ID")
    ai_model = os.getenv("OPENAI_MODEL")

    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        return
    
    # Initialize OpenAI client with organization ID
    client = OpenAI(
        api_key=api_key,
        organization=org_id
    )
    
    print("🤖 Simple Chat with GPT-4")
    print("Type 'quit' or 'exit' to end the conversation")
    print("-" * 50)
    
    # Chat loop
    while True:
        # Get user input
        user_input = input("\n👤 You: ").strip()
        
        # Check for exit commands
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            # Make API call to the AI model
            response = client.chat.completions.create(
                model=ai_model,  
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant. Be concise and friendly."
                    },
                    {
                        "role": "user", 
                        "content": user_input
                    }
                ],
                max_completion_tokens=500
            )
            
            # Extract and display response
            ai_response = response.choices[0].message.content
            print(f"\n🤖 {ai_model}: {ai_response}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()