import github
import datetime

import github.PaginatedList
import github.Secret
import os

def get_repo_secrets(
    gh_client: github.Github,
    repo: str,
    username: str,
) -> github.PaginatedList.PaginatedList:
    repo = gh_client.get_repo(
        f'{username}/{repo}',
    )

    secrets = repo.get_secrets()
    return secrets

def is_secret_outdated(
    gh_secret: github.Secret,
) -> bool:
    if gh_secret.updated_at < datetime.datetime.now(gh_secret.updated_at.tzinfo) - datetime.timedelta(days=365):
        print(f'Secret needs to be regenerated - {gh_secret.name}')

def main():
    TOKEN = os.environ['GITHUB_ACCESS_TOKEN']

    REPO_NAME = 'my-test-repo'
    USER_NAME = 'amit-hilf'

    gh_auth = github.Auth.Token(TOKEN)
    gh_client = github.Github(auth=gh_auth)

    gh_secrets = get_repo_secrets(
        gh_client=gh_client,
        repo=REPO_NAME,
        username=USER_NAME,
    )

    for gh_secret in gh_secrets:
        is_secret_outdated(
            gh_secret=gh_secret,
        )

    gh_client.close()

if __name__ == '__main__':
    main()
