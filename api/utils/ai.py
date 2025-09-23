from typing import Type

from orjson import dumps
from openai import AsyncClient
from pydantic import BaseModel

from api.core.config import settings

client = AsyncClient(api_key=settings.OPENAI_API_KEY)

PROMPT = """
Parse the food image and provide the information in JSON format with the following structure.
Return **only raw JSON**, do not wrap it in markdown or ```json blocks.

{schema}
"""

FALLBACK_PROMPT = """
You are a recovery system. Convert this text into valid JSON,
strictly following the schema below. Return only raw JSON, **no code blocks** or explanations.

Schema:
{schema}

Source text:
{raw_text}
"""

async def analyze_image_with_ai(
    image_url: str, 
    expected_schema: Type[BaseModel],
) -> str:
    ai_response = await client.responses.create( 
            model="gpt-4.1-mini",
            input=[{
                "role": "user",
                "content": [
                    {
                        "type": "input_text", 
                        "text": PROMPT.format(
                            schema=dumps(expected_schema.model_json_schema())
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": image_url,
                    },
                ]} # type: ignore
            ],
        )
    return ai_response.output_text


async def fallback_image_analyze(
    raw_response: str,
    expected_schema: Type[BaseModel],
) -> str:
    ai_response = await client.responses.create(
        model='gpt-4.1-mini',
        input=[
            {
                'role': 'user',
                'content': [{
                    'type': 'input_text',
                    'text': FALLBACK_PROMPT.format(
                        schema=dumps(expected_schema.model_json_schema()),
                        raw_text=raw_response,
                    ),
                }]
            } # type: ignore
        ]
    )
    if not ai_response.output_text:
        raise ValueError("Fallback model returned empty response")
    return ai_response.output_text
