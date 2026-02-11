from pydantic import BaseModel

class EquationRequest(BaseModel):
    expression: str

class EquationResponse(BaseModel):
    input: str
    solution: str
    steps: list
