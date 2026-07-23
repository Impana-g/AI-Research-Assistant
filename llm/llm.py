from openai import OpenAI
from config.settings import OPENROUTER_API_KEY, BASE_URL, MODEL_NAME

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)

def generate_response(user_query, context):

    prompt = f"""
You are an AI Research Assistant.

Answer the user's question ONLY using the provided context.

If the answer is not available in the context, say:
"I couldn't find that information in the uploaded document."

Context:
{context}

Question:
{user_query}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI Research Assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content