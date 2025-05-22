import os
from dotenv import load_dotenv
from jira import JIRA
from ticket_estimator import TicketEstimator

def test_jira_connection():
    """Test the Jira connection using credentials from .env file"""
    load_dotenv()
    
    try:
        # Initialize Jira client
        jira = JIRA(
            server=os.getenv('JIRA_URL'),
            basic_auth=(os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_TOKEN'))
        )

        print(f"JIRA_API_TOKEN: {os.getenv('JIRA_API_TOKEN')}")

        # Construct JQL to search by various fields
        search_text = "PNAV-24609"
        jql = (
            # f'text ~ "{search_text}" '
            # f'OR summary ~ "{search_text}" '
            # f'OR description ~ "{search_text}" '
            f'key = "{search_text.upper()}" '
            # f'ORDER BY created DESC'
        )

        issues = jira.search_issues(jql, maxResults=100, validate_query=False)
        
        for issue in issues:
         print(f"\nIssue Key: {issue.key}")
         print(f"Summary: {issue.fields.summary}")
        #  print(f"Description: {issue.fields.description}")
         print(f"story point: {issue.fields.customfield_10028}")
         print(f"Status: {issue.fields.status.name}")
        #  print(f"All Fields: {issue.raw['fields']}")

        print(f"issues: {issues}")

        if issues:
            print("✅ Successfully connected to Jira!")
            print(f"Found issue: {issues[0].key} - {issues[0].fields.summary}")
        else:
            print("⚠️ Connected to Jira but no issues found in the project.")
            
    except Exception as e:
        print("❌ Failed to connect to Jira:")
        print(f"Error: {str(e)}")
        return False
    
    return True

def test_estimator():
    """Test the ticket estimator functionality"""
    try:
        estimator = TicketEstimator()
        print("\nTesting ticket estimator...")

        test_description = "Implement user authentication with OAuth2"
        print(f"\nTesting with description: '{test_description}'")

        points, similar_tickets = estimator.estimate_story_points(test_description)

        print(f"\nEstimated Story Points: {round(points, 1)}")
        print("\nSimilar Tickets:")
        for ticket, similarity in similar_tickets:
            print(f"\nTicket: {ticket['key']}")
            print(f"Summary: {ticket['summary']}")
            print(f"Story Points: {ticket['story_points']}")
            print(f"Similarity: {similarity:.2f}")

    except Exception as e:
        print("❌ Error testing ticket estimator:")
        print(f"Error: {str(e)}")
        return False

    return True

if __name__ == "__main__":
    print("Testing Jira Connection and Ticket Estimator...")
    print("----------------------------------------------")

    if test_jira_connection():
        test_estimator()
