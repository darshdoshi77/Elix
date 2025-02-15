import requests
import os
from OpenAI import *





def get_news(user_request):
    
    get_news_function = {
        "name": "get_news",
        "description": "Fetches the latest news articles on a specific topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The keyword to search for news."
                },
            },
            "required": ["query"]     
        }
    }

    context_str = """
    You are an AI assistant that extracts concise search queries for news. 
    Given a user request for news, return a short keyword or phrase as the query.
    Examples:
    - "Give me the latest news on Bitcoin." → "bitcoin"
    - "What's happening with Tesla?" → "tesla"
    - "Any updates about AI technology?" → "AI technology"
    - "Tell me about the 2024 elections." → "2024 elections"

    """
   
   
    gpt_response = run_llm_function_call(user_request,context_str, [get_news_function], temperature=0.0)
    print("gpt output", gpt_response)
    query = gpt_response[0]["query"]
    print("query",query)
    if not query or not isinstance(query, str):
        return "Error: Unable to extract a valid search query."

    url = f"https://newsdata.io/api/1/latest?apikey=pub_696611aefc818c48ce9a0446c1eef81d97138&language=en&q={query}"
    
    try:
        response = requests.get(url).json()
        print("response", response)
        if "results" in response and response["results"]:
            news_list = response["results"][:3] 

            formatted_news = [
                f"{news['title']} ({news['source_id']})\n {news['link']}"
                for news in news_list
            ]
            return {"news": formatted_news}

        else:
            return f"No news articles found for '{query}'."

    except Exception as e:
        return f"Error fetching news: {str(e)}"
