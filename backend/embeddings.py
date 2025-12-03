"""
Embeddings and semantic search for RAG-based deduplication and similarity detection.
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from typing import List, Tuple

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(text: str) -> np.ndarray:
    """
    Generate embedding for a given text using sentence-transformers.
    
    Args:
        text: The text to embed
        
    Returns:
        Embedding vector as numpy array
    """
    try:
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return np.zeros(384)  # Return zero vector on error


def serialize_embedding(embedding: np.ndarray) -> bytes:
    """
    Serialize embedding to bytes for storage.
    
    Args:
        embedding: Numpy array embedding
        
    Returns:
        Pickled bytes
    """
    return pickle.dumps(embedding)


def deserialize_embedding(data: bytes) -> np.ndarray:
    """
    Deserialize embedding from bytes.
    
    Args:
        data: Pickled bytes
        
    Returns:
        Numpy array embedding
    """
    try:
        return pickle.loads(data)
    except Exception as e:
        print(f"Error deserializing embedding: {e}")
        return np.zeros(384)


def calculate_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two embeddings.
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
        
    Returns:
        Similarity score between 0 and 1
    """
    try:
        similarity = cosine_similarity(
            embedding1.reshape(1, -1),
            embedding2.reshape(1, -1)
        )[0][0]
        return float(similarity)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0


def find_similar_articles(query_embedding: np.ndarray, 
                         article_embeddings: List[Tuple[int, np.ndarray]],
                         threshold: float = 0.7) -> List[Tuple[int, float]]:
    """
    Find articles similar to a query embedding.
    
    Args:
        query_embedding: The query embedding
        article_embeddings: List of (article_id, embedding) tuples
        threshold: Minimum similarity threshold
        
    Returns:
        List of (article_id, similarity_score) tuples sorted by similarity
    """
    results = []
    
    for article_id, embedding in article_embeddings:
        similarity = calculate_similarity(query_embedding, embedding)
        if similarity >= threshold:
            results.append((article_id, similarity))
    
    # Sort by similarity score descending
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def batch_embed_texts(texts: List[str]) -> List[np.ndarray]:
    """
    Generate embeddings for multiple texts efficiently.
    
    Args:
        texts: List of texts to embed
        
    Returns:
        List of embedding vectors
    """
    try:
        embeddings = model.encode(texts, convert_to_numpy=True)
        return [embedding for embedding in embeddings]
    except Exception as e:
        print(f"Error batch embedding texts: {e}")
        return [np.zeros(384) for _ in texts]


def semantic_search_articles(query: str, 
                            articles: List[dict],
                            top_k: int = 10) -> List[dict]:
    """
    Perform semantic search on articles using embeddings.
    
    Args:
        query: Search query
        articles: List of article dictionaries with 'content' and 'embedding' fields
        top_k: Number of top results to return
        
    Returns:
        List of top matching articles with similarity scores
    """
    query_embedding = get_embedding(query)
    results = []
    
    for article in articles:
        try:
            if article.get('embedding'):
                article_embedding = deserialize_embedding(article['embedding'])
                similarity = calculate_similarity(query_embedding, article_embedding)
                results.append({
                    **article,
                    'similarity_score': similarity
                })
        except Exception as e:
            print(f"Error processing article {article.get('id')}: {e}")
    
    # Sort by similarity and return top_k
    results.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
    return results[:top_k]


def detect_duplicate_articles(article1_embedding: np.ndarray,
                             article2_embedding: np.ndarray,
                             threshold: float = 0.85) -> Tuple[bool, float]:
    """
    Detect if two articles are duplicates based on embedding similarity.
    
    Args:
        article1_embedding: First article embedding
        article2_embedding: Second article embedding
        threshold: Similarity threshold for considering articles as duplicates
        
    Returns:
        Tuple of (is_duplicate, similarity_score)
    """
    similarity = calculate_similarity(article1_embedding, article2_embedding)
    is_duplicate = similarity >= threshold
    return is_duplicate, similarity
