from pathlib import PurePosixPath


class PathPolicyService:
    ALLOWED_PREFIXES = [
        "generated/code/",
        "generated/tests/"
    ]

    @staticmethod
    def validate_generated_path(path: str) -> None:
        normalized_path = str(PurePosixPath(path))

        if normalized_path.startswith("/"):
            raise ValueError(f"Absolute paths are not allowed: {path}")

        if not any(
            normalized_path.startswith(prefix)
            for prefix in PathPolicyService.ALLOWED_PREFIXES
        ):
            raise ValueError(
                f"Generated path is outside approved directories: {path}"
            )