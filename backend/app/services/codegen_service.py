import json
from pathlib import Path
from app.services.path_policy_service import PathPolicyService
from app.services.llm_service import LLMService



class CodegenService:
    PROJECT_ROOT = Path.cwd()

    @staticmethod
    async def generate_code(spec: dict, plan: dict) -> dict:
        with open("app/prompts/codegen_prompt.txt", "r", encoding="utf-8") as file:
            template = file.read()

        prompt = (
            template
            .replace("__SPEC__", json.dumps(spec, indent=2))
            .replace("__PLAN__", json.dumps(plan, indent=2))
        )

        response = await LLMService.generate(prompt)

        cleaned_response = CodegenService._clean_json_response(response)

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

    @staticmethod
    def normalize_code_content(content: str) -> str:
        if content is None:
            raise ValueError("Generated file content is missing")
   
        if "\\n" in content:
            content = content.replace("\\r\\n", "\n")
            content = content.replace("\\n", "\n")

 
        if "\\t" in content:
            content = content.replace("\\t", "\t")


        if '\\"' in content:
            content = content.replace('\\"', '"')


        if "\\'" in content:
            content = content.replace("\\'", "'")

        return content.strip() + "\n"

    @staticmethod
    def write_generated_files(generated_code: dict) -> list[dict]:
        files = generated_code.get("files", [])

        written_files = []

        for file in files:
            relative_path = file.get("path")
            content = file.get("content")

            if not relative_path:
                raise ValueError("Generated file path is missing")

            PathPolicyService.validate_generated_path(relative_path)

            normalized_content = CodegenService.normalize_code_content(
                content
            )

            target_path = CodegenService.PROJECT_ROOT / relative_path

            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(normalized_content, encoding="utf-8")

            written_files.append({
                "path": relative_path,
                "absolute_path": str(target_path)
            })

        return written_files