import logging
from langchain_community.embeddings import HuggingFaceEmbeddings

# Configure logging
logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating text embeddings."""
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize the embedding service.
        
        Args:
            model_name (str): The name of the model to use for embeddings
        """
        self.model_name = model_name
    
    def get_embeddings(self):
        """Get the embedding model.
        
        Returns:
            HuggingFaceEmbeddings: The embedding model
        """
        try:
            logger.info(f"Initializing HuggingFace embeddings with model: {self.model_name}")
            embeddings = HuggingFaceEmbeddings(model_name=self.model_name)
            return embeddings
        except Exception as e:
            logger.error(f"Error initializing embeddings: {str(e)}")
            raise