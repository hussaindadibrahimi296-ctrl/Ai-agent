from sources import get_news


def main():
    print("AI News Agent started...")
    print("-" * 50)

    news = get_news()

    print(f"Found {len(news)} news articles.")
    print()

    for item in news:
        print(f"Source: {item['source']}")
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print("-" * 50)


if __name__ == "__main__":
    main()
