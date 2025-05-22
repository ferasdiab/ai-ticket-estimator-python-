# AI Ticket Estimator

A local tool that estimates story points for Jira tickets using sentence embeddings and similarity matching.

## Features

- Uses local sentence transformers for generating embeddings
- Connects to Jira API to fetch historical tickets
- Caches ticket data locally to minimize API calls
- Estimates story points based on similarity to past tickets
- Simple CLI interface

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your Jira credentials:
   ```
   JIRA_URL=your_jira_instance_url
   JIRA_EMAIL=your_email@example.com
   JIRA_API_TOKEN=your_api_token
   ```

   To get your Jira API token:
   1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
   2. Click "Create API token"
   3. Give it a name and copy the token
   4. Paste it in the .env file

## Usage

Run the script with:
```bash
python ticket_estimator.py
```

You can then:
1. Enter a new ticket description directly
2. Or provide a Jira ticket key to fetch its description

The tool will:
- Show the top 5 most similar past tickets
- Provide a story point estimate based on similar tickets
- Cache the results for future use

## How it Works

1. The tool uses the `all-MiniLM-L6-v2` model to generate embeddings for ticket descriptions
2. It maintains a local cache of past tickets with their story points
3. For new tickets, it:
   - Generates an embedding
   - Finds the most similar past tickets using cosine similarity
   - Averages the story points of the top 5 matches
   - Provides the estimate along with similar tickets for reference

## Note

This tool runs entirely locally and doesn't require any cloud services or paid APIs. 