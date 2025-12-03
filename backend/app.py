"""
FastAPI application for AI-Powered Financial News Intelligence System.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime
import json

from database import init_db, get_db_connection, DB_PATH
from embeddings import get_embedding, serialize_embedding, deserialize_embedding, semantic_search_articles, detect_duplicate_articles
from groq_integration import extract_entities, detect_duplicates, map_stock_impact, query_with_context, analyze_sentiment

# Initialize FastAPI app
app = FastAPI(
    title="Financial News Intelligence System",
    description="AI-powered system for processing financial news with deduplication, entity extraction, and impact mapping",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    init_db()
    print(f"Database initialized at {DB_PATH}")


# ==================== Pydantic Models ====================

class Article(BaseModel):
    """Article model for input/output."""
    title: str
    content: str
    source: Optional[str] = None
    url: Optional[str] = None
    published_date: Optional[str] = None


class Entity(BaseModel):
    """Entity model."""
    entity_text: str
    entity_type: str
    confidence: float = 1.0


class StockImpact(BaseModel):
    """Stock impact model."""
    stock_symbol: str
    impact_type: str
    confidence: float = 0.5
    sentiment: Optional[str] = None


class ArticleResponse(BaseModel):
    """Article response model."""
    id: int
    title: str
    content: str
    source: Optional[str]
    url: Optional[str]
    published_date: Optional[str]
    is_duplicate: bool
    canonical_id: Optional[int]
    entities: List[Entity]
    stock_impacts: List[StockImpact]


# ==================== Health Check ====================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Financial News Intelligence System",
        "version": "1.0.0"
    }


# ==================== Article Management ====================

@app.post("/articles", response_model=dict)
async def add_article(article: Article):
    """
    Add a new article to the system.
    Automatically processes for deduplication, entity extraction, and stock impact mapping.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Generate embedding for the article
        embedding = get_embedding(article.content)
        embedding_bytes = serialize_embedding(embedding)
        
        # Check for duplicates with existing articles
        cursor.execute("SELECT id, content, embedding FROM articles WHERE is_duplicate = 0")
        existing_articles = cursor.fetchall()
        
        is_duplicate = False
        canonical_id = None
        
        for existing in existing_articles:
            existing_embedding = deserialize_embedding(existing[2])
            is_dup, similarity = detect_duplicate_articles(embedding, existing_embedding, threshold=0.85)
            
            if is_dup:
                is_duplicate = True
                canonical_id = existing[0]
                break
        
        # Insert article
        cursor.execute("""
            INSERT INTO articles (title, content, source, url, published_date, embedding, is_duplicate, canonical_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            article.title,
            article.content,
            article.source,
            article.url,
            article.published_date,
            embedding_bytes,
            is_duplicate,
            canonical_id
        ))
        
        article_id = cursor.lastrowid
        
        # Extract entities
        entities_data = extract_entities(article.content)
        
        for entity_type, entities_list in entities_data.items():
            for entity_text in entities_list:
                cursor.execute("""
                    INSERT INTO entities (article_id, entity_text, entity_type, confidence)
                    VALUES (?, ?, ?, ?)
                """, (article_id, entity_text, entity_type, 1.0))
        
        # Map stock impacts
        for entity_type, entities_list in entities_data.items():
            if entity_type in ["companies", "sectors"]:
                for entity_text in entities_list:
                    impact_data = map_stock_impact(article.content, entity_text)
                    
                    for stock in impact_data.get("stocks", []):
                        cursor.execute("""
                            INSERT INTO stock_impacts (article_id, stock_symbol, impact_type, confidence, sentiment)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            article_id,
                            stock.get("symbol"),
                            stock.get("impact_type"),
                            stock.get("confidence", 0.5),
                            None
                        ))
        
        # Analyze sentiment
        sentiment_data = analyze_sentiment(article.content)
        
        conn.commit()
        conn.close()
        
        return {
            "id": article_id,
            "title": article.title,
            "is_duplicate": is_duplicate,
            "canonical_id": canonical_id,
            "entities": entities_data,
            "sentiment": sentiment_data,
            "message": "Article added successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int):
    """Get a specific article with its entities and stock impacts."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get article
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        article = cursor.fetchone()
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Get entities
        cursor.execute("SELECT entity_text, entity_type, confidence FROM entities WHERE article_id = ?", (article_id,))
        entities = [Entity(**dict(row)) for row in cursor.fetchall()]
        
        # Get stock impacts
        cursor.execute("SELECT stock_symbol, impact_type, confidence, sentiment FROM stock_impacts WHERE article_id = ?", (article_id,))
        impacts = [StockImpact(**dict(row)) for row in cursor.fetchall()]
        
        conn.close()
        
        return ArticleResponse(
            id=article[0],
            title=article[1],
            content=article[2],
            source=article[3],
            url=article[4],
            published_date=article[5],
            is_duplicate=article[8],
            canonical_id=article[9],
            entities=entities,
            stock_impacts=impacts
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/articles")
async def list_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    unique_only: bool = Query(False)
):
    """List articles with pagination."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if unique_only:
            cursor.execute("""
                SELECT id, title, source, published_date, is_duplicate, canonical_id
                FROM articles WHERE is_duplicate = 0
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (limit, skip))
        else:
            cursor.execute("""
                SELECT id, title, source, published_date, is_duplicate, canonical_id
                FROM articles
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (limit, skip))
        
        articles = []
        for row in cursor.fetchall():
            articles.append({
                "id": row[0],
                "title": row[1],
                "source": row[2],
                "published_date": row[3],
                "is_duplicate": row[4],
                "canonical_id": row[5]
            })
        
        conn.close()
        return articles
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Deduplication ====================

@app.get("/deduplication/stats")
async def deduplication_stats():
    """Get deduplication statistics."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM articles")
        total_articles = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM articles WHERE is_duplicate = 1")
        duplicate_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM articles WHERE is_duplicate = 0")
        unique_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(similarity_score) FROM deduplication_records WHERE is_duplicate = 1")
        avg_similarity = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_articles": total_articles,
            "unique_articles": unique_count,
            "duplicate_articles": duplicate_count,
            "deduplication_rate": round((duplicate_count / total_articles * 100) if total_articles > 0 else 0, 2),
            "average_similarity_score": round(avg_similarity, 3)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Entity Extraction ====================

@app.get("/entities")
async def list_entities(
    entity_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500)
):
    """List extracted entities with optional filtering by type."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if entity_type:
            cursor.execute("""
                SELECT DISTINCT entity_text, entity_type, COUNT(*) as frequency
                FROM entities WHERE entity_type = ?
                GROUP BY entity_text
                ORDER BY frequency DESC
                LIMIT ? OFFSET ?
            """, (entity_type, limit, skip))
        else:
            cursor.execute("""
                SELECT DISTINCT entity_text, entity_type, COUNT(*) as frequency
                FROM entities
                GROUP BY entity_text
                ORDER BY frequency DESC
                LIMIT ? OFFSET ?
            """, (limit, skip))
        
        entities = []
        for row in cursor.fetchall():
            entities.append({
                "entity_text": row[0],
                "entity_type": row[1],
                "frequency": row[2]
            })
        
        conn.close()
        return entities
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Stock Impact Mapping ====================

@app.get("/stock-impacts")
async def list_stock_impacts(
    stock_symbol: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500)
):
    """List stock impacts with optional filtering by symbol."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if stock_symbol:
            cursor.execute("""
                SELECT stock_symbol, impact_type, AVG(confidence) as avg_confidence, COUNT(*) as frequency
                FROM stock_impacts WHERE stock_symbol = ?
                GROUP BY stock_symbol, impact_type
                ORDER BY frequency DESC
                LIMIT ? OFFSET ?
            """, (stock_symbol, limit, skip))
        else:
            cursor.execute("""
                SELECT stock_symbol, impact_type, AVG(confidence) as avg_confidence, COUNT(*) as frequency
                FROM stock_impacts
                GROUP BY stock_symbol, impact_type
                ORDER BY frequency DESC
                LIMIT ? OFFSET ?
            """, (limit, skip))
        
        impacts = []
        for row in cursor.fetchall():
            impacts.append({
                "stock_symbol": row[0],
                "impact_type": row[1],
                "average_confidence": round(row[2], 3),
                "frequency": row[3]
            })
        
        conn.close()
        return impacts
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Semantic Search & Query ====================

@app.post("/search")
async def semantic_search(
    query: str = Query(..., min_length=1),
    top_k: int = Query(10, ge=1, le=100)
):
    """
    Perform semantic search on articles using embeddings.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, title, content, embedding FROM articles WHERE is_duplicate = 0")
        articles = []
        for row in cursor.fetchall():
            articles.append({
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "embedding": row[3]
            })
        
        conn.close()
        
        # Perform semantic search
        results = semantic_search_articles(query, articles, top_k=top_k)
        
        return {
            "query": query,
            "results_count": len(results),
            "results": [
                {
                    "id": r["id"],
                    "title": r["title"],
                    "similarity_score": round(r["similarity_score"], 3)
                }
                for r in results
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def intelligent_query(query: str = Query(..., min_length=1)):
    """
    Process natural language queries with context awareness.
    Returns AI-generated response based on relevant articles.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get relevant articles
        cursor.execute("""
            SELECT id, title, content FROM articles WHERE is_duplicate = 0
            ORDER BY created_at DESC LIMIT 10
        """)
        
        context_articles = [
            {
                "id": row[0],
                "title": row[1],
                "content": row[2]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        # Get AI response
        response = query_with_context(query, context_articles)
        
        return {
            "query": query,
            "response": response,
            "context_articles_used": len(context_articles)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Analytics & Statistics ====================

@app.get("/statistics")
async def get_statistics():
    """Get comprehensive statistics about the system."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Article statistics
        cursor.execute("SELECT COUNT(*) FROM articles")
        total_articles = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM articles WHERE is_duplicate = 0")
        unique_articles = cursor.fetchone()[0]
        
        # Entity statistics
        cursor.execute("SELECT COUNT(DISTINCT entity_type) FROM entities")
        entity_types = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT entity_text) FROM entities")
        unique_entities = cursor.fetchone()[0]
        
        # Stock statistics
        cursor.execute("SELECT COUNT(DISTINCT stock_symbol) FROM stock_impacts")
        unique_stocks = cursor.fetchone()[0]
        
        # Top entities
        cursor.execute("""
            SELECT entity_text, entity_type, COUNT(*) as frequency
            FROM entities
            GROUP BY entity_text, entity_type
            ORDER BY frequency DESC
            LIMIT 10
        """)
        top_entities = [
            {"entity": row[0], "type": row[1], "frequency": row[2]}
            for row in cursor.fetchall()
        ]
        
        # Top stocks
        cursor.execute("""
            SELECT stock_symbol, COUNT(*) as frequency, AVG(confidence) as avg_confidence
            FROM stock_impacts
            GROUP BY stock_symbol
            ORDER BY frequency DESC
            LIMIT 10
        """)
        top_stocks = [
            {"symbol": row[0], "frequency": row[1], "avg_confidence": round(row[2], 3)}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            "articles": {
                "total": total_articles,
                "unique": unique_articles,
                "duplicates": total_articles - unique_articles
            },
            "entities": {
                "types": entity_types,
                "unique_entities": unique_entities,
                "top_10": top_entities
            },
            "stocks": {
                "unique_stocks": unique_stocks,
                "top_10": top_stocks
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
