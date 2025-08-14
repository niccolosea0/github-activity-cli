"""
GitHub User Activity CLI
A command-line tool to fetch and display recent GitHub user activity
"""

import sys
import json
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Optional

class GitHubActivityFetcher:
    """Handles fetching and processing GitHub user activity data"""
    BASE_URL = "https://api.github.com/user"

    def __init__(self):
        self.session_headers = {
            'User_Agent': 'GitHub-Activity-CLI/1.0',
            'Accept': 'application/vnd.github.v3+json'
        }

    def fetch_user_activity(self, username: str) -> List[Dict]:
        """
        Fetch recent activity for a GitHub user.

        Args:
            username: GitHub username to fetch activity for

        Returns:
            List of activity events as dictionaries

        Raises:
            ValueError: If username is invalid
            ConnectionError: If API request fails
        """
        if not username or not username.strip():
            raise ValueError('Username cannot be empty')

        url = f"{self.BASE_URL}/{username}/events"

        try:
            request = urllib.request.Request(url, headers=self.session_headers)

            with urllib.request.urlopen(request, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return data
                else:
                    raise ConnectionError(f"API returned status code: {response.status}")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ValueError(f"User: '{username}' not found")
            elif e.code == 403:
                raise ConnectionError("API rate limit exceeded. Please try again later")
            else:
                raise ConnectionError(f"HTTP error {e.code}: {e.reason}")

        except urllib.error.URLError as e:
            raise ConnectionError(f"Network error: {e.reason}")

        except json.JSONDecodeError:
            raise ConnectionError("Invalid response from GitHub API")

class ActivityFormatter:
    """Formats GitHub activity data for terminal display"""

    EVENT_FORMATTERS = {
        'PushEvent': lambda event: f"Pushed {event['payload'].get('size', 0)} commit(s) to {event['repo']['name']}",
        'IssuesEvent': lambda event: f"{event['payload']['action'].capitalize()} an issue in {event['repo']['name']}",
        'WatchEvent': lambda event: f"Starred {event['repo']['name']}",
        'CreateEvent': lambda event: f"Created {event['payload'].get('ref_type', 'repository')} in {event['repo']['name']}",
        'ForkEvent': lambda event: f"Forked {event['repo']['name']}",
        'PullRequestEvent': lambda event: f"{event['payload']['action'].capitalize()} a pull request in {event['repo']['name']}",
        'DeleteEvent': lambda event: f"Deleted {event['payload'].get('ref_type', 'branch')} in {event['repo']['name']}",
        'ReleaseEvent': lambda event: f"{event['payload']['action'].capitalize()} a release in {event['repo']['name']}",
        'PublicEvent': lambda event: f"Made {event['repo']['name']} public",
    }

    @classmethod
    def format_activity(cls, events: List[Dict]) -> List[str]:
        """
        Format activity events into readable strings.

        Args:
            events: List of GitHub event dictionaries

        Returns:
            List of formatted activity strings
        """
        formatted_activities = []

        for event in events[:10]: # Limit to most recent 10 events
            event_type = event.get('type')

            if event_type in cls.EVENT_FORMATTERS:
                try:
                    activity_text = cls.EVENT_FORMATTERS[event_type](event)
                    formatted_activities.append(f"- {activity_text}")
                except (KeyError, TypeError):
                    continue

            else:
                # Handle unknown event types
                repo_name = event.get('repo', {}).get('name', 'unknown repository')
                formatted_activities.append(f"- {event_type} in {repo_name}")

        return formatted_activities



