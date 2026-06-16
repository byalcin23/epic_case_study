import requests

from tenacity import retry, wait_exponential, stop_after_attempt

# retrying mechanism for handling transient errors
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def fetch_available_pets():
    url = "https://petstore.swagger.io/v2/pet/findByStatus?status=available"
    
    # get request to the API with a timeout of 5 seconds
    response = requests.get(url, timeout=5)
    
    # Response validation: raise an exception for HTTP errors
    response.raise_for_status() 
    
    return response.json()
    