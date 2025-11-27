import openai, json, os

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

CLASSIFICATION_PROMPT = """
Classify content asset. Return ONLY JSON:
persona (Buyer-Finance, Buyer-Marketing, Buyer-IT, Buyer-Exec, CS, Developer),
funnel_stage (Awareness, Consideration, Decision, Retention, Expansion),
topic (short text),
intent (Learn, Evaluate, Compare, Buy, Troubleshoot, Upsell),
summary (1 sentence).
Content:
Title: {title}
Text: {text}
"""

def classify_asset(title, text):
    prompt = CLASSIFICATION_PROMPT.format(title=title, text=text[:1800])
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"You are a content classifier. Return only JSON."},
                  {"role":"user","content":prompt}],
        temperature=0.0,
        max_tokens=400
    )
    out = resp["choices"][0]["message"]["content"]
    return json.loads(out)

