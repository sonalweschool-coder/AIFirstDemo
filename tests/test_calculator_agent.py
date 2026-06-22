from fastapi.testclient import TestClient

from app.agent import CalculatorAgent
from app.main import app


def test_percentage_calculation() -> None:
    result = CalculatorAgent().run("calculate 20% of 8500")

    assert result.task == "percentage calculation"
    assert result.tool == "calculator"
    assert result.answer == 1700


def test_basic_arithmetic_calculation() -> None:
    result = CalculatorAgent().run("calculate 12 * (5 + 3)")

    assert result.task == "multiplication calculation"
    assert result.answer == 96


def test_api_calculate() -> None:
    client = TestClient(app)

    response = client.post("/api/calculate", json={"prompt": "calculate 10 percent of 250"})

    assert response.status_code == 200
    assert response.json()["answer"] == 25
