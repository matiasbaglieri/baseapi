from pydantic import BaseModel
from typing import Optional, Any, Dict

class BaseResponse(BaseModel):
    message: str
    status: str
    data: Optional[Dict[str, Any]] = None 