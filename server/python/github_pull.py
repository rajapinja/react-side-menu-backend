from github import Github

# Your GitHub personal access token
token = 'YOUR_ACCESS_TOKEN'

# GitHub organization or repository name
organization_name = 'your-organization'
repository_name = 'your-repository'

# Teams and team names
team_names = ['team1', 'team2', 'team3']

# Initialize the GitHub API client
g = Github(token)

# Get the organization or repository
org = g.get_organization(organization_name)
repo = org.get_repo(repository_name)

# Function to automatically approve Pull Requests
def auto_approve_pull_requests(team_name):
    team = org.get_team_by_slug(team_name)
    if not team:
        print(f"Team '{team_name}' not found.")
        return

    for pr in repo.get_pulls(state='open', base='master'):
        if pr.user.login != team_name:
            pr.create_review(event="APPROVE")
            print(f"Pull Request #{pr.number} approved by {team_name}.")

# Loop through the specified teams and auto-approve PRs
for team_name in team_names:
    auto_approve_pull_requests(team_name)
