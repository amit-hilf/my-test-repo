import github
import os
import github.Repository
import requests


def is_automated_security_fixes_enabled(
    repo_name: str,
    user_name: str,
    token: str,
) -> bool:
    r = requests.get(
        url=f'https://api.github.com/repos/{user_name}/{repo_name}/automated-security-fixes',
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {token}',
            'X-GitHub-Api-Version': '2022-11-28',
        }
    )
    r.raise_for_status()

    content = r.json()

    return content['enabled']

def enable_automated_security_fixes(
    gh_client: github.Github,
    repo_name: str,
    user_name: str,
) -> None:
    repo = gh_client.get_repo(
        f'{user_name}/{repo_name}',
    )

    vuln_alerts_enabled = repo.enable_vulnerability_alert()
    if not vuln_alerts_enabled:
        raise Exception(
            'enable_vulnerability_alert method failed',
        )
    auto_security_fixes_enabled = repo.enable_automated_security_fixes()
    if not auto_security_fixes_enabled:
        raise Exception(
            'enable_automated_security_fixes failed'
        )
    
    print(f'vulnerability alerts and security fixes enabled for {repo}')


def main():
    token = os.environ['GITHUB_ACCESS_TOKEN']
    repo_name = os.environ['GITHUB_REPO_NAME']
    user_name = os.environ['GITHUB_USER_NAME']

    gh_auth = github.Auth.Token(token)
    gh_client = github.Github(auth=gh_auth)

    is_enabled = is_automated_security_fixes_enabled(
        repo_name=repo_name,
        user_name=user_name,
        token=token,
    )
    if not is_enabled:
        print(
            f'auto security fixes is currently disabled for {repo_name}, executing remediation'
        )
        enable_automated_security_fixes(
            gh_client=gh_client,
            repo_name=repo_name,
            user_name=user_name,
        )

    gh_client.close()

if __name__ == '__main__':
    main()
