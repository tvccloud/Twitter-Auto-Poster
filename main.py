import os
import time
import random
import logging
import sys
import tweepy
import feedparser

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Load credentials
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
    logging.error("Missing Twitter credentials. Exiting.")
    sys.exit(1)

# Twitter client
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET,
    wait_on_rate_limit=True
)

# Blocked keywords
BLOCKED = {
    "politics", "election", "government", "minister",
    "bjp", "congress", "parliament", "president",
    "religion", "god", "hindu", "islam", "christian",
    "temple", "mosque", "church", "israel", "palestine"
}

def is_safe(text):
    t = text.lower()
    return not any(word in t for word in BLOCKED)

def get_trending_topics(limit=5):
    feed = feedparser.parse(
        "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    )
    topics = []
    for entry in feed.entries:
        title = entry.get("title", "")
        if title and is_safe(title):
            topics.append(title)
        if len(topics) >= limit:
            break
    return topics

TEMPLATES = [
    "{topic}. This is gaining attention today.",
    "A lot of people are discussing: {topic}",
    "Trending now: {topic}",
    "Seeing increased buzz around {topic}.",
    "{topic} is worth keeping an eye on."
]

def main():
    topics = get_trending_topics()
    if not topics:
        logging.info("No safe topics found.")
        return

    for topic in topics:
        tweet = random.choice(TEMPLATES).format(topic=topic)[:270]
        client.create_tweet(text=tweet)
        logging.info("Tweet posted.")
        time.sleep(random.randint(15, 45))

if __name__ == "__main__":
    main()
