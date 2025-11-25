from pytrends.request import TrendReq
import random

class TrendSpotter:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def fetch_trending_topics(self):
        """
        Fetches trending financial topics from Google Trends and simulates X (Twitter) trends.
        """
        trends = []
        
        # Google Trends (Real)
        try:
            # Focusing on finance-related keywords
            kw_list = ["Bitcoin", "Stock Market", "Nvidia", "AI", "Recession"]
            self.pytrends.build_payload(kw_list, cat=0, timeframe='now 1-d', geo='', gprop='')
            related_queries = self.pytrends.related_queries()
            
            for kw in kw_list:
                if related_queries and kw in related_queries:
                    top = related_queries[kw]['top']
                    if top is not None:
                        trends.extend(top['query'].head(3).tolist())
        except Exception as e:
            print(f"Error fetching Google Trends: {e}")
            # Fallback if Google Trends fails or blocks
            trends.extend(["Bitcoin Crash", "Nvidia Earnings", "Fed Rate Cut"])

        # Simulated X (Twitter) Trends (Mock for now as X API is expensive/restricted)
        # In a real scenario, we would use tweepy or similar here.
        x_trends = [
            "Solana Breakout",
            "Tech Layoffs",
            "Housing Market Bubble",
            "Crypto Regulation",
            "Elon Musk Tweet"
        ]
        
        trends.extend(x_trends)
        
        # Deduplicate and shuffle
        unique_trends = list(set(trends))
        random.shuffle(unique_trends)
        
        return unique_trends[:5] # Return top 5 mixed trends

if __name__ == "__main__":
    spotter = TrendSpotter()
    print("Trending Topics:", spotter.fetch_trending_topics())
