import os
import typing
import github

from . import worker
import scripts


class GitHubJobPayload(
    typing.TypedDict,
):
    gh_client: github.Github
    repo_name: str
    user_name: str


class GitHubWorker(
    worker.Worker,
):
    def __init__(
        self,
    ):
        self.token = os.environ['GITHUB_ACCESS_TOKEN']

        self.gh_auth = github.Auth.Token(self.token)
        self.gh_client = github.Github(auth=self.gh_auth)

    def get_jobs_map(
        self,
    ) -> typing.Callable:
        jobs = {
            'enable_auto_security_fixes': scripts.enable_auto_security_fixes.enable_automated_security_fixes,
        }

        return jobs

    def work(
        self,
        message: dict,
    ) -> None:
        jobs_map = self.get_jobs_map()

        scheduled_job = message['scheduled_job']
        params = GitHubJobPayload(
            gh_client=self.gh_client,
            repo_name=message['repo_name'],
            user_name=message['user_name'],
        )

        jobs_map[scheduled_job](**params)
        