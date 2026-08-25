import feedparser


RSS_SOURCES = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "Google AI": "https://blog.google/technology/ai/rss/",
    "Hugging Face": "https://huggingface.co/blog/feed.xml",
}


def get_news():
    news = []

    for source_name, rss_url in RSS_SOURCES.items():
        try:
            feed = feedparser.parse(rss_url)

            for item in feed.entries[:10]:
                title = item.get("title", "").strip()
                link = item.get("link", "").strip()
                summary = item.get("summary", "").strip()

                if not title or not link:
                    continue

                news.append({
                    "source": source_name,
                    "title": title,
                    "link": link,
                    "summary": summary
                })

        except Exception as e:
            print(f"Error reading {source_name}: {e}")

    return news
