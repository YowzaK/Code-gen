import json

from app.services.llm_service import LLMService
from app.core.logger import logger


class PlannerService:

    @staticmethod
    async def generate_plan(spec: dict):

        with open("app/prompts/planner_prompt.txt", "r", encoding="utf-8") as file:
            template = file.read()

        prompt = template.replace(
            "__SPEC__",
            json.dumps(spec, indent=2)
        )

        logger.info("Generating implementation plan from pipeline spec")

        response = await LLMService.generate(prompt)

        cleaned_response = PlannerService._clean_json_response(response)

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