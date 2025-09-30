# Image Generation API Development Guide

## Overview
The OpenAI Image Generation API allows you to build applications that create and edit images using text prompts. The API uses the GPT Image model and automatically optimizes prompts for better results.

## Basic Setup

### Required Dependencies
```python
from openai import OpenAI
import base64
import os
```

### Client Initialization
```python
client = OpenAI(api_key="your_api_key")
```

## Core Implementation Patterns

### 1. Simple Image Generation
```python
def generate_image(prompt, save_path="generated_image.png"):
    """Generate a single image from a text prompt."""
    
    response = client.responses.create(
        model="gpt-5",
        input=f"Generate an image: {prompt}",
        tools=[{"type": "image_generation"}],
    )
    
    # Extract image data
    for output in response.output:
        if output.type == "image_generation_call":
            image_base64 = output.result
            
            # Save to file
            with open(save_path, "wb") as f:
                f.write(base64.b64decode(image_base64))
            
            return save_path, output.revised_prompt
    
    return None, None

# Usage
image_path, revised_prompt = generate_image("a sunset over mountains")
print(f"Saved to: {image_path}")
print(f"Revised prompt: {revised_prompt}")
```

### 2. Configurable Image Generation
```python
def generate_image_with_options(prompt, **options):
    """Generate image with custom options."""
    
    # Default options
    default_options = {
        "size": "1024x1024",
        "quality": "high", 
        "format": "png",
        "background": "auto"
    }
    
    # Merge with user options
    image_options = {**default_options, **options}
    
    response = client.responses.create(
        model="gpt-5",
        input=f"Generate an image: {prompt}",
        tools=[{
            "type": "image_generation",
            **image_options
        }],
    )
    
    return extract_image_from_response(response)

# Usage examples
generate_image_with_options("cat in space", size="1024x1536", quality="medium")
generate_image_with_options("logo design", background="transparent")
```

### 3. Multi-turn Image Editing
```python
class ImageEditor:
    def __init__(self):
        self.client = OpenAI()
        self.last_response_id = None
    
    def create_initial_image(self, prompt):
        """Create the first image in an editing session."""
        response = self.client.responses.create(
            model="gpt-5",
            input=f"Generate an image: {prompt}",
            tools=[{"type": "image_generation"}],
        )
        
        self.last_response_id = response.id
        return self.save_image_from_response(response, "initial.png")
    
    def edit_image(self, edit_instruction, save_name=None):
        """Edit the last generated image."""
        if not self.last_response_id:
            raise ValueError("No initial image created")
        
        response = self.client.responses.create(
            model="gpt-5",
            previous_response_id=self.last_response_id,
            input=f"Edit the image: {edit_instruction}",
            tools=[{"type": "image_generation"}],
        )
        
        self.last_response_id = response.id
        filename = save_name or f"edit_{response.id[:8]}.png"
        return self.save_image_from_response(response, filename)
    
    def save_image_from_response(self, response, filename):
        """Extract and save image from API response."""
        for output in response.output:
            if output.type == "image_generation_call":
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(output.result))
                return filename
        return None

# Usage
editor = ImageEditor()
editor.create_initial_image("a red car")
editor.edit_image("make it blue")
editor.edit_image("add racing stripes")
```

### 4. Streaming Image Generation
```python
def generate_image_with_streaming(prompt, partial_count=2):
    """Generate image with streaming partial results."""
    
    stream = client.images.generate(
        prompt=f"Draw {prompt}",
        model="gpt-image-1",
        stream=True,
        partial_images=partial_count,
    )
    
    partial_files = []
    
    for event in stream:
        if event.type == "image_generation.partial_image":
            idx = event.partial_image_index
            filename = f"partial_{idx}.png"
            
            image_bytes = base64.b64decode(event.b64_json)
            with open(filename, "wb") as f:
                f.write(image_bytes)
            
            partial_files.append(filename)
            print(f"Saved partial image: {filename}")
    
    return partial_files

# Usage
partials = generate_image_with_streaming("a magical forest", partial_count=3)
```

## Utility Functions

### Image Processing Helpers
```python
def image_to_base64(image_path):
    """Convert local image to base64 for API input."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def save_base64_image(base64_data, filename):
    """Save base64 image data to file."""
    with open(filename, "wb") as f:
        f.write(base64.b64decode(base64_data))

def extract_all_images(response, prefix="image"):
    """Extract all images from a response."""
    images = []
    for i, output in enumerate(response.output):
        if output.type == "image_generation_call":
            filename = f"{prefix}_{i}.png"
            save_base64_image(output.result, filename)
            images.append({
                "filename": filename,
                "revised_prompt": getattr(output, 'revised_prompt', None)
            })
    return images
```

## Best Practices

### 1. Prompt Engineering
```python
# Good prompts use action words
"Draw a realistic portrait of..."
"Create a logo featuring..."
"Edit the image to add..."

# Include style and detail specifications
"Draw a watercolor painting of a sunset with warm colors"
"Create a minimalist black and white logo"
```

### 2. Error Handling
```python
def robust_image_generation(prompt, max_retries=3):
    """Generate image with retry logic."""
    for attempt in range(max_retries):
        try:
            response = client.responses.create(
                model="gpt-5",
                input=f"Generate an image: {prompt}",
                tools=[{"type": "image_generation"}],
            )
            
            for output in response.output:
                if output.type == "image_generation_call":
                    return output.result
                    
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
    
    return None
```

### 3. Batch Processing
```python
def generate_multiple_images(prompts, output_dir="generated"):
    """Generate multiple images efficiently."""
    os.makedirs(output_dir, exist_ok=True)
    results = []
    
    for i, prompt in enumerate(prompts):
        try:
            filename = f"{output_dir}/image_{i:03d}.png"
            path, revised = generate_image(prompt, filename)
            results.append({
                "original_prompt": prompt,
                "revised_prompt": revised,
                "filename": path,
                "success": True
            })
        except Exception as e:
            results.append({
                "original_prompt": prompt,
                "error": str(e),
                "success": False
            })
    
    return results
```

## Configuration Options

### Image Parameters
- **size**: "1024x1024", "1024x1536", "1536x1024"
- **quality**: "low", "medium", "high", "auto"
- **format**: "png", "jpeg", "webp"
- **compression**: 0-100 (for JPEG/WebP)
- **background**: "transparent", "opaque", "auto"

### Model Selection
- Use **gpt-5**, **gpt-4o**, or **gpt-4.1** as mainline models
- Image generation always uses **gpt-image-1** internally

## Common Use Cases

1. **Content Creation**: Blog images, social media graphics
2. **Product Visualization**: Mockups, concept art
3. **Creative Tools**: Art generation, style transfer
4. **Iterative Design**: Logo refinement, image editing
5. **Batch Processing**: Generating variations, A/B testing visuals

## Error Handling

Always handle potential errors:
- API rate limits
- Invalid prompts
- Model availability
- File I/O operations
- Base64 encoding/decoding issues