import re


# =========================================================
# AI TOPICS
# =========================================================

AI_KEYWORDS = [
    "artificial intelligence",
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
]


# =========================================================
# AI MODELS / PRODUCTS
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
    "replit",
    "gemma",
    "phi",
    "kimi",
    "glm",
]


# =========================================================
# VERY IMPORTANT AI EVENTS
# =========================================================

NEW_MODEL_KEYWORDS = [
    "new model",
    "new ai model",
    "new llm",
    "new language model",
    "new foundation model",
    "introducing",
    "introduced",
    "launch",
    "launched",
    "release",
    "released",
    "available now",
    "now available",
]


NEW_FEATURE_KEYWORDS = [
    "new feature",
    "new capability",
    "new capabilities",
    "major update",
    "major upgrade",
    "model update",
    "important update",
    "version",
    "upgraded",
    "upgrade",
]


# =========================================================
# FREE AI
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
    "no cost",
    "free credits",
    "free usage",
    "free api",
    "free api access",
]


# =========================================================
# OPEN SOURCE / OPEN WEIGHTS
# =========================================================

OPEN_KEYWORDS = [
    "open source",
    "open-source",
    "open source ai",
    "open-source ai",
    "open weights",
    "open-weight",
    "open model",
    "weights released",
    "model weights",
    "download the model",
    "self-host",
    "self hosted",
]


# =========================================================
# REJECT LOW-VALUE CONTENT
# =========================================================

REJECT_KEYWORDS = [
    "marketing campaign",
    "advertising campaign",
    "ads campaign",
    "marketing",
    "sponsorship",
    "sponsored",
    "partnership",
    "football",
    "soccer",
    "sports",
    "home decor",
    "shopping",
    "fashion",
    "car",
    "automotive",
    "phone partnership",
    "politics",
    "political",
    "election",
    "war",
    "military",
    "russia",
    "ukraine",
    "influence campaign",
    "covert influence",
    "malicious campaign",
    "cyberattack",
    "security incident",
    "customer story",
    "case study",
    "cuts launch hours",
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


def calculate_score(item):

    title = clean_text(
        item.get("title", "")
    )

    summary = clean_text(
        item.get("summary", "")
    )

    text = f"{title} {summary}"

    score = 0

    # -----------------------------------------------------
    # Basic AI relevance
    # -----------------------------------------------------

    if contains_any(text, AI_KEYWORDS):
        score += 3

    if contains_any(text, AI_PRODUCTS):
        score += 3

    # -----------------------------------------------------
    # New model = very important
    # -----------------------------------------------------

    if contains_any(text, NEW_MODEL_KEYWORDS):
        score += 8

    # -----------------------------------------------------
    # New feature / major update
    # -----------------------------------------------------

    if contains_any(text, NEW_FEATURE_KEYWORDS):
        score += 6

    # -----------------------------------------------------
    # FREE AI = highest priority
    # -----------------------------------------------------

    if contains_any(text, FREE_KEYWORDS):
        score += 10

    # -----------------------------------------------------
    # OPEN SOURCE / OPEN WEIGHTS
    # -----------------------------------------------------

    if contains_any(text, OPEN_KEYWORDS):
        score += 9

    return score


def filter_news(news):

    filtered = []

    for item in news:

        title = clean_text(
            item.get("title", "")
        )

        summary = clean_text(
            item.get("summary", "")
        )

        text = f"{title} {summary}"

        # -------------------------------------------------
        # Reject obviously bad content
        # -------------------------------------------------

        if contains_any(
            text,
            REJECT_KEYWORDS
        ):
            continue

        # -------------------------------------------------
        # Must actually be AI related
        # -------------------------------------------------

        has_ai = (
            contains_any(text, AI_KEYWORDS)
            or
            contains_any(text, AI_PRODUCTS)
        )

        if not has_ai:
            continue

        # -------------------------------------------------
        # Calculate score
        # -------------------------------------------------

        item["score"] = calculate_score(item)

        # -------------------------------------------------
        # Minimum quality threshold
        # -------------------------------------------------

        if item["score"] < 8:
            continue

        filtered.append(item)

    # Highest value first
    filtered.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return filtered
