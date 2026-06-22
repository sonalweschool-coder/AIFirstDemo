from pydantic import BaseModel

from app.tools.calculator import CalculatorTool


class AgentResult(BaseModel):
    task: str
    reasoning: str
    tool: str
    answer: float | int


class CalculatorAgent:
    """A tiny rule-based agent that chooses the calculator tool for math tasks."""

    def __init__(self) -> None:
        self.calculator = CalculatorTool()

    def run(self, user_input: str) -> AgentResult:
        task = self._understand_task(user_input)
        answer = self.calculator.execute(user_input)

        return AgentResult(
            task=task,
            reasoning=f"I need {task}, so I will use the calculator tool.",
            tool=self.calculator.name,
            answer=answer,
        )

    def _understand_task(self, user_input: str) -> str:
        lowered = user_input.lower()
        if "%" in lowered or "percent" in lowered or "percentage" in lowered:
            return "percentage calculation"
        if any(word in lowered for word in ("multiply", "times", "*", " x ")):
            return "multiplication calculation"
        if any(word in lowered for word in ("divide", "divided", "/")):
            return "division calculation"
        if any(word in lowered for word in ("add", "sum", "plus", "+")):
            return "addition calculation"
        if any(word in lowered for word in ("subtract", "minus", "-")):
            return "subtraction calculation"
        return "mathematical calculation"
