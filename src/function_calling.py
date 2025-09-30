#!/usr/bin/env python3
"""
Simple Chat with Function Calling
A bare-bones chat interface with arithmetic function calling for instructional purposes.
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Define arithmetic functions
def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b."""
    if b == 0:
        return "Error: Division by zero"
    return a / b

# Define function schemas for the AI
FUNCTION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number", 
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "subtract",
            "description": "Subtract the second number from the first number",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "Number to subtract from"
                    },
                    "b": {
                        "type": "number",
                        "description": "Number to subtract"
                    }
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "divide",
            "description": "Divide the first number by the second number", 
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "Number to be divided (dividend)"
                    },
                    "b": {
                        "type": "number",
                        "description": "Number to divide by (divisor)"
                    }
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        }
    }
]

def execute_function(function_name, arguments):
    """Execute a function call and return the result."""
    if function_name == "add":
        return add(arguments["a"], arguments["b"])
    elif function_name == "subtract":
        return subtract(arguments["a"], arguments["b"])
    elif function_name == "multiply":
        return multiply(arguments["a"], arguments["b"])
    elif function_name == "divide":
        return divide(arguments["a"], arguments["b"])
    else:
        return f"Error: Unknown function {function_name}"

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
    
    print("🤖 Chat with Function Calling (Arithmetic)")
    print("Try asking me to do math like: 'What is 15 + 7?' or 'Calculate 100 divided by 4'")
    print("Type 'quit' or 'exit' to end the conversation")
    print("-" * 60)
    
    # Initialize conversation history
    messages = [
        {
            "role": "system", 
            "content": "You are a helpful assistant with access to arithmetic functions. Use the provided functions to perform calculations when asked. Always show your work by explaining what calculation you're performing."
        }
    ]
    
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
        
        # Add user message to conversation
        messages.append({"role": "user", "content": user_input})
        
        try:
            # Make API call with function tools
            response = client.chat.completions.create(
                model=ai_model,
                messages=messages,
                tools=FUNCTION_TOOLS,
                tool_choice="auto",
                max_completion_tokens=500
            )
            
            response_message = response.choices[0].message
            
            # Check if the model wants to call functions
            if response_message.tool_calls:
                print(f"\n🔧 {ai_model} is calling functions...")
                
                # Add the assistant's response to conversation
                messages.append(response_message)
                
                # Execute each function call
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"   📞 Calling {function_name}({function_args})")
                    
                    # Execute the function
                    function_result = execute_function(function_name, function_args)
                    print(f"   📊 Result: {function_result}")
                    
                    # Add function result to conversation
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(function_result)
                    })
                
                # Get final response from the model
                final_response = client.chat.completions.create(
                    model=ai_model,
                    messages=messages,
                    max_completion_tokens=500
                )
                
                final_message = final_response.choices[0].message.content
                print(f"\n🤖 {ai_model}: {final_message}")
                
                # Add final response to conversation
                messages.append({"role": "assistant", "content": final_message})
                
            else:
                # No function calls, just regular response
                ai_response = response_message.content
                print(f"\n🤖 {ai_model}: {ai_response}")
                
                # Add response to conversation
                messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()