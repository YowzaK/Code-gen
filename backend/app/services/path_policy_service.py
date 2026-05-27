from pathlib import PurePosixPath


class PathPolicyService:
    ALLOWED_PREFIXES = [
        "generated/code/"
    ]

    #for future use when i need to add more strict guardrails 
    BLOCKED_PATTERNS = [
        # "...",
        # "todo",
        # "pass",
        # "implementation omitted",
        # "omitted for brevity",
        # "placeholder",
        # "your code here"
    ]

    @staticmethod
    def validate_generated_path(path: str) -> None:
        normalized_path = str(PurePosixPath(path))

        if normalized_path.startswith("/"):
            raise ValueError(f"Absolute paths are not allowed: {path}")

        for blocked_pattern in PathPolicyService.BLOCKED_PATTERNS:
            if blocked_pattern in normalized_path:
                raise ValueError(
                    f"Generated path contains blocked pattern: {path}"
                )

        if not any(
            normalized_path.startswith(prefix)
            for prefix in PathPolicyService.ALLOWED_PREFIXES
        ):
            raise ValueError(
                f"Generated path is outside approved directories: {path}"
            )