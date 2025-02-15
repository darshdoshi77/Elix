import requests
import os
from backend.OpenAI import run_llm_function_call

API_KEY = os.getenv("NEWSDATA_API_KEY")


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
            "required": ["query"]
            }
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
   
   
    gpt_response = run_llm_function_call(user_request,context_str, temperature=0.0)
    query = gpt_response[0]["query"]
    
    if not query or not isinstance(query, str):
        return "Error: Unable to extract a valid search query."

    url = f"https://newsdata.io/api/1/latest?apikey={API_KEY}&q={query.strip()}"
    
    try:
        response = requests.get(url).json()

        if "results" in response and response["results"]:
            news_list = response["results"][:3] 

            formatted_news = [
                f"{news['title']} ({news['source_id']})\n {news['link']}"
                for news in news_list
            ]
            return "\n\n".join(formatted_news)

        else:
            return f"No news articles found for '{query}'."

    except Exception as e:
        return f"Error fetching news: {str(e)}"
