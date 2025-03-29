import streamlit as st
import logging

# Configure logging
logger = logging.getLogger(__name__)

class Sidebar:
    """Sidebar component for the Streamlit app."""
    
    def __init__(self, process_website_callback):
        """Initialize the sidebar.
        
        Args:
            process_website_callback: Callback function for processing websites
        """
        self.process_website_callback = process_website_callback
    
    def render(self):
        """Render the sidebar in the Streamlit app."""
        with st.sidebar:
            st.header("Configuration")
            
            # Website URL input
            website_url = st.text_input("Enter website URL:")
            
            # Process button
            if st.button("Process Website"):
                if not website_url:
                    st.error("Please enter a valid URL")
                else:
                    with st.spinner("Processing website... (This might take a minute)"):
                        logger.info(f"Processing website: {website_url}")
                        success = self.process_website_callback(website_url)
                        
                        if success:
                            st.success("Website processed successfully!")
                            logger.info("Website processed successfully")
            
            # Add additional configurations if needed
            st.markdown("---")
            st.markdown("### About")
            st.markdown("This app allows you to chat with websites using AI.")