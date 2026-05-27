import subprocess
from pathlib import Path


class QualityCheckService:
    PROJECT_ROOT = Path.cwd()

    @staticmethod
    def run_command(command: list[str]) -> dict:
        result = subprocess.run(
            command,
            cwd=QualityCheckService.PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False
        )

        return {
            "command": " ".join(command),
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "passed": result.returncode == 0
        }

    @staticmethod
    def run_quality_gates() -> dict:
        checks = {
            "syntax_check": QualityCheckService.run_command([
                "python",
                "-m",
                "compileall",
                "generated/code",
                "generated/tests"
            ]),
            "ruff_format": QualityCheckService.run_command([
                "ruff",
                "format",
                "generated/code",
                "generated/tests"
            ]),
            "ruff_check": QualityCheckService.run_command([
                "ruff",
                "check",
                "generated/code",
                "generated/tests",
                "--fix"
            ]),
            "pytest": QualityCheckService.run_command([
                "pytest",
                "generated/tests"
            ]),
            "security_scan": QualityCheckService.run_command([
                "bandit",
                "-r",
                "generated/code"
            ])
        }

        overall_status = "passed"

        for check in checks.values():
            if not check["passed"]:
                overall_status = "failed"
                break

        return {
            "overall_status": overall_status,
            "checks": checks
        }