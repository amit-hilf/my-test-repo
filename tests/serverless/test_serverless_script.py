import pytest

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

def test_run_script(
    mock_scheduler: scheduler.MockScheduler, 
    mock_param_store: param_store.MockParamStore, 
    mock_serverless_function: serverless_function.MockServerlessFunction,
):
    mock_param_store.set_param("script1_schedule", "rate(1 day)")
    schedule_expression = mock_param_store.get_param("script1_schedule")

    mock_scheduler.add_job("Script1", schedule_expression, mock_serverless_function.invoke)

    mock_scheduler.run_job()
