# Simple example of web search using OpenAI compatible API
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_web_search_response(query, model="qwen-plus", search_config=None):
    """
    Get response from model with web search enabled
    
    Args:
        query (str): User's search query
        model (str): Model name, default is qwen-plus
        search_config (dict): Web search configuration parameters:
            - enable_search (bool): Enable/disable web search
            - search_engine (str): Search engine to use, options: 'bing', 'google'
            - search_depth (int): Search depth, range: 1-3
            - search_timeout (int): Search timeout in seconds
            - search_max_results (int): Maximum number of search results
            - search_filter (str): Filter search results, e.g., 'site:example.com'
            - search_language (str): Search language, e.g., 'zh-CN', 'en-US'
            - search_region (str): Search region, e.g., 'CN', 'US'
            - search_safe_mode (bool): Enable/disable safe search
            - search_freshness (str): Result freshness, e.g., 'day', 'week', 'month'
        
    Returns:
        str: Model's response
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(
            # If environment variable is not set, replace with: api_key="sk-xxx"
            api_key=os.getenv('BL_API_KEY'),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # DashScope service base_url
        )
        
        # Default search configuration
        default_search_config = {
            "enable_search": True,          # Enable web search
            "search_engine": "bing",        # Use Bing as search engine
            "search_depth": 2,              # Medium search depth
            "search_timeout": 30,           # 30 seconds timeout
            "search_max_results": 5,        # Maximum 5 search results
            "search_filter": "",            # No filter
            "search_language": "zh-CN",     # Chinese language
            "search_region": "CN",          # China region
            "search_safe_mode": True,       # Enable safe search
            "search_freshness": "week"      # Results from past week
        }
        
        # Merge user config with default config
        if search_config:
            default_search_config.update(search_config)
        
        # Create chat completion with web search enabled
        completion = client.chat.completions.create(
            model=model,  # Model name, can be changed as needed
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': query}
            ],
            extra_body=default_search_config
        )
        
        # Return the response content
        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"Error during API call: {str(e)}")
        return None

def print_response_details(completion):
    """
    Print detailed response information
    
    Args:
        completion: API response object
    """
    print("\nDetailed Response Information:")
    print(f"Model: {completion.model}")
    print(f"Created: {completion.created}")
    print(f"Finish Reason: {completion.choices[0].finish_reason}")
    print(f"Usage: {completion.usage}")
    print("\nResponse Content:")
    print(completion.choices[0].message.content)

if __name__ == "__main__":
    # Test examples with different search configurations
    test_cases = [
        {
            "query": "中国队在巴黎奥运会获得了多少枚金牌",
            "config": {
                "enable_search": True,
                "search_engine": "bing",
                "search_language": "zh-CN",
                "search_freshness": "day"
            }
        },
        {
            "query": "2024年最新的AI技术发展有哪些",
            "config": {
                "enable_search": True,
                "search_engine": "google",
                "search_depth": 3,
                "search_max_results": 10,
                "search_freshness": "week"
            }
        },
        {
            "query": "最近有什么重要的科技新闻",
            "config": {
                "enable_search": True,
                "search_filter": "site:techcrunch.com",
                "search_language": "en-US",
                "search_region": "US"
            }
        }
    ]
    
    for case in test_cases:
        print("\n" + "="*50)
        print(f"Query: {case['query']}")
        print(f"Search Config: {case['config']}")
        
        # Get response with specific search configuration
        response = get_web_search_response(case['query'], search_config=case['config'])
        
        if response:
            print("\nResponse:")
            print(response)
        else:
            print("Failed to get response")
        print("="*50) 