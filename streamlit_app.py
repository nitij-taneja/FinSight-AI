"""
Streamlit frontend for AI-Powered Financial News Intelligence System.
"""

import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# Configure Streamlit page
st.set_page_config(
    page_title="Financial News Intelligence",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)
import os
# Try to get from Streamlit secrets, otherwise fallback to localhost
if "API_URL" in st.secrets:
    API_BASE_URL = st.secrets["API_URL"]
else:
    API_BASE_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["🏠 Dashboard", "📰 News Feed", "🔍 Search & Query", "📊 Analytics", "➕ Add Article", "⚙️ Settings"]
)

# Helper functions
@st.cache_data
def get_health_status():
    """Check API health status."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

@st.cache_data(ttl=60)
def get_statistics():
    """Fetch system statistics."""
    try:
        response = requests.get(f"{API_BASE_URL}/statistics", timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

@st.cache_data(ttl=60)
def get_dedup_stats():
    """Fetch deduplication statistics."""
    try:
        response = requests.get(f"{API_BASE_URL}/deduplication/stats", timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def add_article(title, content, source, url, published_date):
    """Add a new article to the system."""
    try:
        payload = {
            "title": title,
            "content": content,
            "source": source,
            "url": url,
            "published_date": published_date
        }
        response = requests.post(f"{API_BASE_URL}/articles", json=payload, timeout=30)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}

def search_articles(query, top_k=10):
    """Perform semantic search on articles."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/search",
            params={"query": query, "top_k": top_k},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def intelligent_query(query):
    """Process intelligent query with context."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            params={"query": query},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def list_articles(skip=0, limit=10, unique_only=False):
    """List articles with pagination."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/articles",
            params={"skip": skip, "limit": limit, "unique_only": unique_only},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

def get_entities(entity_type=None, skip=0, limit=50):
    """List extracted entities."""
    try:
        params = {"skip": skip, "limit": limit}
        if entity_type:
            params["entity_type"] = entity_type
        response = requests.get(f"{API_BASE_URL}/entities", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

def get_stock_impacts(stock_symbol=None, skip=0, limit=50):
    """List stock impacts."""
    try:
        params = {"skip": skip, "limit": limit}
        if stock_symbol:
            params["stock_symbol"] = stock_symbol
        response = requests.get(f"{API_BASE_URL}/stock-impacts", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

# ==================== DASHBOARD PAGE ====================
if page == "🏠 Dashboard":
    st.title("📊 Financial News Intelligence Dashboard")
    
    # Health Status
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### System Status")
    with col2:
        if get_health_status():
            st.success("✅ API Online")
        else:
            st.error("❌ API Offline")
    
    # Key Metrics
    stats = get_statistics()
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Articles",
                stats["articles"]["total"],
                delta=f"Unique: {stats['articles']['unique']}"
            )
        
        with col2:
            st.metric(
                "Unique Entities",
                stats["entities"]["unique_entities"],
                delta=f"Types: {stats['entities']['types']}"
            )
        
        with col3:
            st.metric(
                "Tracked Stocks",
                stats["stocks"]["unique_stocks"],
                delta="Active"
            )
        
        with col4:
            dedup = get_dedup_stats()
            if dedup:
                st.metric(
                    "Dedup Rate",
                    f"{dedup['deduplication_rate']}%",
                    delta=f"Duplicates: {dedup['duplicate_articles']}"
                )
    
    # Top Entities
    if stats:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏢 Top Entities")
            if stats["entities"]["top_10"]:
                df_entities = pd.DataFrame(stats["entities"]["top_10"])
                st.dataframe(df_entities, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### 📈 Top Stocks")
            if stats["stocks"]["top_10"]:
                df_stocks = pd.DataFrame(stats["stocks"]["top_10"])
                st.dataframe(df_stocks, use_container_width=True, hide_index=True)

# ==================== NEWS FEED PAGE ====================
elif page == "📰 News Feed":
    st.title("📰 News Feed")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        skip = st.number_input("Skip", min_value=0, value=0, step=10)
    with col2:
        limit = st.number_input("Limit", min_value=1, max_value=100, value=10)
    with col3:
        unique_only = st.checkbox("Unique Articles Only", value=False)
    
    articles = list_articles(skip=skip, limit=limit, unique_only=unique_only)
    
    if articles:
        for article in articles:
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"### {article['title']}")
                    st.caption(f"📅 {article['published_date']} | 📍 {article['source']}")
                
                with col2:
                    if article['is_duplicate']:
                        st.warning("Duplicate")
                    else:
                        st.success("Unique")
                
                st.divider()
    else:
        st.info("No articles found.")

# ==================== SEARCH & QUERY PAGE ====================
elif page == "🔍 Search & Query":
    st.title("🔍 Search & Intelligent Query")
    
    tab1, tab2 = st.tabs(["Semantic Search", "Intelligent Query"])
    
    with tab1:
        st.markdown("### Semantic Search")
        st.write("Find articles based on semantic similarity to your query.")
        
        search_query = st.text_input("Enter search query:", placeholder="e.g., HDFC Bank dividend")
        top_k = st.slider("Number of results", min_value=1, max_value=50, value=10)
        
        if st.button("🔍 Search", key="search_btn"):
            if search_query:
                with st.spinner("Searching..."):
                    results = search_articles(search_query, top_k=top_k)
                    
                    if results and results.get("results"):
                        st.success(f"Found {results['results_count']} results")
                        
                        for i, result in enumerate(results["results"], 1):
                            col1, col2 = st.columns([4, 1])
                            with col1:
                                st.markdown(f"{i}. **{result['title']}**")
                            with col2:
                                st.caption(f"Score: {result['similarity_score']}")
                    else:
                        st.warning("No results found.")
            else:
                st.warning("Please enter a search query.")
    
    with tab2:
        st.markdown("### Intelligent Query with Context")
        st.write("Ask questions about financial news. The system will provide AI-generated responses based on context.")
        
        query_text = st.text_area(
            "Enter your question:",
            placeholder="e.g., What is the impact of RBI rate hike on banking stocks?",
            height=100
        )
        
        if st.button("💡 Get Answer", key="query_btn"):
            if query_text:
                with st.spinner("Processing your query..."):
                    result = intelligent_query(query_text)
                    
                    if result:
                        st.markdown("### AI Response")
                        st.write(result.get("response", "No response generated."))
                        st.caption(f"Context articles used: {result.get('context_articles_used', 0)}")
                    else:
                        st.error("Failed to process query. Please try again.")
            else:
                st.warning("Please enter a question.")

# ==================== ANALYTICS PAGE ====================
elif page == "📊 Analytics":
    st.title("📊 Analytics & Insights")
    
    tab1, tab2, tab3 = st.tabs(["Entities", "Stock Impacts", "Deduplication"])
    
    with tab1:
        st.markdown("### Extracted Entities")
        
        entity_type = st.selectbox(
            "Filter by entity type:",
            ["All", "companies", "sectors", "regulators", "people", "events"]
        )
        
        entities = get_entities(
            entity_type=None if entity_type == "All" else entity_type,
            limit=50
        )
        
        if entities:
            df = pd.DataFrame(entities)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No entities found.")
    
    with tab2:
        st.markdown("### Stock Impact Analysis")
        
        stock_symbol = st.text_input("Filter by stock symbol (optional):", placeholder="e.g., HDFCBANK")
        
        impacts = get_stock_impacts(
            stock_symbol=stock_symbol if stock_symbol else None,
            limit=50
        )
        
        if impacts:
            df = pd.DataFrame(impacts)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No stock impacts found.")
    
    with tab3:
        st.markdown("### Deduplication Statistics")
        
        dedup_stats = get_dedup_stats()
        if dedup_stats:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Articles", dedup_stats["total_articles"])
            
            with col2:
                st.metric("Unique Articles", dedup_stats["unique_articles"])
            
            with col3:
                st.metric("Deduplication Rate", f"{dedup_stats['deduplication_rate']}%")
            
            st.metric(
                "Average Similarity Score",
                f"{dedup_stats['average_similarity_score']:.3f}",
                delta="For duplicates"
            )

# ==================== ADD ARTICLE PAGE ====================
elif page == "➕ Add Article":
    st.title("➕ Add New Article")
    
    with st.form("article_form"):
        title = st.text_input("Article Title *", placeholder="Enter article title")
        content = st.text_area("Article Content *", placeholder="Enter article content", height=200)
        source = st.text_input("Source", placeholder="e.g., Reuters, Bloomberg")
        url = st.text_input("URL", placeholder="https://example.com/article")
        published_date = st.date_input("Published Date")
        
        submitted = st.form_submit_button("📤 Add Article")
        
        if submitted:
            if not title or not content:
                st.error("Title and Content are required!")
            else:
                with st.spinner("Processing article..."):
                    success, result = add_article(
                        title=title,
                        content=content,
                        source=source,
                        url=url,
                        published_date=str(published_date)
                    )
                    
                    if success:
                        st.success("✅ Article added successfully!")
                        st.json(result)
                    else:
                        st.error(f"❌ Error adding article: {result.get('error', 'Unknown error')}")

# ==================== SETTINGS PAGE ====================
elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    
    st.markdown("### API Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**API Base URL**")
        st.code(API_BASE_URL)
    
    with col2:
        st.markdown("**API Status**")
        if get_health_status():
            st.success("✅ Connected")
        else:
            st.error("❌ Disconnected")
    
    st.markdown("### System Information")
    
    st.markdown("""
    **Financial News Intelligence System v1.0.0**
    
    This system provides:
    - 🔄 Intelligent News Deduplication (≥95% accuracy)
    - 🏢 Entity Extraction & Classification
    - 📈 Stock Impact Mapping with Confidence Scores
    - 🔍 Context-Aware Query System
    - 💡 AI-Powered Insights using Groq Llama
    - 📊 Comprehensive Analytics Dashboard
    
    **Technology Stack:**
    - Backend: FastAPI + SQLite
    - AI Model: Groq Llama (mixtral-8x7b-32768)
    - Embeddings: Sentence-Transformers
    - Frontend: Streamlit
    
    **Features:**
    - RAG-based semantic search
    - Vector embeddings for similarity detection
    - Sentiment analysis and price impact prediction
    - Real-time entity extraction
    - Stock impact confidence scoring
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p>Financial News Intelligence System | Powered by Groq Llama & FastAPI</p>
    <p>© 2025| All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
