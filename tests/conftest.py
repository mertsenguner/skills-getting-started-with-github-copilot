import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


def pytest_configure(config):
    # Ensure the FastAPI app is available to pytest discovery if needed
    config.addinivalue_line("markers", "fastapi: mark test as using FastAPI app")


@pytest.fixture(autouse=True)
def reset_activities_state():
    original_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


@pytest.fixture()
def client():
    return TestClient(app)
