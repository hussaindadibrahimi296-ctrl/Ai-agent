import json
import os

from openai import OpenAI


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def judge_news(item):

    title = item.get("title", "")
    summary = item.get("summary", "")
    source = item.get("source", "")
    link = item.get("link", "")

    prompt = f"""
You are the final editor of an AI news Telegram channel.

Your job is to decide whether this news article is worth publishing.

CHANNEL FOCUS:
- New AI models
- New AI tools
- Important AI features
- Free AI tools
- Free AI plans
- Free tiers
- Open-source AI
- Open-weight AI models
- Important AI updates

REJECT:
- Marketing case studies
- Ordinary company announcements
- Sports
- Politics
- General technology news
- Partnerships without important AI news
- Advertising
- Corporate promotion
- Security/political incidents unless they introduce an important AI product/model
- News that is not genuinely useful to AI users

IMPORTANT:
Do not approve an article just because it mentions ChatGPT, Gemini,
Claude or another AI product.

The article must contain meaningful and useful AI news.

ARTICLE:

Source:
{source}

Title:
{title}

Summary:
{summary}

Link:
{link}

Return ONLY valid JSON:

{{
  "publish": true,
  "score": 0,
  "reason": "short reason"
}}

Score from 0 to 100.

Publishing rules:
- 80-100 = excellent AI news
- 65-79 = good AI news
- 50-64 = borderline
- below 50 = reject

Give especially high scores to:
- New AI models
- Free AI
- Free tiers
- Open-source AI
- Open-weight models
- Major new AI capabilities
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    result = response.output_text.strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        return {
            "publish": False,
            "score": 0,
            "reason": "Invalid AI response"
        }
