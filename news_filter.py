import re


AI_KEYWORDS = [
    "artificial intelligence",
    "artificial intelligence",
    "ai",
    "generative ai",
    "gen ai",
    "machine learning",
    "deep learning",
    "llm",
    "large language model",
    "language model",
    "ai model",
    "foundation model",
    "open source ai",
    "open-source ai",
    "free ai",
    "free ai tool",
    "ai tool",
    "ai assistant",
    "ai agent",
    "ai chatbot",
    "text to image",
    "text-to-image",
    "text to video",
    "text-to-video",
    "image generation",
    "video generation",
    "ai coding",
    "coding agent",
    "ai search",
    "ai browser",
]

HIGH_VALUE_KEYWORDS = [
    "new model",
    "new ai",
    "launch",
    "launched",
    "introducing",
    "release",
    "released",
    "available",
    "free",
    "free tier",
    "open source",
    "open-source",
    "open weights",
    "new version",
    "update",
    "major update",
    "gpt",
    "gemini",
    "claude",
    "llama",
    "mistral",
    "qwen",
    "deepseek",
    "groq",
    "hugging face",
]


def clean_text(text):
    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_ai_news(item):
    text = clean_text(
        f"{item.get('title', '')} {item.get('summary', '')}"
    )

    has_ai_keyword = any(
        keyword in text
        for keyword in AI_KEYWORDS
    )

    if not has_ai_keyword:
        return False

    return True


def calculate_score(item):
    text = clean_text(
        f"{item.get('title', '')} {item.get('summary', '')}"
    )

    score = 0

    for keyword in AI_KEYWORDS:
        if keyword in text:
            score += 1

    for keyword in HIGH_VALUE_KEYWORDS:
        if keyword in text:
            score += 3

    return score


def filter_news(news):
    filtered = []

    for item in news:

        if not is_ai_news(item):
            continue

        item["score"] = calculate_score(item)

        filtered.append(item)

    filtered.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return filtered
