
import google.generativeai as genai

from retriever import retrieve_assessments
from prompts import SYSTEM_PROMPT

GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"


genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


REFUSAL_KEYWORDS = [
    "legal",
    "salary",
    "fire employee",
    "court",
]


COMPARE_KEYWORDS = [
    "difference",
    "compare",
    "vs",
]


def is_vague(user_message):

    vague_phrases = [
        "need assessment",
        "hiring",
        "test",
    ]

    lowered = user_message.lower()

    if len(lowered.split()) <= 3:
        return True

    for phrase in vague_phrases:
        if phrase == lowered.strip():
            return True

    return False



def should_refuse(message):

    lowered = message.lower()

    for word in REFUSAL_KEYWORDS:
        if word in lowered:
            return True

    return False



def is_comparison(message):

    lowered = message.lower()

    for word in COMPARE_KEYWORDS:
        if word in lowered:
            return True

    return False



def build_conversation(messages):

    conversation = ""

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        conversation += f"{role}: {content}\n"

    return conversation



def generate_reply(messages):

    latest_user_message = messages[-1]["content"]

    if should_refuse(latest_user_message):

        return {
            "reply": "I can only help with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False,
        }

    if is_vague(latest_user_message):

        return {
            "reply": "Can you share the role, seniority level, and important skills you want to assess?",
            "recommendations": [],
            "end_of_conversation": False,
        }

    retrieved = retrieve_assessments(latest_user_message, top_k=5)

    context = "\n\n".join(
        [
            f"""
            Name: {item['name']}
            Description: {item['description']}
            URL: {item['url']}
            Type: {item['test_type']}
            """
            for item in retrieved
        ]
    )

    conversation = build_conversation(messages)

    prompt = f"""
    {SYSTEM_PROMPT}

    Conversation:
    {conversation}

    Retrieved Catalog:
    {context}

    Generate a grounded recommendation response.
    """

    response = model.generate_content(prompt)

    recommendations = []

    for item in retrieved:

        recommendations.append(
            {
                "name": item["name"],
                "url": item["url"],
                "test_type": item["test_type"],
            }
        )

    return {
        "reply": response.text,
        "recommendations": recommendations[:10],
        "end_of_conversation": True,
    }
