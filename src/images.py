 #!/usr/bin/env python3
"""
Image Generation REPL
A chat interface that generates images based on user input using GPT-5.
"""

import os
import base64
import re
import hashlib
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


def create_smart_filename(prompt, base_dir="images"):
    """
    Create a smart filename based on the prompt to avoid duplicates.
    Uses a combination of cleaned prompt text, timestamp, and hash.
    """
    # Clean the prompt for filename use
    clean_prompt = re.sub(r'[^\w\s-]', '', prompt.lower())
    clean_prompt = re.sub(r'[-\s]+', '_', clean_prompt)
    clean_prompt = clean_prompt[:50]  # Limit length
    
    # Create a short hash of the full prompt for uniqueness
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Combine elements
    filename = f"{clean_prompt}_{timestamp}_{prompt_hash}.png"
    
    # Ensure the images directory exists
    Path(base_dir).mkdir(exist_ok=True)
    
    return os.path.join(base_dir, filename)


def generate_image(client, prompt, model):
    """Generate an image using the OpenAI API."""
    try:
        print(f"🎨 Generating image: '{prompt}'...")
        
        response = client.responses.create(
            model=model,
            input=f"Generate an image: {prompt}",
            tools=[{"type": "image_generation"}],
        )
        
        # Extract image data and metadata
        for output in response.output:
            if output.type == "image_generation_call":
                return {
                    "image_data": output.result,
                    "revised_prompt": getattr(output, 'revised_prompt', prompt),
                    "success": True
                }
        
        return {"success": False, "error": "No image generated in response"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def save_image(image_data, filename):
    """Save base64 image data to file."""
    try:
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_data))
        return True
    except Exception as e:
        print(f"❌ Error saving image: {e}")
        return False


def list_recent_images(base_dir="images", count=5):
    """List the most recently created images."""
    if not os.path.exists(base_dir):
        return []
    
    # Get all PNG files and sort by modification time
    image_files = []
    for file in Path(base_dir).glob("*.png"):
        image_files.append((file.stat().st_mtime, file.name))
    
    # Sort by time (newest first) and return top 'count'
    image_files.sort(reverse=True)
    return [name for _, name in image_files[:count]]


def display_help():
    """Display help information."""
    help_text = """
🎨 Image Generation Commands:
    
    • Just type what you want to see: "a sunset over mountains"
    • Be descriptive: "a realistic photo of a golden retriever in a park"
    • Specify style: "a watercolor painting of flowers"
    • Ask for edits: "the same image but make it nighttime"
    
📋 Special Commands:
    • 'help' - Show this help
    • 'recent' - Show recent images
    • 'clear' - Clear images folder
    • 'quit' or 'exit' - Exit the program
    
💡 Tips:
    • Use descriptive language for better results
    • Specify art styles, colors, lighting, etc.
    • The AI will optimize your prompt automatically
    """
    print(help_text)


def clear_images(base_dir="images"):
    """Clear all images from the images directory."""
    if not os.path.exists(base_dir):
        print("📁 No images directory found.")
        return
    
    image_files = list(Path(base_dir).glob("*.png"))
    if not image_files:
        print("📁 No images to clear.")
        return
    
    confirm = input(f"🗑️  Are you sure you want to delete {len(image_files)} images? (y/N): ")
    if confirm.lower() in ['y', 'yes']:
        for file in image_files:
            file.unlink()
        print(f"🗑️  Deleted {len(image_files)} images.")
    else:
        print("❌ Cancelled.")


def main():
    """Main image generation REPL."""
    
    # Get API credentials from environment
    api_key = os.getenv("OPENAI_API_KEY")
    org_id = os.getenv("OPENAI_ORG_ID")
    ai_model = os.getenv("OPENAI_MODEL", "gpt-5")

    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        return
    
    # Initialize OpenAI client
    client = OpenAI(
        api_key=api_key,
        organization=org_id
    )
    
    # Welcome message
    print("🎨 AI Image Generator (GPT-5)")
    print("Type what you want to see and I'll generate an image!")
    print("Type 'help' for commands or 'quit' to exit")
    print("-" * 60)
    
    # Show recent images if any exist
    recent = list_recent_images()
    if recent:
        print(f"📸 Recent images: {', '.join(recent[:3])}")
        if len(recent) > 3:
            print(f"   ... and {len(recent) - 3} more")
    
    print()
    
    # Main REPL loop
    while True:
        try:
            # Get user input
            user_input = input("🎨 Describe your image: ").strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("👋 Goodbye!")
                break
            
            elif user_input.lower() == 'help':
                display_help()
                continue
            
            elif user_input.lower() == 'recent':
                recent = list_recent_images(count=10)
                if recent:
                    print("� Recent images:")
                    for i, img in enumerate(recent, 1):
                        print(f"   {i}. {img}")
                else:
                    print("📁 No images found.")
                continue
            
            elif user_input.lower() == 'clear':
                clear_images()
                continue
            
            # Generate image
            result = generate_image(client, user_input, ai_model)
            
            if result["success"]:
                # Create smart filename
                filename = create_smart_filename(user_input)
                
                # Save image
                if save_image(result["image_data"], filename):
                    print(f"✅ Image saved: {filename}")
                    
                    # Show revised prompt if different
                    if result.get("revised_prompt") and result["revised_prompt"] != user_input:
                        print(f"🔄 Revised prompt: {result['revised_prompt']}")
                    
                    # Show file size
                    file_size = os.path.getsize(filename)
                    print(f"📊 File size: {file_size:,} bytes")
                else:
                    print("❌ Failed to save image")
            else:
                print(f"❌ Error generating image: {result['error']}")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()