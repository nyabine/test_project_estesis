from pydantic import BaseModel


class ErrorModel(BaseModel):
    error: str


class SuccessModel(BaseModel):
    success: bool
    