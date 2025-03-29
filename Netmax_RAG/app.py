import streamlit as st
from api.chatgpt_client import ChatGPTClient
from data.embedding_service import EmbeddingService
from data.vector_store_service import VectorStoreService
from ui.chat_interface import ChatInterface
from ui.sidebar import Sidebar
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebsiteChatApp:
    """Main application class for the Website Chat Assistant."""
    
    def __init__(self):
        """Initialize the application components."""
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()
        self.chatgpt_client = ChatGPTClient()
        self.sidebar = Sidebar(self.process_website)
        self.chat_interface = ChatInterface(self.generate_response)
    
    def process_website(self, url):
        """Process a website URL and create a vector store.
        
        Args:
            url (str): The URL of the website to process
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            embeddings = self.embedding_service.get_embeddings()
            vector_store, error = self.vector_store_service.create_vector_store(url, embeddings)
            
            if error:
                st.error(f"Error: {error}")
                return False
            else:
                st.session_state.vector_store = vector_store
                return True
        except Exception as e:
            logger.error(f"Error processing website: {str(e)}")
            st.error(f"Error processing website: {str(e)}")
            return False
    
    def generate_response(self, query):
        """Generate a response for the user query.
        
        Args:
            query (str): The user's question
            
        Returns:
            str: The generated response
        """
        try:
            if "vector_store" not in st.session_state:
                return "Please process a website first by entering a URL in the sidebar."
            
            vector_store = st.session_state.vector_store
            docs, context = self.vector_store_service.retrieve_relevant_content(query, vector_store)
            
            # Show document count in UI
            st.write(f"Found {len(docs)} relevant sections from the website")
            
            # Generate response using ChatGPT
            response = self.chatgpt_client.generate_response(query, context)
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def run(self):
        """Run the Streamlit application."""
        st.title("Website Chat Assistant with ChatGPT")
        
        # Render sidebar
        self.sidebar.render()
        
        # Render chat interface
        self.chat_interface.render()

# Run the application
if __name__ == "__main__":
    app = WebsiteChatApp()
    app.run()