from openai import OpenAI

from app.core.config import OPENROUTER_API_KEY, MODEL_NAME
from app.core.logger import logger


if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not configured")

if not MODEL_NAME:
    raise ValueError("MODEL_NAME is not configured")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


class LLMService:

    @staticmethod
    async def generate(prompt: str):

        logger.info(f"Calling LLM model: {MODEL_NAME}")

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content