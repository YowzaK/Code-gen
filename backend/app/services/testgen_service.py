import json

from app.services.llm_service import LLMService
from app.core.logger import logger


class TestgenService:

    @staticmethod
    async def generate_tests(
        spec: dict,
        plan: dict,
        generated_code: dict
    ) -> dict:
        with open("app/prompts/testgen_prompt.txt", "r", encoding="utf-8") as file:
            template = file.read()

        prompt = (
            template
            .replace("__SPEC__", json.dumps(spec, indent=2))
            .replace("__PLAN__", json.dumps(plan, indent=2))
            .replace("__GENERATED_CODE__", json.dumps(generated_code, indent=2))
        )

        logger.info("Generating automated tests from generated code artifacts")

        response = await LLMService.generate(prompt)

        cleaned_response = TestgenService._clean_json_response(response)

        return json.loads(cleaned_response)

    @staticmethod
    def _clean_json_response(response: str) -> str:
        response = response.strip()

        if response.startswith("```json"):
            response = response.replace("```json", "", 1).strip()

        if response.startswith("```"):
            response = response.replace("```", "", 1).strip()

        if response.endswith("```"):
            response = response[:-3].strip()

        return response