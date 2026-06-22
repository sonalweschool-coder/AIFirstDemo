import ast
import operator
import re


class CalculatorTool:
    name = "calculator"

    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def execute(self, user_input: str) -> float | int:
        percentage_result = self._try_percentage(user_input)
        if percentage_result is not None:
            return self._clean_number(percentage_result)

        expression = self._extract_expression(user_input)
        result = self._safe_eval(expression)
        return self._clean_number(result)

    def _try_percentage(self, user_input: str) -> float | None:
        match = re.search(
            r"(-?\d+(?:\.\d+)?)\s*(?:%|percent|percentage)\s*(?:of|from)?\s*(-?\d+(?:\.\d+)?)",
            user_input,
            flags=re.IGNORECASE,
        )
        if not match:
            return None
        percentage, base = (float(match.group(1)), float(match.group(2)))
        return base * percentage / 100

    def _extract_expression(self, user_input: str) -> str:
        expression = user_input.lower()
        replacements = {
            "calculate": "",
            "what is": "",
            "please": "",
            "add": "+",
            "plus": "+",
            "sum of": "+",
            "subtract": "-",
            "minus": "-",
            "multiply": "*",
            "multiplied by": "*",
            "times": "*",
            "x": "*",
            "divide": "/",
            "divided by": "/",
        }
        for word, replacement in replacements.items():
            expression = expression.replace(word, replacement)

        expression = re.sub(r"[^0-9+\-*/().\s]", "", expression)
        expression = re.sub(r"\s+", " ", expression).strip()
        if not expression:
            raise ValueError("Please enter a mathematical expression.")
        return expression

    def _safe_eval(self, expression: str) -> float:
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError("I could not understand that calculation.") from exc
        return float(self._evaluate_node(tree.body))

    def _evaluate_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in self._operators:
            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)
            return float(self._operators[type(node.op)](left, right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._operators:
            operand = self._evaluate_node(node.operand)
            return float(self._operators[type(node.op)](operand))
        raise ValueError("Only basic arithmetic is supported.")

    def _clean_number(self, value: float) -> float | int:
        if value.is_integer():
            return int(value)
        return round(value, 8)
