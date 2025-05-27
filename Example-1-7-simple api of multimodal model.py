# Simple example of using dashscope multimodal model to extract text content from images
import json
import os
import base64
import re
from dotenv import load_dotenv
import dashscope
from dashscope.api_entities.dashscope_response import Role

# Load environment variables
load_dotenv()

# Get API key from environment variables
dashscope.api_key = os.getenv('BL_API_KEY')

def image_to_base64(image_path):
    """
    Convert local image to base64 encoding
    
    Args:
        image_path (str): Local image path
        
    Returns:
        str: Base64 encoded image string in format "data:image/jpeg;base64,xxx..."
    """
    try:
        with open(image_path, 'rb') as image_file:
            # Get image format
            image_format = os.path.splitext(image_path)[1].lower().replace('.', '')
            if image_format == 'jpg':
                image_format = 'jpeg'
                
            # Read image and convert to base64
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/{image_format};base64,{encoded_string}"
    except Exception as e:
        print(f"Image conversion failed: {str(e)}")
        return None

def get_response(messages):
    """
    Get response from Qwen vision model
    
    Args:
        messages (list): Message list containing image and text content
        
    Returns:
        dashscope.MultiModalConversation.Response: Model response object
    """
    try:
        response = dashscope.MultiModalConversation.call(
            model='qwen-vl-plus',
            messages=messages
        )
        return response
    except Exception as e:
        print(f"API call error: {str(e)}")
        return None

def extract_table_from_image(image_path_or_url, prompt="This is an image, please extract the text content from it. Only output the extracted text content, do not output any other content"):
    """
    Extract content from image
    
    Args:
        image_path_or_url (str): Local image path or URL
        prompt (str): Prompt text to guide model on how to process the image
        
    Returns:
        str: Raw content returned by the model
    """
    # Check if it's a local image or URL
    if os.path.exists(image_path_or_url):
        # Local image, convert to base64
        image_content = image_to_base64(image_path_or_url)
        if not image_content:
            print("Image conversion failed")
            return None
    else:
        # URL image, use directly
        image_content = image_path_or_url
    
    # Build message content
    content = [
        {'image': image_content},  # Image content (base64 or URL)
        {'text': prompt}  # Prompt text
    ]
    
    # Build message list
    messages = [{"role": "user", "content": content}]
    
    # Get response
    response = get_response(messages)
    if not response or not response.output:
        print("Failed to get response")
        return None
        
    # Return raw content from model
    try:
        text_content = response.output.choices[0].message.content[0]['text']
        print("\nRaw content from model:")
        print(text_content)
        return text_content
    except Exception as e:
        print(f"Error processing response content: {str(e)}")
        return None

if __name__ == "__main__":
    # Test examples
    test_images = [
        "https://aiwucai.oss-cn-huhehaote.aliyuncs.com/pdf_table.jpg",  # Online image
        "D:/1.png"  # Local image
    ]
    
    for image in test_images:
        print(f"\nProcessing image: {image}")
        # Check if it's a local file
        if os.path.exists(image):
            print("Processing local image...")
        else:
            print("Processing online image...")
            
        result = extract_table_from_image(image)
        
        if result:
            print("\nExtracted content:")
            print(result)
        else:
            print("Content extraction failed") 