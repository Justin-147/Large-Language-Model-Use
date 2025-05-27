# Simple sentiment analysis example using dashscope with prompt
import json
import os
from dotenv import load_dotenv
import dashscope
from dashscope.api_entities.dashscope_response import Role

# Load environment variables
load_dotenv()

# Get API key from environment variables
dashscope.api_key = os.getenv('BL_API_KEY')

def get_response(messages):
    """
    Get response from Qwen model
    
    Args:
        messages (list): Message list containing conversation history
        
    Returns:
        dashscope.Generation.Response: Model response object
    """
    response = dashscope.Generation.call(
        model='qwen-turbo', # model='deepseek-r1'
        messages=messages,
        result_format='message'  # Set output format to message
    )
    return response

def analyze_sentiment(text):
    """
    Analyze text sentiment
    
    Args:
        text (str): Text to analyze
        
    Returns:
        str: 'Positive' or 'Negative'
    """
    messages = [
        {"role": "system", "content": "You are a sentiment analyst. Help me determine if the product review is positive or negative. Please respond with a single word: Positive or Negative"},
        {"role": "user", "content": text}
    ]
    
    response = get_response(messages)
    return response.output.choices[0].message.content

if __name__ == "__main__":
    # Test example
    review = '这款音效特别好,给你意想不到的音质。'
    sentiment = analyze_sentiment(review)
    print(f"Review: {review}")
    print(f"Sentiment analysis result: {sentiment}") 