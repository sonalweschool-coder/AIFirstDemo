from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.agent import CalculatorAgent

app = FastAPI(title="AIFirstDemo Calculator Agent")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

agent = CalculatorAgent()


class CalculationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, examples=["calculate 20% of 8500"])


class CalculationResponse(BaseModel):
    task: str
    reasoning: str
    tool: str
    answer: float | int


@app.get("/")
def index() -> FileResponse:
    return FileResponse("app/static/index.html")


@app.post("/api/calculate", response_model=CalculationResponse)
def calculate(request: CalculationRequest) -> CalculationResponse:
    result = agent.run(request.prompt)
    return CalculationResponse(**result.model_dump())
