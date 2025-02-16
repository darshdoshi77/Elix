from exa_py import Exa
import os

exa = Exa(os.getenv('EXA_API_KEY'))


def web_search(request):
    result = exa.stream_answer(
    request,
    text=True,
    )
    
    response = ""
    for chunk in result:
        response = str(chunk)
        
    return response
        
        
 