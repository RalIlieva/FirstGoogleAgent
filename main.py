# main.py — run the ADK dev UI or terminal chat from PyCharm
import os, subprocess, sys

# Choose one:
MODE = os.environ.get("ADK_MODE", "web")  # "web" or "run"

if MODE == "web":
    cmd = ["adk", "web"]
else:
    cmd = ["adk", "run", "multi_tool_agent"]

# Runs with whatever venv PyCharm is using for this run config.
sys.exit(subprocess.call(cmd))
