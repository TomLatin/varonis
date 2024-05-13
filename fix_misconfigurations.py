import requests
from typing import List
from github import Github

# GitHub authentication token
TOKEN = ''

# Initialize PyGithub with token
g = Github(TOKEN)
# # Repository information
REPO_OWNER = "TomLatin"
REPO_NAME = "varonis"


def main():
    # Perform checks and fixes for each configuration
    check_and_fix_config("Protected Branches", check_protected_branches, fix_protected_branches)
    check_and_fix_config("Dependabot Alerts", check_dependabot_alerts, fix_dependabot_alerts)
    check_and_fix_config("Private Repository Status", check_private_repo, fix_private_repo)

# Function to check and fix configuration
def check_and_fix_config(configuration_name, check_function, fix_function=None):
    print(f"\nChecking {configuration_name} configuration...")
    config_status = check_function()
    print(f"{configuration_name} configuration status: {config_status}")

    if not config_status and fix_function:
        print(f"Fixing {configuration_name} configuration...")
        fix_function()
        print(f"{configuration_name} configuration fixed successfully!")


# Function to check if protected branches are configured
def check_protected_branches():
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    branches = repo.get_branches()
    for branch in branches:
        if branch.protected:
            return True
    return False


# Function to fix protected branches configuration
def fix_protected_branches():
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    branch_to_protect = "master"  # Example branch
    branch = repo.get_branch(branch_to_protect)
    branch.edit_protection(enforce_admins=True, require_code_owner_reviews=True, required_approving_review_count=1,
                           dismiss_stale_reviews=True)


# Function to check if Dependabot alerts are enabled
def check_dependabot_alerts():
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    alerts = repo.get_vulnerability_alert()
    return alerts


# Function to enable Dependabot alerts
def fix_dependabot_alerts():
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    repo.enable_vulnerability_alert()

def check_private_repo():
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    return repo.private


# Function to transfer repository to private
def fix_private_repo():
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    if not repo.private:
        repo.edit(private=True)
        print("Repository transferred to private successfully!")

if __name__ == '__main__':
    main()
