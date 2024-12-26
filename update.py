import os
import subprocess
from datetime import datetime

# Configuration
REPO_DIR = os.path.dirname(os.path.abspath(__file__))  # Current directory
BRANCH = "main"  # Replace with your branch name

def run_command(command, cwd=None):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}\n{e.stderr}")
        return None

def check_and_push_updates():
    """Check for changes and push updates to GitHub."""
    os.chdir(REPO_DIR)

    # Check the Git status
    status = run_command(["git", "status", "--porcelain"])
    if not status:
        print("No changes detected.")
        return

    # Stage changes
    run_command(["git", "add", "."])
    print("Changes staged.")

    # Commit changes
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_command(["git", "commit", "-m", f\"Automated update at {timestamp}\"])
    print("Changes committed.")

    # Push changes to GitHub
    result = run_command(["git", "push", "origin", BRANCH])
    if result:
        print("Changes pushed to GitHub.")
    else:
        print("Failed to push changes to GitHub.")

if __name__ == "__main__":
    check_and_push_updates()
