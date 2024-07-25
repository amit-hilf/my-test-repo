import pytest
import pytest_mock

import scripts

from . import scheduler
from .  import serverless_function
from . import param_store

@pytest.fixture
def mock_scheduler():
    return scheduler.MockScheduler()

@pytest.fixture
def mock_param_store():
    return param_store.MockParamStore()

@pytest.fixture
def mock_serverless_function():
    return serverless_function.MockServerlessFunction(
        name="enable_auto_security_fixes", 
        func=scripts.enable_auto_security_fixes.main,
    )

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
    mock_scheduler: scheduler.MockScheduler, 
    mock_param_store: param_store.MockParamStore, 
    mock_serverless_function: serverless_function.MockServerlessFunction,
    mock_get_repo: None,
):
    mock_param_store.set_param("script1_schedule", "rate(1 day)")
    schedule_expression = mock_param_store.get_param("script1_schedule")

    mock_scheduler.add_job("Script1", schedule_expression, mock_serverless_function.invoke)

    mock_scheduler.run_jobs()
