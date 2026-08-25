from sources import get_news
from database import load_seen_news, save_seen_news
from news_filter import filter_news


def main():
    print("AI News Agent started...")
    print("-" * 50)

    news = get_news()

    print(f"Total news found: {len(news)}")

    filtered_news = filter_news(news)

    print(f"AI news after filtering: {len(filtered_news)}")

    seen_news = load_seen_news()

    new_news = []

    for item in filtered_news:

        link = item["link"]

        if link in seen_news:
            continue

        new_news.append(item)
        seen_news.add(link)

    save_seen_news(seen_news)

    print(f"New AI news: {len(new_news)}")
    print()

    for item in new_news:

        print(f"Source: {item['source']}")
        print(f"Score: {item['score']}")
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print("-" * 50)


if __name__ == "__main__":
    main()
