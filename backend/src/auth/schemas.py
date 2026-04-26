from pydantic import BaseModel
from datetime import datetime

class BaseUser(BaseModel):
    id: int
    name: str
    created_at: datetime
    picture: str


class User(BaseUser):
    email: str
    google_id: str = None
    
    
class UserPublic(BaseUser):
    pass