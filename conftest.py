import pytest
from helpers import Api


@pytest.fixture
def gist():
    api_operations = Api()
    return api_operations
