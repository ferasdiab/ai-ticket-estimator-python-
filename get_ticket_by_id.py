import os
from dotenv import load_dotenv
from jira import JIRA
import json

# Load environment variables from .env
load_dotenv()

# Setup JIRA client
jira = JIRA(
    server=os.getenv('JIRA_URL'),
    basic_auth=(os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_TOKEN'))
)

def fetch_ticket(ticket_key: str):
    try:
        issue = jira.issue(ticket_key)
        
        print("\n✅ Ticket Found")
        print(f"issue: {issue}")
        print(f"Summary: {issue.fields.summary}")
        print(f"Status: {issue.fields.status.name}")
        
        print("\n📦 Full Fields JSON:")
        print(json.dumps(issue.raw['fields'], indent=2))

        print("\n🔍 Common Custom Fields:")
        for k, v in issue.raw['fields'].items():
            if 'point' in k.lower():
                print(f"{k}: {v}")

    except Exception as e:
        print("❌ Failed to fetch ticket")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Replace with your ticket key or pass via input
    ticket_key = "PNAV-24609"
    fetch_ticket(ticket_key)
