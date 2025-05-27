# Simple example of function calling using dashscope to get database server status
import json
import os
import random
from dotenv import load_dotenv
import dashscope
from dashscope.api_entities.dashscope_response import Role

# Load environment variables
load_dotenv()

# Get API key from environment variables
dashscope.api_key = os.getenv('BL_API_KEY')

def get_current_status():
    """
    Simulate getting current database server status
    Returns: connection count, CPU usage, memory usage
    """
    # Generate mock data
    connections = random.randint(10, 100)
    cpu_usage = round(random.uniform(1, 100), 1)
    memory_usage = round(random.uniform(10, 100), 1)
    
    status_info = {
        "Connection Count": connections,
        "CPU Usage": f"{cpu_usage}%",
        "Memory Usage": f"{memory_usage}%"
    }
    return json.dumps(status_info, ensure_ascii=False)

def get_response(messages, tools):
    """
    Get response from Qwen model
    
    Args:
        messages (list): Message list
        tools (list): Tool list
        
    Returns:
        dashscope.Generation.Response: Model response object
    """
    try:
        response = dashscope.Generation.call(
            model='qwen-turbo',
            messages=messages,
            tools=tools,
            result_format='message'
        )
        return response
    except Exception as e:
        print(f"API call error: {str(e)}")
        return None

def analyze_alert(alert_content):
    """
    Analyze alert content
    
    Args:
        alert_content (str): Alert content
        
    Returns:
        str: Analysis result
    """
    # Define available tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_status",
                "description": "Get current database server performance metrics, including: connection count, CPU usage, memory usage",
                "parameters": {},
                "required": []
            }
        }
    ]
    
    # Build message list
    messages = [
        {
            "role": "system", 
            "content": "I am an operations analyst. I will analyze the alert content, determine the current abnormal situation (alert object, abnormal pattern), and provide analysis suggestions."
        },
        {
            "role": "user", 
            "content": alert_content
        }
    ]
    
    # Get model response
    while True:
        response = get_response(messages, tools)
        if not response or not response.output:
            return "Failed to get response"
            
        message = response.output.choices[0].message
        messages.append(message)
        
        # If model completes response, exit loop
        if response.output.choices[0].finish_reason == 'stop':
            break
        
        # If model needs to call tools
        if message.tool_calls:
            # Get function name and arguments
            fn_name = message.tool_calls[0]['function']['name']
            fn_arguments = message.tool_calls[0]['function']['arguments']
            
            # Call corresponding function
            if fn_name == 'get_current_status':
                tool_response = get_current_status()
                tool_info = {
                    "name": fn_name,
                    "role": "tool",
                    "content": tool_response
                }
                messages.append(tool_info)
    
    # Return final analysis result
    return messages[-1].content

if __name__ == "__main__":
    # Test examples
    test_alerts = [
        """Alert: Database connection count exceeds threshold
Time: 2024-03-15 15:30:00""",
        
        """Alert: CPU usage abnormal
Time: 2024-03-15 16:45:00
Details: CPU usage consistently above 90%"""
    ]
    
    for alert in test_alerts:
        print("\n" + "="*50)
        print("Alert content:")
        print(alert)
        print("\nAnalysis result:")
        result = analyze_alert(alert)
        print(result)
        print("="*50) 