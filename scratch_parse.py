import sys
sys.path.insert(0, '.')
from agents.architect_agent.architect_agent import parse_new_file_lines
import json

with open("dashboard/tasks/live_593.json", "r") as f:
    data = json.load(f)
    
plan = data.get("plan", "")
print("PLAN:", repr(plan))
print("PARSED:", list(parse_new_file_lines(plan)))

