import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS

# Configure logging
logger = logging.getLogger(__name__)

class VectorStoreService:
    """Service for creating and querying vector stores."""
    
    def __init__(self):
        """Initialize the vector store service."""
        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    def create_vector_store(self, url, embeddings):
        """Create a vector store from a website URL.
        
        Args:
            url (str): The URL of the website to process
            embeddings: The embedding model to use
            
        Returns:
            tuple: (vector_store, error) where vector_store is the FAISS vector store
                  and error is an error message (or None if successful)
        """
        try:
            logger.info(f"Loading content from URL: {url}")
            # Load the content from the URL
            loader = WebBaseLoader(url)
            documents = loader.load()
            
            logger.info(f"Loaded {len(documents)} documents from website")
            
            # Text chunking
            text_splitter = self._create_text_splitter()
            chunks = text_splitter.split_documents(documents)
            
            logger.info(f"Created {len(chunks)} chunks from documents")
            
            # Create vector store using FAISS
            vector_store = FAISS.from_documents(chunks, embeddings)
            
            return vector_store, None
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            return None, str(e)
    
    def retrieve_relevant_content(self, query, vector_store, k=5, fetch_k=15, lambda_mult=0.7):
        """Retrieve relevant content from the vector store.
        
        Args:
            query (str): The query to search for
            vector_store: The FAISS vector store
            k (int): Number of documents to return
            fetch_k (int): Number of documents to consider
            lambda_mult (float): Diversity factor for MMR
            
        Returns:
            tuple: (docs, context) where docs is the list of documents and
                  context is the concatenated text
        """
        try:
            logger.info(f"Retrieving content for query: {query}")
            # Enhanced retrieval strategy using MMR
            docs = vector_store.max_marginal_relevance_search(
                query, 
                k=k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult
            )
            
            # Extract the content from documents
            context = "\n\n".join([doc.page_content for doc in docs])
            
            logger.info(f"Retrieved {len(docs)} relevant documents")
            
            return docs, context
        except Exception as e:
            logger.error(f"Error retrieving content: {str(e)}")
            raise
    
    def _create_text_splitter(self):
        """Create a text splitter for chunking documents.
        
        Returns:
            RecursiveCharacterTextSplitter: The text splitter
        """
        return RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )