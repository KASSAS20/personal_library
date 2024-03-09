import pytest
from app.main import app
from fastapi.testclient import TestClient
from random import randint
client = TestClient(app)


class TestRegistration:
    url = '/auth/registration'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    @pytest.mark.parametrize(
        "headers, url, login, password, result",
        [
            (headers, url, str(randint(100, 1000000)), 'correct_password', 200),
            (headers, url, 'a', 'correct_password', 400),
            (headers, url, 'test_correct_name', 'a', 400),
            (headers, url, 'a', 'a', 422),
            (headers, url, 'test_name', 'test_name', 422)
        ]
    )
    def test_connect_and_validation(self, headers, url, login, password, result):
        payload = {
            "login": f'{login}',
            "password": f'{password}'
        }
        response = client.post(url, json=payload, headers=headers)
        assert response.status_code == result



