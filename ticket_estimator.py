import os
import sys
from dotenv import load_dotenv
from jira import JIRA
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

STORY_POINT_FIELD = "customfield_10028"  # Confirmed story point field
PROJECT_KEY = "PNAV"

class TicketEstimator:
    def __init__(self):
        self.jira = JIRA(
            server=os.getenv('JIRA_URL'),
            basic_auth=(os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_TOKEN'))
        )
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def get_ticket_by_key(self, key):
        try:
            return self.jira.issue(key)
        except Exception as e:
            print(f"❌ Could not fetch ticket {key}: {e}")
            return None

    def get_done_tickets_with_story_points(self, prefix=None, max_results=500):
        try:
            jql = (
                f'project = {PROJECT_KEY} AND statusCategory = Done AND issuetype = Story '
            )

            if prefix:
                jql += f'AND summary ~ "{prefix} " '

            jql += 'ORDER BY created DESC'

            return self.jira.search_issues(jql, maxResults=max_results)
        except Exception as e:
            print(f"❌ Error fetching issues: {e}")
            return []

    def compute_similarity(self, desc1, desc2):
        emb1 = self.model.encode(desc1)
        emb2 = self.model.encode(desc2)
        return cosine_similarity([emb1], [emb2])[0][0]

    def fibonacci_round_up(self, value):
        fibonacci = [1, 2, 3, 5, 8, 13, 20, 40, 100]
        for f in fibonacci:
            if f >= value:
                return f
        return value

    def estimate(self, ticket_key):
        ticket = self.get_ticket_by_key(ticket_key)
        if not ticket:
            return

        desc = f"{ticket.fields.summary or ''} {ticket.fields.description or ''}".strip()
        print(f"\n🎯 Estimating for: {desc}\n")

        prefix = None
        if ticket.fields.summary:
            if ticket.fields.summary.startswith("FE"):
                prefix = "FE"
            elif ticket.fields.summary.startswith("Android"):
                prefix = "Android"
            elif ticket.fields.summary.startswith("iOS"):
                prefix = "iOS"

        done_tickets = self.get_done_tickets_with_story_points(prefix=prefix)
        if not done_tickets:
            print("⚠️ No closed tickets with story points found.")
            return

        similarities = []
        for t in done_tickets:
            print(f"summary{t.fields.summary}")
            t_desc = f"{t.fields.summary or ''} {t.fields.description or ''}".strip()
            sim = self.compute_similarity(desc, t_desc)
            sp = getattr(t.fields, STORY_POINT_FIELD, None)
            if sp is not None:
                similarities.append((sim, sp, t.key))

        if not similarities:
            print("⚠️ No similar tickets with story points.")
            return

        top = sorted(similarities, key=lambda x: x[0], reverse=True)[:5]
        estimated = sum(sp for _, sp, _ in top) / len(top)
        fib_estimate = self.fibonacci_round_up(round(estimated, 1))

        print(f"✅ Estimated Story Points: {round(estimated, 1)} → Fibonacci Rounded: {fib_estimate}")
        print("\n🔍 Most Similar Tickets:")
        for sim, sp, key in top:
            fib = self.fibonacci_round_up(sp)
            print(f" - {key}: {sp} pts → {fib} (Fibonacci) (Similarity: {sim:.2f})")

# ----------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python ticket_estimator.py <TICKET_KEY>")
        sys.exit(1)

    key = sys.argv[1].strip().upper()
    estimator = TicketEstimator()
    estimator.estimate(key)
