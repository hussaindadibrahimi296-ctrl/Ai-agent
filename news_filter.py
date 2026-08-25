import re


# =========================================================
# STRONG AI KEYWORDS
# =========================================================

AI_KEYWORDS = [
    "artificial intelligence",
    "artificial intelligence model",
    "generative ai",
    "machine learning",
    "deep learning",
    "large language model",
    "language model",
    "llm",
    "foundation model",
    "ai model",
    "ai agent",
    "ai assistant",
    "ai chatbot",
    "ai coding",
    "coding agent",
    "ai search",
    "ai browser",
    "image generation",
    "video generation",
    "text-to-image",
    "text-to-video",
    "open source ai",
    "open-source ai",
]


# =========================================================
# IMPORTANT AI PRODUCTS / MODELS
# =========================================================

AI_PRODUCTS = [
    "gpt",
    "chatgpt",
    "gemini",
    "claude",
    "llama",
    "mistral",
    "qwen",
    "deepseek",
    "grok",
    "copilot",
    "perplexity",
    "hugging face",
    "openrouter",
    "midjourney",
    "stable diffusion",
    "flux",
    "runway",
    "cursor",
    "windsurf",
    "lovable",
    "replit",
]


# =========================================================
# HIGH VALUE NEWS
# =========================================================

HIGH_VALUE_KEYWORDS = [
    "new model",
    "new ai model",
    "new version",
    "new release",
    "released",
    "release",
    "launch",
    "launched",
    "introducing",
    "available now",
    "now available",
    "major update",
    "important update",
    "new feature",
    "new capabilities",
    "model update",
    "ai tool",
    "ai platform",
    "ai service",
]


# =========================================================
# FREE AI KEYWORDS
# =========================================================

FREE_KEYWORDS = [
    "free",
    "free plan",
    "free tier",
    "free version",
    "free access",
    "free users",
    "free to use",
    "available for free",
    "without paying",
    "no cost",
    "no payment",
    "open source",
    "open-source",
    "open weights",
    "free credits",
    "free usage",
    "free api",
    "free api access",
]


# =========================================================
# LOW VALUE / REJECT
# =========================================================

REJECT_KEYWORDS = [
    "politics",
    "political",
    "election",
    "war",
    "military",
    "russia",
    "ukraine",
    "israel",
    "iran",
    "influence campaign",
    "cyberattack",
    "malicious campaign",
    "security incident",
    "marketing",
    "advertising",
    "ads campaign",
    "football",
    "soccer",
    "sports",
    "partnership",
    "sponsorship",
    "home decor",
    "shopping",
    "fashion",
    "automotive",
    "car",
    "phone",
    "pixel",
]


def clean_text(text):
    text = text.lower()

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def contains_any(text, keywords):
    return any(
        keyword in text
        for keyword in keywords
    )


def is_strong_ai_news(item):

    title = clean_text(
        item.get("title", "")
    )

    summary = clean_text(
        item.get("summary", "")
    )

    text = f"{title} {summary}"

    # -----------------------------------------------------
    # Reject clearly irrelevant news
    # -----------------------------------------------------

    if contains_any(
        text,
        REJECT_KEYWORDS
    ):
        return False

    # -----------------------------------------------------
    # Must contain a real AI topic
    # -----------------------------------------------------

    has_ai_topic = contains_any(
        text,
        AI_KEYWORDS
    )

    has_ai_product = contains_any(
        text,
        AI_PRODUCTS
    )

    if not has_ai_topic and not has_ai_product:
        return False

    # -----------------------------------------------------
    # Must be a meaningful AI update
    # -----------------------------------------------------

    has_important_update = contains_any(
        text,
        HIGH_VALUE_KEYWORDS
    )

    has_free_signal = contains_any(
        text,
        FREE_KEYWORDS
    )

    # Accept:
    # 1. Important AI release/update
    # 2. Free AI announcement
    if not has_important_update and not has_free_signal:
        return False

    return True


def calculate_score(item):

    title = clean_text(
        item.get("title", "")
    )

    summary = clean_text(
        item.get("summary", "")
    )

    text = f"{title} {summary}"

    score = 0

    # AI topic
    for keyword in AI_KEYWORDS:
        if keyword in text:
            score += 2

    # Known AI product/model
    for keyword in AI_PRODUCTS:
        if keyword in text:
            score += 3

    # Important update
    for keyword in HIGH_VALUE_KEYWORDS:
        if keyword in text:
            score += 4

    # FREE = very important for our channel
    for keyword in FREE_KEYWORDS:
        if keyword in text:
            score += 8

    return score


def filter_news(news):

    filtered = []

    for item in news:

        if not is_strong_ai_news(item):
            continue

        item["score"] = calculate_score(item)

        filtered.append(item)

    # Highest-value news first
    filtered.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return filtered
