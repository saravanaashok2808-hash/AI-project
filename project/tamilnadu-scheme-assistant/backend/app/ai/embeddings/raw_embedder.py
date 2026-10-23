import torch
import logging

logger = logging.getLogger(__name__)

class RawEmbedder:
    def __init__(self, model_id: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.is_loaded = False
        self.is_loading = False

    def load_model(self):
        if self.is_loaded or self.is_loading:
            return self.is_loaded
        self.is_loading = True
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedding model {self.model_id} on {self.device}...")
            self.model = SentenceTransformer(self.model_id, device=self.device)
            self.is_loaded = True
            logger.info("Raw Embedding model loaded successfully!")
            return True
        except Exception as e:
            logger.warning(f"Could not load embedding model: {e}")
            self.is_loaded = False
            return False
        finally:
            self.is_loading = False

    def embed_text(self, text: str):
        if not self.is_loaded:
            self.load_model()
            
        if not self.is_loaded or self.model is None:
            return None
            
        with torch.no_grad():
            embeddings = self.model.encode(text, convert_to_tensor=True)
            
        return embeddings.cpu().numpy()

# Singleton instance (lazy loaded)
embedding_service = RawEmbedder()
