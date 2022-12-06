from fastapi import HTTPException, status
from pydantic import BaseModel, constr, validator

class ContentDTO(BaseModel):
    content: constr()
    @validator('content')
    def check_content(cls, v):
        if v == "" or len(v) > 300: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content가 잘못됨.")
        return v