from pytrends.request import TrendReq
import random
from datetime import datetime


class TrendSpotter:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def fetch_trending_topics(self):
        """
        Fetches trending financial topics with detailed metadata.
        Returns list of dicts with: topic, source, score, category
        """
        trends = []
        
        # Google Trends (Real)
        try:
            # Focusing on finance-related keywords
            kw_list = ["Bitcoin", "Stock Market", "Nvidia", "AI stocks", "Recession"]
            self.pytrends.build_payload(kw_list, cat=0, timeframe='now 1-d', geo='', gprop='')
            related_queries = self.pytrends.related_queries()
            
            for kw in kw_list:
                if related_queries and kw in related_queries:
                    top = related_queries[kw]['top']
                    if top is not None:
                        for query in top['query'].head(3).tolist():
                            trends.append({
                                "topic": query,
                                "source": "Google Trends",
                                "score": random.randint(70, 95),
                                "category": "search"
                            })
        except Exception as e:
            print(f"Error fetching Google Trends: {e}")
            # Fallback trends
            fallback = [
                "Bitcoin halving 2024",
                "Nvidia earnings beat",
                "Fed rate decision",
                "Tesla stock crash",
                "Dogecoin rally"
            ]
            for topic in fallback:
                trends.append({
                    "topic": topic,
                    "source": "Google Trends (fallback)",
                    "score": random.randint(60, 80),
                    "category": "search"
                })

        # Finance News Headlines (Simulated - would use NewsAPI or RSS in production)
        news_topics = [
            {"topic": "S&P 500 hits new all-time high", "category": "markets"},
            {"topic": "Crypto regulation bill passes Senate", "category": "crypto"},
            {"topic": "Housing market shows signs of cooling", "category": "real_estate"},
            {"topic": "Tech layoffs continue at major firms", "category": "employment"},
            {"topic": "Gold prices surge amid uncertainty", "category": "commodities"},
            {"topic": "Retail sales data misses expectations", "category": "economy"},
            {"topic": "AI stocks outperform broader market", "category": "tech"},
        ]
        
        for item in random.sample(news_topics, min(4, len(news_topics))):
            trends.append({
                "topic": item["topic"],
                "source": "Finance News",
                "score": random.randint(75, 95),
                "category": item["category"]
            })

        # Social Media Finance Trends (Simulated X/Twitter, Reddit)
        social_topics = [
            {"topic": "Solana's new memecoin goes viral", "category": "meme"},
            {"topic": "WSB discovers new short squeeze target", "category": "meme"},
            {"topic": "Crypto bro loses life savings on leverage", "category": "meme"},
            {"topic": "POV: checking your portfolio at 3am", "category": "meme"},
            {"topic": "When the Fed pivots but you're still broke", "category": "meme"},
            {"topic": "That feeling when your stop loss triggers", "category": "meme"},
            {"topic": "Elon tweets and market goes crazy", "category": "meme"},
            {"topic": "Day trader's perfect win streak ends", "category": "story"},
            {"topic": "Retail investors vs hedge funds round 2", "category": "story"},
        ]
        
        for item in random.sample(social_topics, min(5, len(social_topics))):
            trends.append({
                "topic": item["topic"],
                "source": "Social Media",
                "score": random.randint(80, 100) if item["category"] == "meme" else random.randint(65, 85),
                "category": item["category"]
            })

        # Educational Finance Topics (evergreen but trending)
        educational_topics = [
            {"topic": "How compound interest actually works", "category": "education"},
            {"topic": "Common mistakes beginner traders make", "category": "education"},
            {"topic": "Understanding market cycles and timing", "category": "education"},
            {"topic": "Risk management strategies that work", "category": "education"},
            {"topic": "Reading candlestick patterns correctly", "category": "education"},
            {"topic": "Dollar cost averaging vs lump sum", "category": "education"},
        ]
        
        for item in random.sample(educational_topics, min(3, len(educational_topics))):
            trends.append({
                "topic": item["topic"],
                "source": "Educational",
                "score": random.randint(70, 90),
                "category": "education"
            })
        
        # Sort by score and return
        trends.sort(key=lambda x: x['score'], reverse=True)
        return trends

    def get_high_potential_topics(self, count_range=(5, 15)):
        """
        Get high potential topics for video generation.
        Ensures mix of educational and meme content.
        """
        all_trends = self.fetch_trending_topics()
        
        # Separate by category
        meme_trends = [t for t in all_trends if t['category'] in ['meme', 'story']]
        serious_trends = [t for t in all_trends if t['category'] not in ['meme', 'story']]
        
        # Determine count
        target_count = random.randint(*count_range)
        
        # 70% serious, 30% meme
        meme_count = int(target_count * 0.30)
        serious_count = target_count - meme_count
        
        # Select topics
        selected = []
        selected.extend(random.sample(meme_trends, min(meme_count, len(meme_trends))))
        selected.extend(random.sample(serious_trends, min(serious_count, len(serious_trends))))
        
        # Shuffle to mix them
        random.shuffle(selected)
        
        return selected[:target_count]


if __name__ == "__main__":
    spotter = TrendSpotter()
    print("All Trending Topics:")
    for trend in spotter.fetch_trending_topics()[:10]:
        print(f"  - {trend['topic']} ({trend['category']}) - Score: {trend['score']}")
    
    print("\nHigh Potential Topics:")
    for trend in spotter.get_high_potential_topics():
        print(f"  - {trend['topic']} ({trend['category']})")

