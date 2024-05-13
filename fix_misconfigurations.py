from github import Github
from typing import Callable, Any

# GitHub authentication token
TOKEN = ''

# Initialize PyGithub with token
g = Github(TOKEN)

# Repository information
REPO_OWNER = "TomLatin"
REPO_NAME = "varonis"


def main():
    # Perform checks and fixes for each configuration
    check_and_fix_config("Protected Branches", check_protected_branches, fix_protected_branches)
    check_and_fix_config("Dependabot Alerts", check_dependabot_alerts, fix_dependabot_alerts)
    check_and_fix_config("Private Repository Status", check_private_repo, fix_private_repo)


# Function to check and fix configuration
def check_and_fix_config(configuration_name: str, check_function: Callable[[], bool],
                         fix_function: Callable[[], None] = None) -> None:
    print(f"\nChecking {configuration_name} configuration...")
    config_status = check_function()
    print(f"{configuration_name} configuration status: {config_status}")

    if not config_status and fix_function:
        print(f"Fixing {configuration_name} configuration...")
        fix_function()
        print(f"{configuration_name} configuration fixed successfully!")


def check_protected_branches() -> bool:
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    branches = repo.get_branches()
    for branch in branches:
        if branch.protected:
            return False
    return True


def fix_protected_branches() -> None:
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    branches = repo.get_branches()
    for branch in branches:
        if not branch.protected:
            branch.edit_protection(enforce_admins=True, require_code_owner_reviews=True,
                                   required_approving_review_count=1,
                                   dismiss_stale_reviews=True)


def check_dependabot_alerts() -> bool:
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    alerts = repo.get_vulnerability_alert()
    return alerts


def fix_dependabot_alerts() -> None:
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    repo.enable_vulnerability_alert()


def check_private_repo() -> bool:
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    return repo.private


def fix_private_repo() -> None:
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    if not repo.private:
        repo.edit(private=True)
        print("Repository transferred to private successfully!")


if __name__ == '__main__':
    main()
