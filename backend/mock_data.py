"""
Mock dataset with 30+ diverse financial news articles for testing and demonstration.
"""

MOCK_ARTICLES = [
    {
        "title": "HDFC Bank announces 15% dividend, board approves stock buyback",
        "content": "HDFC Bank Limited announced a dividend of 15% for FY2024, with the board also approving a share buyback program worth Rs 10,000 crore. The announcement comes as the bank reports strong Q4 earnings with net profit growth of 22% year-over-year. The buyback program is expected to enhance shareholder value and provide support to the stock price.",
        "source": "Reuters",
        "url": "https://example.com/hdfc-dividend-1",
        "published_date": "2025-01-15"
    },
    {
        "title": "Reserve Bank hikes interest rates by 0.25% in surprise move",
        "content": "The Reserve Bank of India (RBI) announced an unexpected 25 basis point increase in the repo rate to 6.75%, citing persistent inflation concerns. This marks the third consecutive rate hike in the current monetary policy cycle. Analysts expect this move to impact borrowing costs across the banking sector and may slow down credit growth.",
        "source": "Bloomberg",
        "url": "https://example.com/rbi-rate-hike-1",
        "published_date": "2025-01-16"
    },
    {
        "title": "Central bank raises policy rate 25bps, signals hawkish stance",
        "content": "In a closely watched monetary policy decision, the central bank raised the policy rate by 25 basis points to combat rising inflation. The decision signals a hawkish stance from the monetary authority, with officials indicating that further tightening may be necessary if inflation doesn't moderate in the coming quarters.",
        "source": "Financial Times",
        "url": "https://example.com/central-bank-rate-1",
        "published_date": "2025-01-16"
    },
    {
        "title": "ICICI Bank opens 500 new branches across Tier-2 cities",
        "content": "ICICI Bank announced an aggressive expansion plan, opening 500 new branches across Tier-2 and Tier-3 cities in India. This expansion is part of the bank's strategy to increase its retail presence and capture growing demand in semi-urban markets. The initiative is expected to boost the bank's deposit base and loan portfolio.",
        "source": "Economic Times",
        "url": "https://example.com/icici-expansion-1",
        "published_date": "2025-01-17"
    },
    {
        "title": "Banking sector NPAs decline to 5-year low, credit growth at 16%",
        "content": "The banking sector's non-performing assets (NPAs) have declined to a 5-year low of 3.2%, indicating improved asset quality across lenders. Simultaneously, credit growth has accelerated to 16% year-over-year, driven by strong demand from retail and corporate segments. This positive trend suggests a healthy banking ecosystem.",
        "source": "Mint",
        "url": "https://example.com/banking-npa-1",
        "published_date": "2025-01-18"
    },
    {
        "title": "Infosys reports 18% revenue growth in Q3, raises FY2024 guidance",
        "content": "Infosys, India's second-largest IT services company, reported Q3 revenue growth of 18% in constant currency terms. The company also raised its full-year FY2024 revenue guidance to 12-14% growth, citing strong demand from clients in the financial services and healthcare sectors. The stock surged 5% on the announcement.",
        "source": "CNBC",
        "url": "https://example.com/infosys-q3-1",
        "published_date": "2025-01-19"
    },
    {
        "title": "TCS wins $500 million deal from European financial services firm",
        "content": "Tata Consultancy Services (TCS) announced a major contract win worth $500 million from a leading European financial services company. The multi-year deal involves digital transformation and cloud migration services. This win strengthens TCS's position in the European market and is expected to contribute significantly to FY2024 revenues.",
        "source": "Business Standard",
        "url": "https://example.com/tcs-deal-1",
        "published_date": "2025-01-20"
    },
    {
        "title": "Reliance Industries Q3 profit surges 35% on oil price recovery",
        "content": "Reliance Industries reported a 35% surge in Q3 net profit, driven by strong performance in its oil and gas segment following the recovery in crude oil prices. The company's refining margins also improved significantly. However, the retail segment faced headwinds due to increased competition.",
        "source": "Hindustan Times",
        "url": "https://example.com/reliance-q3-1",
        "published_date": "2025-01-21"
    },
    {
        "title": "Wipro announces 8% dividend and share buyback program",
        "content": "Wipro announced an 8% dividend for FY2024 and approved a share buyback program worth Rs 3,000 crore. The announcement reflects the company's confidence in its business fundamentals and commitment to shareholder returns. The stock rallied 3% following the announcement.",
        "source": "Moneycontrol",
        "url": "https://example.com/wipro-dividend-1",
        "published_date": "2025-01-22"
    },
    {
        "title": "Axis Bank launches digital banking platform with AI-powered features",
        "content": "Axis Bank unveiled a new digital banking platform incorporating artificial intelligence for personalized financial recommendations. The platform aims to enhance customer experience and streamline banking operations. The bank expects this initiative to reduce operational costs by 20% and improve customer retention.",
        "source": "The Hindu Business Line",
        "url": "https://example.com/axis-digital-1",
        "published_date": "2025-01-23"
    },
    {
        "title": "Bajaj Auto reports 12% growth in two-wheeler sales",
        "content": "Bajaj Auto reported a 12% increase in two-wheeler sales in January 2024, driven by strong demand in rural markets and new product launches. The company's three-wheeler segment also showed resilience with 8% growth. Management attributed the growth to improved consumer sentiment and affordable financing options.",
        "source": "Autocar India",
        "url": "https://example.com/bajaj-sales-1",
        "published_date": "2025-01-24"
    },
    {
        "title": "Maruti Suzuki Q3 net profit declines 15% due to supply chain issues",
        "content": "Maruti Suzuki reported a 15% decline in Q3 net profit, primarily due to semiconductor supply chain disruptions and increased raw material costs. However, the company maintained its full-year guidance, expecting supply normalization in Q4. The stock declined 4% on the earnings miss.",
        "source": "Scroll.in",
        "url": "https://example.com/maruti-q3-1",
        "published_date": "2025-01-25"
    },
    {
        "title": "SEBI imposes restrictions on high-frequency trading to protect retail investors",
        "content": "The Securities and Exchange Board of India (SEBI) announced new regulations restricting high-frequency trading practices to protect retail investors from market manipulation. The new rules include stricter position limits and enhanced surveillance mechanisms. Market analysts expect this to reduce volatility in equity markets.",
        "source": "Indian Express",
        "url": "https://example.com/sebi-hft-1",
        "published_date": "2025-01-26"
    },
    {
        "title": "RBI announces new guidelines for digital payment providers",
        "content": "The Reserve Bank of India released comprehensive guidelines for digital payment service providers, including stricter KYC requirements and enhanced fraud prevention measures. The guidelines aim to strengthen the digital payments ecosystem and protect consumer data. Payment companies have 6 months to comply with the new regulations.",
        "source": "The Times of India",
        "url": "https://example.com/rbi-digital-1",
        "published_date": "2025-01-27"
    },
    {
        "title": "Pharma sector sees 20% growth driven by generic drug exports",
        "content": "India's pharmaceutical sector reported 20% growth in FY2024, driven by strong demand for generic drugs in international markets. Exports increased by 18% to $25 billion, with the US and European markets being key contributors. Industry experts expect this momentum to continue in FY2025.",
        "source": "Pharma Pulse",
        "url": "https://example.com/pharma-growth-1",
        "published_date": "2025-01-28"
    },
    {
        "title": "Dr. Reddy's Laboratories receives FDA approval for new diabetes drug",
        "content": "Dr. Reddy's Laboratories announced FDA approval for its new diabetes management drug, expanding its portfolio in the therapeutic segment. The drug is expected to generate annual revenues of $150-200 million at peak sales. The stock surged 7% on the regulatory approval.",
        "source": "Business Wire",
        "url": "https://example.com/drreddy-fda-1",
        "published_date": "2025-01-29"
    },
    {
        "title": "Cipla partners with international firm for vaccine development",
        "content": "Cipla announced a strategic partnership with a leading international pharmaceutical company for the development and commercialization of a new vaccine candidate. The collaboration aims to accelerate vaccine development and expand market reach. Financial terms of the deal were not disclosed.",
        "source": "Mint",
        "url": "https://example.com/cipla-vaccine-1",
        "published_date": "2025-01-30"
    },
    {
        "title": "Coal India reports record production of 700 million tonnes",
        "content": "Coal India Limited reported record coal production of 700 million tonnes in FY2024, exceeding previous targets. The company's expansion initiatives and operational efficiency improvements contributed to this achievement. The government's push for domestic coal production to reduce import dependency supported this growth.",
        "source": "Coal India Press Release",
        "url": "https://example.com/coalindia-production-1",
        "published_date": "2025-01-31"
    },
    {
        "title": "NTPC announces 15% increase in renewable energy capacity",
        "content": "NTPC announced a 15% increase in its renewable energy capacity as part of its transition to clean energy. The company plans to invest Rs 50,000 crore in renewable projects over the next 5 years. This initiative aligns with India's target of 500 GW renewable energy capacity by 2030.",
        "source": "NTPC News",
        "url": "https://example.com/ntpc-renewable-1",
        "published_date": "2025-02-01"
    },
    {
        "title": "Power Grid Corporation reports 10% increase in transmission capacity",
        "content": "Power Grid Corporation of India reported a 10% increase in transmission capacity, supporting the country's growing electricity demand. The company completed several critical transmission projects ahead of schedule. Analysts expect this to improve grid stability and reduce transmission losses.",
        "source": "Power Grid Press",
        "url": "https://example.com/powergrid-capacity-1",
        "published_date": "2025-02-02"
    },
    {
        "title": "Bharti Airtel Q3 revenue grows 8% on 4G subscriber additions",
        "content": "Bharti Airtel reported Q3 revenue growth of 8% driven by strong 4G subscriber additions and improved average revenue per user (ARPU). The company added 5 million new 4G subscribers in the quarter. Management expects this momentum to continue with the rollout of 5G services.",
        "source": "Telecom News",
        "url": "https://example.com/airtel-q3-1",
        "published_date": "2025-02-03"
    },
    {
        "title": "Jio announces aggressive 5G expansion with 10,000 new towers",
        "content": "Reliance Jio announced plans to deploy 10,000 new 5G towers across India in the next quarter, accelerating its 5G network expansion. The company aims to provide 5G coverage to 50% of the population by end of FY2024. This expansion is expected to drive subscriber growth and ARPU improvement.",
        "source": "Jio Press",
        "url": "https://example.com/jio-5g-1",
        "published_date": "2025-02-04"
    },
    {
        "title": "Vodafone Idea reports Q3 loss, seeks regulatory relief",
        "content": "Vodafone Idea reported a significant Q3 loss and sought regulatory relief from the government. The company cited intense competition and high spectrum costs as challenges. The company's financial position remains precarious, with analysts questioning its long-term viability.",
        "source": "Telecom Regulatory Authority",
        "url": "https://example.com/vi-loss-1",
        "published_date": "2025-02-05"
    },
    {
        "title": "HDFC and ICICI Bank announce merger discussions",
        "content": "HDFC Bank and ICICI Bank announced preliminary discussions regarding a potential merger to create India's largest private sector bank. The merger would create a banking powerhouse with combined assets exceeding Rs 20 lakh crore. Regulatory approvals are expected within 12-18 months.",
        "source": "Reuters",
        "url": "https://example.com/hdfc-icici-merger-1",
        "published_date": "2025-02-06"
    },
    {
        "title": "Kotak Mahindra Bank reports 25% profit growth in Q3",
        "content": "Kotak Mahindra Bank reported a 25% increase in Q3 net profit, driven by strong loan growth and improved net interest margins. The bank's asset quality remained robust with NPA ratio at 1.5%. Management raised FY2024 guidance to 20% profit growth.",
        "source": "Stock Exchange",
        "url": "https://example.com/kotak-q3-1",
        "published_date": "2025-02-07"
    },
    {
        "title": "ICRA upgrades India's economic growth forecast to 7.2%",
        "content": "ICRA upgraded India's economic growth forecast for FY2024 to 7.2% from 6.8%, citing strong performance in services and manufacturing sectors. The rating agency expects inflation to moderate in Q4, supporting RBI's potential rate cut in the next fiscal year.",
        "source": "ICRA Press Release",
        "url": "https://example.com/icra-forecast-1",
        "published_date": "2025-02-08"
    },
    {
        "title": "Government announces Rs 1 lakh crore infrastructure investment",
        "content": "The Indian government announced a Rs 1 lakh crore infrastructure investment program focusing on roads, railways, and ports. This initiative is expected to create 2 million jobs and boost economic growth. The program will be implemented over the next 3 years.",
        "source": "Government Press Bureau",
        "url": "https://example.com/govt-infra-1",
        "published_date": "2025-02-09"
    },
    {
        "title": "Foreign investors increase India exposure amid market rally",
        "content": "Foreign institutional investors (FIIs) increased their India exposure significantly, investing Rs 15,000 crore in January 2024. The inflows were driven by India's strong economic fundamentals and attractive valuations compared to other emerging markets. Analysts expect FII inflows to continue supporting the market.",
        "source": "Market Watch",
        "url": "https://example.com/fii-inflows-1",
        "published_date": "2025-02-10"
    },
    {
        "title": "Sensex crosses 75,000 mark on strong corporate earnings",
        "content": "The BSE Sensex crossed the 75,000 mark for the first time, driven by strong corporate earnings and positive economic data. The index gained 8% in January 2024, outperforming other major global indices. Market analysts attribute this rally to improving corporate profitability and stable macroeconomic conditions.",
        "source": "BSE",
        "url": "https://example.com/sensex-75k-1",
        "published_date": "2025-02-11"
    },
    {
        "title": "Nifty 50 reaches all-time high on banking sector strength",
        "content": "The Nifty 50 index reached an all-time high, driven primarily by strength in the banking and financial services sectors. Major banks reported strong Q3 results, boosting investor confidence. The index gained 10% in the last quarter, significantly outperforming expectations.",
        "source": "NSE",
        "url": "https://example.com/nifty-ath-1",
        "published_date": "2025-02-12"
    }
]


def load_mock_data():
    """Load mock data into the database."""
    from database import get_db_connection
    from embeddings import get_embedding, serialize_embedding, detect_duplicate_articles , deserialize_embedding
    from groq_integration import extract_entities, map_stock_impact, analyze_sentiment
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    processed_articles = []

    for i, article in enumerate(MOCK_ARTICLES):
        try:
            # 1. Generate embedding
            embedding = get_embedding(article["content"])
            embedding_bytes = serialize_embedding(embedding)
            
            # 2. Check for duplicates against already processed articles
            is_duplicate = False
            canonical_id = None
            similarity_score = 0.0

            for pid, p_emb in processed_articles:
                is_dup, score = detect_duplicate_articles(embedding, p_emb, threshold=0.85)
                if is_dup:
                    is_duplicate = True
                    canonical_id = pid
                    similarity_score = score
                    # Keep the highest similarity found
                    break 

            # 3. Insert article
            cursor.execute("""
                INSERT INTO articles (title, content, source, url, published_date, embedding, is_duplicate, canonical_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article["title"],
                article["content"],
                article["source"],
                article["url"],
                article["published_date"],
                embedding_bytes,
                is_duplicate,
                canonical_id
            ))
            
            article_id = cursor.lastrowid

            # 4. If duplicate, insert into deduplication_records (THIS FIXES THE ANALYTICS)
            if is_duplicate:
                cursor.execute("""
                    INSERT INTO deduplication_records (article_id_1, article_id_2, similarity_score, is_duplicate)
                    VALUES (?, ?, ?, ?)
                """, (canonical_id, article_id, similarity_score, 1))
                print(f"  ↳ Detected duplicate of ID {canonical_id} (Score: {similarity_score:.2f})")
            else:
                # Add to processed list if it's a unique article
                processed_articles.append((article_id, embedding))
            
            # 5. Extract entities (Only for unique articles to save API costs, or all if you prefer)
            if not is_duplicate:
                entities_data = extract_entities(article["content"])
                
                # Insert Entities
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
                            impact_data = map_stock_impact(article["content"], entity_text)
                            
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

            print(f"✓ Loaded [{i+1}/{len(MOCK_ARTICLES)}]: {article['title'][:40]}...")
        
        except Exception as e:
            print(f"✗ Error loading article: {e}")
            import traceback
            traceback.print_exc()
    
    conn.commit()
    conn.close()
    print(f"\nSuccessfully loaded {len(MOCK_ARTICLES)} articles.")


if __name__ == "__main__":
    load_mock_data()
