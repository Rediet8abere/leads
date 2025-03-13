from pydantic import BaseModel
from typing_extensions import Optional

class ClientBase(BaseModel):
    firstname: str
    lastname: str
    email: str
    resume: str

class AttorneyBase(BaseModel):
    firstname: str
    lastname: str
    email: str

class ClientUpdateBase(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    resume: Optional[str] = None

class ClientStateUpdateBase(BaseModel):
    state: Optional[str] = None