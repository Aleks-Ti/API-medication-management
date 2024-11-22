from pydantic import BaseModel


class PreBase(BaseModel):
    class Config:
        from_attributes = True
