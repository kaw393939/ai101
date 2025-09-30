#!/usr/bin/env python3
"""
Speech Generation REPL
A chat interface that generates transcripts and converts them to audio using AI.
"""

import os
import re
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


def create_task_folder(prompt, base_dir="audio"):
    """
    Create a task folder based on the prompt to organize transcript and audio files.
    Uses a combination of cleaned prompt text, timestamp, and hash.
    """
    # Clean the prompt for folder name use
    clean_prompt = re.sub(r'[^\w\s-]', '', prompt.lower())
    clean_prompt = re.sub(r'[-\s]+', '_', clean_prompt)
    clean_prompt = clean_prompt[:30]  # Limit length for folder name
    
    # Create a short hash of the full prompt for uniqueness
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Combine elements
    folder_name = f"{clean_prompt}_{timestamp}_{prompt_hash}"
    
    # Create the full path
    task_folder = os.path.join(base_dir, folder_name)
    Path(task_folder).mkdir(parents=True, exist_ok=True)
    
    return task_folder


def generate_transcript(client, prompt, model):
    """Generate a transcript using the OpenAI API."""
    try:
        print(f"📝 Generating transcript for: '{prompt}'...")
        print(f"🤖 Using model: {model}")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant that creates well-structured, engaging content based on user prompts. Generate clear, natural-sounding text that would work well as a spoken transcript."
                },
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=2000  # Increased token limit
            # Removed temperature parameter for GPT-5 compatibility
        )
        
        print(f"📊 Response received, usage: {response.usage}")
        transcript = response.choices[0].message.content
        
        # Debug: Show raw response before stripping
        print(f"📋 Raw response (before strip): '{transcript}'")
        print(f"📏 Raw response length: {len(transcript) if transcript else 0}")
        
        transcript = transcript.strip() if transcript else ""
        
        # Debug: Check if transcript is empty
        if not transcript:
            print(f"⚠️  Warning: Generated transcript is empty after stripping!")
            print(f"📋 Content was: '{response.choices[0].message.content}'")
            print(f"🔍 Response object: {response.choices[0]}")
            return {"success": False, "error": "Generated transcript is empty"}
        
        print(f"✅ Generated transcript ({len(transcript)} characters)")
        
        return {
            "transcript": transcript,
            "success": True
        }
        
    except Exception as e:
        print(f"🔥 Exception in generate_transcript: {e}")
        return {"success": False, "error": str(e)}


def generate_and_save_audio(client, transcript, audio_path, voice="alloy"):
    """Generate audio from transcript and save to file."""
    try:
        print(f"🔊 Generating audio with voice '{voice}'...")
        
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=transcript
        )
        
        # Save audio file
        with open(audio_path, "wb") as f:
            f.write(response.content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating/saving audio: {e}")
        return False


def save_transcript(transcript, transcript_path, original_prompt):
    """Save transcript and metadata to JSON file."""
    try:
        transcript_data = {
            "original_prompt": original_prompt,
            "transcript": transcript,
            "generated_at": datetime.now().isoformat(),
            "word_count": len(transcript.split())
        }
        
        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(transcript_data, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving transcript: {e}")
        return False


def list_recent_tasks(base_dir="audio", count=5):
    """List the most recently created speech tasks."""
    if not os.path.exists(base_dir):
        return []
    
    # Get all task folders and sort by modification time
    task_folders = []
    for folder in Path(base_dir).iterdir():
        if folder.is_dir():
            task_folders.append((folder.stat().st_mtime, folder.name))
    
    # Sort by time (newest first) and return top 'count'
    task_folders.sort(reverse=True)
    return [name for _, name in task_folders[:count]]


def display_help():
    """Display help information."""
    help_text = """
🗣️  Speech Generation Commands:
    
    • Tell me what to create: "Write a story about a brave knight"
    • Ask for specific content: "Create a product description for a new phone"
    • Request educational content: "Explain how photosynthesis works"
    • Generate creative content: "Write a poem about the ocean"
    
📋 Special Commands:
    • 'help' - Show this help
    • 'recent' - Show recent speech tasks
    • 'clear' - Clear audio folder
    • 'voices' - Show available voices
    • 'voice <name>' - Change voice (alloy, echo, fable, onyx, nova, shimmer)
    • 'quit' or 'exit' - Exit the program
    
💡 Tips:
    • Be specific about the type of content you want
    • The AI will create natural-sounding text for speech
    • Both transcript and audio files are saved for each task
    """
    print(help_text)


def clear_audio_tasks(base_dir="audio"):
    """Clear all audio tasks from the audio directory."""
    if not os.path.exists(base_dir):
        print("📁 No audio directory found.")
        return
    
    task_folders = [folder for folder in Path(base_dir).iterdir() if folder.is_dir()]
    if not task_folders:
        print("📁 No audio tasks to clear.")
        return
    
    confirm = input(f"🗑️  Are you sure you want to delete {len(task_folders)} audio tasks? (y/N): ")
    if confirm.lower() in ['y', 'yes']:
        for folder in task_folders:
            shutil.rmtree(folder)
        print(f"🗑️  Deleted {len(task_folders)} audio tasks.")
    else:
        print("❌ Cancelled.")


def show_available_voices():
    """Show available TTS voices."""
    voices = {
        "alloy": "Balanced, natural voice",
        "echo": "Clear, professional voice", 
        "fable": "Warm, storytelling voice",
        "onyx": "Deep, authoritative voice",
        "nova": "Bright, energetic voice",
        "shimmer": "Soft, gentle voice"
    }
    
    print("🎤 Available Voices:")
    for voice, description in voices.items():
        print(f"   • {voice}: {description}")
    print("\n💡 Use 'voice <name>' to change voice (e.g., 'voice fable')")


def main():
    """Main speech generation REPL."""
    
    # Get API credentials from environment
    api_key = os.getenv("OPENAI_API_KEY")
    org_id = os.getenv("OPENAI_ORG_ID")
    ai_model = os.getenv("OPENAI_MODEL", "gpt-4o")  # Changed default to gpt-4o

    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        return
    
    print(f"🤖 Using AI model: {ai_model}")
    
    # Initialize OpenAI client
    client = OpenAI(
        api_key=api_key,
        organization=org_id
    )
    
    # Default voice
    current_voice = "alloy"
    
    # Welcome message
    print("🗣️  AI Speech Generator")
    print("Tell me what content to create and I'll generate transcript + audio!")
    print("Type 'help' for commands or 'quit' to exit")
    print("-" * 60)
    
    # Show recent tasks if any exist
    recent = list_recent_tasks()
    if recent:
        print(f"📁 Recent tasks: {', '.join(recent[:3])}")
        if len(recent) > 3:
            print(f"   ... and {len(recent) - 3} more")
    
    print(f"🎤 Current voice: {current_voice}")
    print()
    
    # Main REPL loop
    while True:
        try:
            # Get user input
            user_input = input("📝 What content should I create? ").strip()
            
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
                recent = list_recent_tasks(count=10)
                if recent:
                    print("📁 Recent tasks:")
                    for i, task in enumerate(recent, 1):
                        print(f"   {i}. {task}")
                else:
                    print("📁 No tasks found.")
                continue
            
            elif user_input.lower() == 'clear':
                clear_audio_tasks()
                continue
            
            elif user_input.lower() == 'voices':
                show_available_voices()
                continue
            
            elif user_input.lower().startswith('voice '):
                voice_name = user_input[6:].strip().lower()
                valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
                if voice_name in valid_voices:
                    current_voice = voice_name
                    print(f"🎤 Voice changed to: {current_voice}")
                else:
                    print(f"❌ Invalid voice. Choose from: {', '.join(valid_voices)}")
                continue
            
            # Generate transcript
            result = generate_transcript(client, user_input, ai_model)
            
            if result["success"]:
                transcript = result["transcript"]
                
                # Safety check: ensure transcript is not empty
                if not transcript or len(transcript.strip()) == 0:
                    print("❌ Error: Generated transcript is empty, cannot create audio")
                    continue
                
                # Create task folder
                task_folder = create_task_folder(user_input)
                
                # Define file paths
                transcript_path = os.path.join(task_folder, "transcript.json")
                audio_path = os.path.join(task_folder, "audio.mp3")
                
                print(f"📁 Created task folder: {os.path.basename(task_folder)}")
                
                # Save transcript
                if save_transcript(transcript, transcript_path, user_input):
                    print(f"✅ Transcript saved: transcript.json")
                    print(f"📊 Word count: {len(transcript.split())} words")
                    
                    # Generate and save audio
                    if generate_and_save_audio(client, transcript, audio_path, current_voice):
                        print(f"✅ Audio saved: audio.mp3")
                        
                        # Show file sizes
                        audio_size = os.path.getsize(audio_path)
                        transcript_size = os.path.getsize(transcript_path)
                        print(f"📊 Audio size: {audio_size:,} bytes")
                        print(f"📊 Transcript size: {transcript_size:,} bytes")
                        
                        # Show preview of transcript
                        preview = transcript[:200] + "..." if len(transcript) > 200 else transcript
                        print(f"📄 Preview: {preview}")
                    else:
                        print("❌ Failed to generate/save audio")
                else:
                    print("❌ Failed to save transcript")
            else:
                print(f"❌ Error generating transcript: {result['error']}")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
