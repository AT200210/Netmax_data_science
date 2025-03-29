import http.client
import json
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class ChatGPTClient:
    """Client for interacting with the ChatGPT API via RapidAPI."""
    
    def __init__(self):
        """Initialize the ChatGPT API client."""
        # Get API key from environment variables or use default if not available
        self.api_key = os.getenv("RAPIDAPI_KEY", "a0615bf2c5msha47f36ce55e3e3dp1da933jsna962bd8e636b")
        self.api_host = "chatgpt-42.p.rapidapi.com"
        self.api_endpoint = "/chatgpt"
        self.timeout = 30
    
    def generate_response(self, query, context):
        """Generate a response from ChatGPT based on query and context.
        
        Args:
            query (str): The user's question
            context (str): The context from the website
            
        Returns:
            str: The generated response
        """
        try:
            conn = http.client.HTTPSConnection(self.api_host, timeout=self.timeout)

            # Format message with context and query
            message_content = self._format_message(query, context)

            # Prepare payload
            payload = json.dumps({
                "messages": [
                    {"role": "user", "content": message_content}
                ],
                "web_access": False
            })

            # Prepare headers
            headers = {
                'x-rapidapi-key': self.api_key,
                'x-rapidapi-host': self.api_host,
                'Content-Type': "application/json"
            }

            # Send request
            logger.info("Sending request to ChatGPT API")
            conn.request("POST", self.api_endpoint, payload, headers)
            
            # Get response
            res = conn.getresponse()
            
            # Handle unsuccessful status codes
            if res.status != 200:
                logger.error(f"API Error: Received status code {res.status}")
                return f"API Error: Received status code {res.status}"
            
            # Read response data
            data = res.read()
            
            if not data:
                logger.warning("No response received from the API")
                return "No response received from the API."
                
            # Parse JSON response
            response_data = json.loads(data.decode("utf-8"))
            
            # Extract result
            if "result" in response_data and response_data.get("status") == True:
                logger.info("Successfully received API response")
                return response_data["result"]
            else:
                logger.warning(f"Unexpected API response structure: {str(response_data)}")
                return f"Unexpected API response structure: {str(response_data)}"
                    
        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {str(e)}")
            if 'data' in locals():
                raw_response = data.decode('utf-8')
                return f"Error parsing API response: {str(e)}. Raw response: {raw_response[:100]}..."
            return f"Error parsing API response: {str(e)}"
            
        except Exception as e:
            logger.error(f"Error communicating with API: {str(e)}")
            return f"Error communicating with API: {str(e)}"
            
        finally:
            # Always close the connection
            if 'conn' in locals():
                conn.close()
    
    def _format_message(self, query, context):
        """Format the message with query and context.
        
        Args:
            query (str): The user's question
            context (str): The context from the website
            
        Returns:
            str: The formatted message
        """
        return f"""Based on this website content:
        
{context}

Question: {query}

Please provide a detailed answer using only the information from the website content above."""