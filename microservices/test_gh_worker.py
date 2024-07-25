import pytest
import pytest_mock

from . import workers

@pytest.fixture
def mock_message():
    return {
        'scheduled_job': 'enable_auto_security_fixes',
        'repo_name': 'my-test-repo',
        'user_name': 'amit-hilf',
    }

@pytest.fixture
def mock_get_repo(mocker: pytest_mock.MockerFixture):
    get_repo_response = mocker.patch('github.Github.get_repo')
    class MockedRepoObject:
        def __init__(
            self,
        ) -> None:
            pass

        def enable_vulnerability_alert(
            self,
        ):
            return True
        
        def enable_automated_security_fixes(
            self,
        ):
            return True

    get_repo_response.return_value = MockedRepoObject()
    yield

def test_run_script(
    mock_message: dict,
    mock_get_repo: None,
):
    github_worker = workers.gh_worker.GitHubWorker()
    github_worker.work(
        message=mock_message
    )
