
import json
import subprocess
import os
import re

def run_command(command, cwd=None):
    """Runs a command and returns its output."""
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd,
        )
        return process.stdout, process.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr

def parse_mypy_output(output):
    """Parses mypy's text output into a list of JSON objects."""
    issues = []
    # Example line: backend/api/main.py:123: error: "MyModel" has no attribute "foobar"  [attr-defined]
    pattern = re.compile(r"([^:]+):(\d+):(?:\d+:)? (\w+): (.+)")
    for line in output.strip().split('\n'):
        match = pattern.match(line)
        if match:
            file_path, line_num, level, message = match.groups()
            issues.append({
                "file_path": file_path,
                "line": int(line_num),
                "level": level,
                "message": message.strip(),
            })
    return issues


def main():
    """
    Runs linting and type checking on the backend and frontend,
    and outputs the issues in a JSON file.
    """
    all_issues = {
        "ruff": [],
        "mypy": [],
        "eslint": [],
    }

    # Install dependencies
    print("Installing backend dependencies...")
    run_command(["pip", "install", "ruff", "mypy"])
    print("Installing frontend dependencies...")
    run_command(["npm", "install"], cwd="client/my-content-app")


    # Backend - ruff
    print("Running ruff...")
    ruff_stdout, ruff_stderr = run_command(["ruff", "check", "backend/", "--output-format=json"])
    if ruff_stdout:
        try:
            all_issues["ruff"] = json.loads(ruff_stdout)
        except json.JSONDecodeError:
            print("Could not parse ruff JSON output")
            all_issues["ruff"] = {"error": "Could not parse JSON", "output": ruff_stdout}


    # Backend - mypy
    print("Running mypy...")
    mypy_stdout, mypy_stderr = run_command(["mypy", "backend/"])
    all_issues["mypy"] = parse_mypy_output(mypy_stderr or mypy_stdout)


    # Frontend - eslint
    print("Running eslint...")
    eslint_stdout, eslint_stderr = run_command(
        ["npm", "run", "lint", "--", "--format", "json"],
        cwd="client/my-content-app",
    )
    if eslint_stdout:
        try:
            # ESLint might output other things before the JSON, so we find the start of it.
            json_start_index = eslint_stdout.find('[')
            if json_start_index != -1:
                eslint_json_output = eslint_stdout[json_start_index:]
                all_issues["eslint"] = json.loads(eslint_json_output)
        except json.JSONDecodeError:
            print("Could not parse eslint JSON output")
            all_issues["eslint"] = {"error": "Could not parse JSON", "output": eslint_stdout}


    # Write output to file
    with open("linting_issues.json", "w") as f:
        json.dump(all_issues, f, indent=4)

    print("Linting and type checking complete. Issues saved to linting_issues.json")

if __name__ == "__main__":
    main()
