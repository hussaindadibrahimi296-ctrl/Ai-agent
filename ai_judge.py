import json
import os

from google import genai


client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


MODEL = "gemini-2.5-flash"


def judge_news(item):

    title = item.get("title", "")
    summary = item.get("summary", "")
    source = item.get("source", "")
    link = item.get("link", "")

    prompt = f"""
You are the final editor of a Telegram channel about AI news.

Your job is to decide whether this article is worth publishing.

CHANNEL FOCUS:

1. New AI models
2. New AI tools
3. Important AI features
4. Free AI tools
5. Free AI plans
6. Free tiers
7. Open-source AI
8. Open-weight AI models
9. Important AI updates
10. Useful AI tools for ordinary users

VERY IMPORTANT:

The channel strongly prefers FREE AI.

Give high priority to:
- Completely free AI tools
- Free AI plans
- Free tiers
- Free API access
- Free credits
- Open-source AI
- Open-weight AI
- AI models that users can download
- New AI models
- Major new AI capabilities

REJECT:

- Marketing case studies
- Ordinary company announcements
- Advertising
- Sponsorships
- Partnerships without important AI news
- Sports
- Politics
- General technology news
- Corporate promotion
- Customer stories
- News that only mentions an AI product
- News that is not useful to AI users
- Duplicate or insignificant updates

IMPORTANT:

Do NOT approve an article simply because it contains
words such as GPT, Gemini, Claude or AI.

Understand the actual meaning of the article.

The article must contain genuinely useful and newsworthy
information about AI.

ARTICLE:

Source:
{source}

Title:
{title}

Summary:
{summary}

Link:
{link}

Return ONLY valid JSON.

Required format:

{{
  "publish": true,
  "score": 0,
  "category": "free_ai",
  "reason": "short explanation"
}}

SCORING:

90-100 = extremely valuable
80-89 = excellent
70-79 = good
60-69 = borderline
0-59 = reject

Scoring priorities:

New free AI model:
+ very high

New free AI tool:
+ very high

Free tier:
+ very high

Open-source model:
+ very high

Open-weight model:
+ very high

New AI model:
+ high

Major AI capability:
+ high

Normal AI update:
+ medium

Marketing/case study:
- very high

Unimportant partnership:
- very high

Return JSON only.
"""

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        result = response.text.strip()

        # Remove accidental markdown code fences
        if result.startswith("```"):
            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

        return json.loads(result)

    except Exception as e:

        print(f"Gemini error: {e}")

        return {
            "publish": False,
            "score": 0,
            "category": "error",
            "reason": "Gemini request failed"
            }
