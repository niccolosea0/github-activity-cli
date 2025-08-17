#!/usr/bin/env python3
"""
GitHub User Activity CLI
A command-line tool to fetch and display recent GitHub user activity.
"""

import sys
import json
import urllib.request
import urllib.error
from typing import List, Dict


class GitHubActivityFetcher:
    """Handles fetching and processing GitHub user activity data."""

    BASE_URL = "https://api.github.com/users"

    def __init__(self):
        self.session_headers = {
            'User-Agent': 'GitHub-Activity-CLI/1.0',
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
            raise ValueError("Username cannot be empty")

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
                raise ValueError(f"User '{username}' not found")
            elif e.code == 403:
                raise ConnectionError("API rate limit exceeded. Please try again later.")
            else:
                raise ConnectionError(f"HTTP error {e.code}: {e.reason}")

        except urllib.error.URLError as e:
            raise ConnectionError(f"Network error: {e.reason}")

        except json.JSONDecodeError:
            raise ConnectionError("Invalid response from GitHub API")


class ActivityFormatter:
    """Formats GitHub activity data for terminal display."""

    EVENT_FORMATTERS = {
        'PushEvent': lambda event: f"Pushed {event['payload'].get('size', 0)} commit(s) to {event['repo']['name']}",
        'IssuesEvent': lambda event: f"{event['payload']['action'].capitalize()} an issue in {event['repo']['name']}",
        'WatchEvent': lambda event: f"Starred {event['repo']['name']}",
        'CreateEvent': lambda
            event: f"Created {event['payload'].get('ref_type', 'repository')} in {event['repo']['name']}",
        'ForkEvent': lambda event: f"Forked {event['repo']['name']}",
        'PullRequestEvent': lambda
            event: f"{event['payload']['action'].capitalize()} a pull request in {event['repo']['name']}",
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

        for event in events[:10]:  # Limit to most recent 10 events
            event_type = event.get('type')

            if event_type in cls.EVENT_FORMATTERS:
                try:
                    activity_text = cls.EVENT_FORMATTERS[event_type](event)
                    formatted_activities.append(f"- {activity_text}")
                except (KeyError, TypeError):
                    # Skip malformed events
                    continue
            else:
                # Handle unknown event types gracefully
                repo_name = event.get('repo', {}).get('name', 'unknown repository')
                formatted_activities.append(f"- {event_type} in {repo_name}")

        return formatted_activities


class GitHubActivityCLI:
    """Main CLI application class."""

    def __init__(self):
        self.fetcher = GitHubActivityFetcher()
        self.formatter = ActivityFormatter()

    def display_usage(self):
        """Display usage instructions."""
        print("Usage: python github_activity.py <username>")
        print("Example: python github_activity.py kamranahmedse")

    def run(self, args: List[str]):
        """
        Main entry point for the CLI application.

        Args:
            args: Command line arguments (excluding script name)
        """
        if len(args) != 1:
            print("Error: Please provide exactly one GitHub username.")
            self.display_usage()
            return 1

        username = args[0].strip()

        try:
            print(f"Fetching activity for GitHub user: {username}")
            print("-" * 50)

            # Fetch user activity
            events = self.fetcher.fetch_user_activity(username)

            if not events:
                print(f"No recent activity found for user '{username}'")
                return 0

            # Format and display activity
            formatted_activities = self.formatter.format_activity(events)

            if formatted_activities:
                print("Recent Activity:")
                for activity in formatted_activities:
                    print(activity)
            else:
                print(f"No displayable activity found for user '{username}'")

            return 0

        except ValueError as e:
            print(f"Error: {e}")
            return 1

        except ConnectionError as e:
            print(f"Connection Error: {e}")
            return 1

        except Exception as e:
            print(f"Unexpected error: {e}")
            return 1


def main():
    """Entry point when script is run directly."""
    cli = GitHubActivityCLI()
    exit_code = cli.run(sys.argv[1:])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()