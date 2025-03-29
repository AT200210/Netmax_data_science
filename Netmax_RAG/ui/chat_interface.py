import streamlit as st
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ChatInterface:
    """Chat interface component for the Streamlit app."""
    
    def __init__(self, generate_response_callback):
        """Initialize the chat interface.
        
        Args:
            generate_response_callback: Callback function for generating responses
        """
        self.generate_response_callback = generate_response_callback
        
        # Initialize chat history if not exists
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! Enter a website URL in the sidebar and I'll help answer questions about it."}
            ]
    
    def render(self):
        """Render the chat interface in the Streamlit app."""
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # User input
        if user_input := st.chat_input("Ask a question about the website:"):
            logger.info(f"User query: {user_input}")
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_input)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = self.generate_response_callback(user_input)
                    st.write(response)
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    logger.info("Response generated and displayed")