"""
Groq Llama integration for AI-powered financial news analysis.
"""

from groq import Groq
import os
import json
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if key exists to prevent errors later
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Please check your .env file.")
client = Groq(api_key=GROQ_API_KEY)


def extract_entities(text: str) -> dict:
    """
    Extract entities (Companies, Sectors, Regulators, People, Events) from text using Llama.
    
    Args:
        text: The article text to analyze
        
    Returns:
        Dictionary containing extracted entities by type
    """
    prompt = f"""
    Analyze the following financial news article and extract entities in JSON format.
    
    Article:
    {text}
    
    Extract and return a JSON object with these entity types:
    - companies: List of company names mentioned
    - sectors: List of sectors/industries affected
    - regulators: List of regulatory bodies mentioned
    - people: List of key people mentioned
    - events: List of key events mentioned
    
    Return ONLY valid JSON, no other text.
    """
    
    try:
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.choices[0].message.content
        
        # Try to parse JSON from response
        try:
            entities = json.loads(response_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                entities = json.loads(json_match.group())
            else:
                entities = {
                    "companies": [],
                    "sectors": [],
                    "regulators": [],
                    "people": [],
                    "events": []
                }
        
        return entities
    except Exception as e:
        print(f"Error extracting entities: {e}")
        return {
            "companies": [],
            "sectors": [],
            "regulators": [],
            "people": [],
            "events": []
        }


def detect_duplicates(article1_text: str, article2_text: str) -> float:
    """
    Detect semantic similarity between two articles using Llama.
    
    Args:
        article1_text: First article text
        article2_text: Second article text
        
    Returns:
        Similarity score between 0 and 1
    """
    prompt = f"""
    Compare these two financial news articles and determine if they cover the same story.
    
    Article 1:
    {article1_text[:500]}
    
    Article 2:
    {article2_text[:500]}
    
    Return a JSON object with:
    - is_duplicate: boolean (true if same story, false if different)
    - similarity_score: number between 0 and 1
    - reasoning: brief explanation
    
    Return ONLY valid JSON.
    """
    
    try:
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=256,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.choices[0].message.content
        
        try:
            result = json.loads(response_text)
            return result.get("similarity_score", 0.0)
        except json.JSONDecodeError:
            import re
            score_match = re.search(r'"similarity_score"\s*:\s*([\d.]+)', response_text)
            if score_match:
                return float(score_match.group(1))
            return 0.0
    except Exception as e:
        print(f"Error detecting duplicates: {e}")
        return 0.0


def map_stock_impact(text: str, entity: str) -> dict:
    """
    Map news impact to specific stocks with confidence scores.
    
    Args:
        text: The article text
        entity: The entity (company/sector) to map
        
    Returns:
        Dictionary with stock symbols and confidence scores
    """
    prompt = f"""
    For the financial news article below, identify which stocks would be impacted by the news about "{entity}".
    
    Article:
    {text}
    
    Return a JSON object with:
    - stocks: List of objects with:
      - symbol: Stock ticker symbol (e.g., HDFCBANK, INFY)
      - confidence: Confidence score 0-1 (1.0 for direct mention, 0.6-0.8 for sector-wide, variable for regulatory)
      - impact_type: "direct", "sector", or "regulatory"
    
    Return ONLY valid JSON.
    """
    
    try:
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=512,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.choices[0].message.content
        
        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"stocks": []}
    except Exception as e:
        print(f"Error mapping stock impact: {e}")
        return {"stocks": []}


def query_with_context(query: str, context_articles: list) -> str:
    """
    Process natural language queries with context awareness using Llama.
    
    Args:
        query: User's natural language query
        context_articles: List of relevant articles for context
        
    Returns:
        AI-generated response with relevant information
    """
    articles_text = "\n\n".join([
        f"Article: {article.get('title', '')}\n{article.get('content', '')[:300]}"
        for article in context_articles[:5]
    ])
    
    prompt = f"""
    A user is asking about financial news. Answer their query based on the provided articles.
    
    User Query: {query}
    
    Relevant Articles:
    {articles_text}
    
    Provide a concise, informative answer based on the articles. If the query is about a company, include sector-wide implications. If about a sector, summarize impacts across companies.
    """
    
    try:
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=512,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.choices[0].message.content
    except Exception as e:
        print(f"Error querying with context: {e}")
        return "Unable to process query at this time."


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment and predict price impact using Llama.
    
    Args:
        text: The article text
        
    Returns:
        Dictionary with sentiment analysis and price impact prediction
    """
    prompt = f"""
    Analyze the sentiment of this financial news article and predict its potential price impact.
    
    Article:
    {text}
    
    Return a JSON object with:
    - sentiment: "positive", "negative", or "neutral"
    - sentiment_score: -1 to 1 (negative to positive)
    - price_impact: "bullish", "bearish", or "neutral"
    - impact_magnitude: "high", "medium", or "low"
    - reasoning: brief explanation
    
    Return ONLY valid JSON.
    """
    
    try:
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=256,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.choices[0].message.content
        
        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {
                "sentiment": "neutral",
                "sentiment_score": 0.0,
                "price_impact": "neutral",
                "impact_magnitude": "low"
            }
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return {
            "sentiment": "neutral",
            "sentiment_score": 0.0,
            "price_impact": "neutral",
            "impact_magnitude": "low"
        }
