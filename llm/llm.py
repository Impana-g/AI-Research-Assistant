from openai import OpenAI
from config.settings import OPENROUTER_API_KEY, BASE_URL, MODEL_NAME

# Create OpenRouter client
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)


def generate_response(user_query):
    """
    Sends the user's question to the LLM
    and returns the generated response.
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
                "content": user_query
            }
        ]
    )

    return response.choices[0].message.content