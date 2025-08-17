# GitHub User Activity CLI

### Description

This project is a simple command-line tool that fetches and displays recent GitHub user activity directly in your terminal. Built with Python using only standard library modules, it demonstrates clean code architecture, proper error handling, and API consumption without any external dependencies.

The application allows you to:
- Fetch recent activity from any public GitHub user
- Display activities in a clean, readable format
- Handle various GitHub events (pushes, issues, stars, forks, etc.)
- Gracefully manage errors like invalid usernames or network issues
- Learn about HTTP APIs, JSON processing, and CLI development

All communication happens through GitHub's REST API v3, and the tool follows best practices for API interaction including proper headers, timeout handling, and rate limit awareness.

---

## Features

- **Fetch User Activity:** Get the 10 most recent activities from any GitHub user
- **Smart Event Formatting:** Converts GitHub API events into human-readable descriptions
- **Comprehensive Error Handling:** Manages network errors, invalid users, and API failures
- **Clean Architecture:** Well-organized code with separation of concerns
- **No Dependencies:** Uses only Python standard library modules
- **Professional API Interaction:** Includes proper headers and follows GitHub API guidelines
- **Educational Value:** Great example of OOP, error handling, and API consumption

---

## Installation

1. **Download the script:**
   ```bash
   # Clone or download github_activity.py
   wget [your-file-url] -O github_activity.py
   # OR create the file and copy the code manually
   ```

2. **Make it executable (optional):**
   ```bash
   chmod +x github_activity.py
   ```

3. **Verify Python installation:**
   ```bash
   python3 --version  # Should show Python 3.6+
   ```

No additional dependencies required! The script uses only Python's built-in modules.

---

## Usage

### Basic Usage
```bash

# Try with popular users
python3 github_activity.py torvalds
python3 github_activity.py octocat


### Error Handling Examples
```bash
# Invalid username
python3 github_activity.py nonexistentuser123
# Output: Error: User 'nonexistentuser123' not found

# No arguments
python3 github_activity.py
# Output: Error: Please provide exactly one GitHub username.
#         Usage: python github_activity.py <username>

# Network issues
# Output: Connection Error: Network error: [specific error message]
```

---

## Supported GitHub Events

The tool recognizes and formats these GitHub activity types:

- **PushEvent** - Code pushes to repositories
- **IssuesEvent** - Opening/closing issues
- **WatchEvent** - Starring repositories
- **CreateEvent** - Creating repositories or branches
- **ForkEvent** - Forking repositories
- **PullRequestEvent** - Pull request activities
- **DeleteEvent** - Deleting branches or tags
- **ReleaseEvent** - Creating releases
- **PublicEvent** - Making repositories public

Unknown event types are handled gracefully with a generic format.

---

## Technical Details

### Architecture
- **GitHubActivityFetcher:** Handles API communication and data retrieval
- **ActivityFormatter:** Converts raw GitHub events into readable text
- **GitHubActivityCLI:** Manages user interaction and application flow

### Key Technologies
- **HTTP API Consumption:** Uses `urllib.request` for GitHub API calls
- **JSON Processing:** Parses GitHub's JSON responses
- **Error Handling:** Comprehensive exception management
- **Object-Oriented Design:** Clean separation of concerns

### GitHub API Integration
- Uses GitHub REST API v3
- Includes proper User-Agent header
- Handles rate limiting gracefully
- Processes various event types

---

## Learning Opportunities

This project demonstrates several important computer science concepts:

1. **API Consumption:** How to interact with RESTful web APIs
2. **JSON Data Processing:** Parsing and manipulating structured data
3. **Error Handling:** Graceful failure management and user feedback
4. **HTTP Protocol:** Understanding web communication fundamentals
5. **Command-Line Interface Design:** Creating user-friendly terminal tools
6. **Object-Oriented Programming:** Clean code architecture and design patterns

---

## Possible Enhancements

Want to take this project further? Consider adding:

- **Caching:** Store API responses to reduce requests
- **Filtering:** Filter activities by event type or date
- **Configuration:** Support GitHub API tokens for higher rate limits
- **Colorized Output:** Add colors for better readability
- **Detailed Information:** Show more event details like commit messages
- **Multiple Users:** Compare activity between users
- **Export Options:** Save activity to files (JSON, CSV, etc.)

---

## Troubleshooting

### Common Issues

**Python not found:**
```bash
sudo apt update
sudo apt install python3
```

**Permission denied:**
```bash
chmod +x github_activity.py
```

**Network connectivity:**
```bash
ping api.github.com
```

**API rate limiting:**
Wait a few minutes or consider using a GitHub personal access token.

---

## Contributing

This is an educational project! Feel free to:
- Fork and experiment with the code
- Add new features or improve existing ones
- Share your enhanced versions
- Use it as a starting point for more complex GitHub tools

---

## License

This project is open source and available for educational purposes.

---

**Happy coding! 🚀**
