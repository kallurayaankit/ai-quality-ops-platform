"""One-command demo runner.

Usage:  python demo/run.py
Runs docker compose on the demo compose file, then prints the report path.
"""

import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).parent.parent
    compose_file = root / "docker-compose.demo.yml"

    if not compose_file.exists():
        print(f"ERROR: {compose_file} not found")
        sys.exit(1)

    cmd = [
        "docker", "compose",
        "-f", str(compose_file),
        "up", "--build",
        "--abort-on-container-exit",
        "--exit-code-from", "test-runner",
    ]

    print("Running demo...")
    print(" ".join(cmd))
    print()

    result = subprocess.run(cmd, cwd=root)

    report = root / "reports" / "summary.html"
    print()
    if report.exists():
        print(f"Report: {report}")
        print(f"Open it in your browser: file:///{report}")
    else:
        print("No report generated.")

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()