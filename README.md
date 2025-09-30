# AI Work 601 - AI Development Toolkit

A comprehensive Python repository featuring practical AI applications and development tools. This project demonstrates various AI capabilities including function calling, image generation, and speech synthesis using OpenAI's APIs.

## 🚀 Features

### **Core AI Applications**
- 🧮 **Function Calling Demo** - Interactive chat with arithmetic function calling
- 🎨 **Image Generation REPL** - Generate and manage AI-created images
- 🗣️ **Speech Generation REPL** - Create transcripts and convert to audio

### **Development Environment**
- 🐍 **Python 3.9+** with virtual environment support
- ✅ **pytest** testing framework with coverage
- � **Multiple AI Providers** - OpenAI, Anthropic, Groq support
- 🔧 **Environment Configuration** - Secure API key management
- 📁 **Organized Output** - Smart file naming and folder structure
- � **Reference Documentation** - Detailed guides for each AI feature

## 📋 Project Structure

```
aiwork601/
├── src/                          # Source applications
│   ├── function_calling.py      # Interactive function calling demo
│   ├── images.py                 # Image generation REPL
│   └── speech.py                 # Speech generation REPL
├── references/                   # Development documentation
│   ├── function_calling.md      # Function calling guide
│   ├── images.md                 # Image generation guide
│   └── audio.md                  # Audio/speech development guide
├── tests/                        # Test suite
│   ├── __init__.py
│   └── conftest.py
├── images/                       # Generated images output
├── audio/                        # Generated speech output
├── .github/                      # GitHub configuration
│   └── copilot-instructions.md
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
├── pytest.ini                   # Test configuration
└── README.md                     # This file
```

## 🛠️ Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd aiwork601

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=your_openai_key_here
# OPENAI_ORG_ID=your_org_id_here (optional)
# OPENAI_MODEL=gpt-4o (or your preferred model)
```

### 3. Run Applications

**Function Calling Demo:**
```bash
python src/function_calling.py
```
Interactive chat that can perform arithmetic calculations using AI function calling.

**Image Generation:**
```bash
python src/images.py
```
Generate images from text descriptions with smart file management.

**Speech Generation:**
```bash
python src/speech.py
```
Create transcripts and convert them to audio with multiple voice options.

## 📱 Application Features

### Function Calling (`src/function_calling.py`)
- **Interactive Chat Interface** - Natural language math operations
- **Arithmetic Functions** - Add, subtract, multiply, divide
- **Error Handling** - Division by zero protection
- **Function Tools Schema** - Demonstrates OpenAI function calling patterns

**Example Usage:**
```
User: "What's 15 times 8 plus 20?"
AI: I'll calculate that for you: (15 × 8) + 20 = 120 + 20 = 140
```

### Image Generation (`src/images.py`)
- **Smart File Naming** - Prevents duplicates with hash + timestamp
- **Image Management** - View recent images, clear storage
- **File Size Reporting** - Track generated image sizes
- **Prompt Optimization** - AI-enhanced image descriptions

**Commands:**
- `help` - Show available commands
- `recent` - List recent images
- `clear` - Delete all images
- `quit` - Exit application

### Speech Generation (`src/speech.py`)
- **Transcript Generation** - AI creates natural-sounding content
- **Text-to-Speech** - Convert transcripts to audio files
- **Voice Selection** - 6 different voice options (alloy, echo, fable, onyx, nova, shimmer)
- **Task Organization** - Each generation creates organized folder with transcript + audio
- **Metadata Tracking** - JSON files with word counts, timestamps, original prompts

**Commands:**
- `help` - Show available commands
- `voices` - List available voices
- `voice <name>` - Change current voice
- `recent` - Show recent speech tasks
- `clear` - Delete all tasks
- `quit` - Exit application

## 🔧 Configuration

### Environment Variables (`.env`)
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_ORG_ID=org-your-org-id-here    # Optional
OPENAI_MODEL=gpt-4o                    # Default: gpt-4o

# Logging (optional)
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Supported AI Models
- **OpenAI**: `gpt-4o`, `gpt-4`, `gpt-3.5-turbo`
- **Image Generation**: Uses OpenAI's DALL-E via responses API
- **Text-to-Speech**: `tts-1`, `tts-1-hd`

### Voice Options (Speech Generation)
- **alloy** - Balanced, natural voice
- **echo** - Clear, professional voice
- **fable** - Warm, storytelling voice
- **onyx** - Deep, authoritative voice
- **nova** - Bright, energetic voice
- **shimmer** - Soft, gentle voice

## 📂 Output Organization

### Images (`images/` folder)
```
images/
├── sunset_over_mountains_20240929_143022_a1b2c3d4.png
├── golden_retriever_park_20240929_143155_e5f6g7h8.png
└── ...
```

### Speech Tasks (`audio/` folder)
```
audio/
├── write_story_brave_knight_20240929_143300_i9j0k1l2/
│   ├── transcript.json
│   └── audio.mp3
├── explain_photosynthesis_20240929_143445_m3n4o5p6/
│   ├── transcript.json
│   └── audio.mp3
└── ...
```

## 🧪 Development

### Running Tests
```bash
# Install development dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=src
```

### Code Quality
The project includes configuration for:
- **pytest** - Testing framework
- **Virtual environment** - Isolated dependencies
- **Environment variables** - Secure configuration
- **Modular design** - Separate applications for different AI tasks

## 📚 Documentation

Detailed guides are available in the `references/` folder:
- **function_calling.md** - Function calling patterns and examples
- **images.md** - Image generation development guide
- **audio.md** - Speech/audio application development

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Configure your environment** (copy `.env.example` to `.env`)
4. **Test your changes** (`pytest`)
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to the branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**API Key Errors:**
- Ensure your `.env` file has valid `OPENAI_API_KEY`
- Check that your OpenAI account has sufficient credits

**Model Compatibility:**
- Some models (like GPT-5) may have specific parameter requirements
- Try switching to `gpt-4o` if you encounter model-specific errors

**File Permissions:**
- Ensure the application can create `images/` and `audio/` directories
- Check write permissions in the project folder

### Getting Help

1. **Check the documentation** in `references/` folder
2. **Review error messages** - applications provide detailed error information
3. **Verify environment configuration** - ensure `.env` is properly configured
4. **Test with simple prompts** first before complex requests

---

Built with ❤️ for AI development and experimentation.