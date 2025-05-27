# Simple example of function calling using dashscope to get weather information
import json
import os
from dotenv import load_dotenv
import dashscope
from dashscope.api_entities.dashscope_response import Role

# Load environment variables
load_dotenv()

# Get API key from environment variables
dashscope.api_key = os.getenv('BL_API_KEY')

def get_current_weather(location, unit="celsius"):
    """
    Get weather information for specified location
    
    Args:
        location (str): Location name
        unit (str): Temperature unit, default is celsius
        
    Returns:
        str: Weather information in JSON format
    """
    temperature = -1
    if '大连' in location or 'Dalian' in location:
        temperature = 10
    if location == '上海':
        temperature = 36
    if location == '深圳':
        temperature = 37
        
    weather_info = {
        "location": location,
        "temperature": temperature,
        "unit": unit,
        "forecast": ["Sunny", "Light breeze"],
    }
    return json.dumps(weather_info, ensure_ascii=False)

def get_response(messages):
    """
    Get response from Qwen model
    
    Args:
        messages (list): Message list containing conversation history
        
    Returns:
        dashscope.Generation.Response: Model response object
    """
    try:
        response = dashscope.Generation.call(
            model='qwen-turbo',
            messages=messages,
            functions=functions,
            result_format='message'
        )
        return response
    except Exception as e:
        print(f"API call error: {str(e)}")
        return None

def run_conversation(query):
    """
    Run conversation flow, handle weather queries
    
    Args:
        query (str): User's query text
        
    Returns:
        dict: Final conversation result
    """
    messages = [{"role": "user", "content": query}]
    
    # First response
    response = get_response(messages)
    if not response or not response.output:
        print("Failed to get response")
        return None
        
    message = response.output.choices[0].message
    messages.append(message)
    
    # Handle function call
    if hasattr(message, 'function_call') and message.function_call:
        function_call = message.function_call
        tool_name = function_call['name']
        arguments = json.loads(function_call['arguments'])
        
        # Execute weather query function
        tool_response = get_current_weather(
            location=arguments.get('location'),
            unit=arguments.get('unit'),
        )
        
        # Add function call result to conversation history
        tool_info = {"role": "function", "name": tool_name, "content": tool_response}
        messages.append(tool_info)
        
        # Get second response
        response = get_response(messages)
        if not response or not response.output:
            print("Failed to get second response")
            return None
            
        message = response.output.choices[0].message
        return message
        
    return message

# Define available functions
functions = [
    {
        'name': 'get_current_weather',
        'description': 'Get current weather information for specified location',
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description': 'City name, e.g.: Dalian, Shanghai, Shenzhen'
                },
                'unit': {
                    'type': 'string',
                    'enum': ['celsius', 'fahrenheit'],
                    'description': 'Temperature unit'
                }
            },
            'required': ['location']
        }
    }
]

if __name__ == "__main__":
    # Test examples
    test_queries = [
        "大连的天气怎样",
        "上海现在天气如何",
        "深圳今天天气怎么样"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = run_conversation(query)
        if result:
            print(f"Result: {result.content}")
        else:
            print("Query failed") 