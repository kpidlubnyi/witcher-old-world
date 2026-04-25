from pydantic import BaseModel, field_validator, computed_field
import time
import arrow

class Lobby(BaseModel):
    id: str
    host_id: int
    host_name: str
    name: str | None = None
    max_players: int = 4
    created_at: int = None

    @field_validator("created_at", mode="before")
    @classmethod
    def set_created_at(cls, v):
        return v or int(time.time())

    @field_validator("name", mode="before")
    @classmethod
    def set_name(cls, v, info):
        if v:
            return v
        data = info.data
        return f"lobbies #{data.get('id', '')}"
    

class CreateLobby(BaseModel):
    name: str
    max_players: int

    @field_validator("max_players")
    @classmethod
    def validate_players(cls, v):
        if not (2 <= v < 6):
            raise ValueError("max_players must be between 2 and 5")
        return v
    
class LobbyResponse(Lobby):
    id: str
    host_id: int
    host_name: str
    name: str | None = None
    max_players: int = 4
    created_at: int = None
    
    @computed_field
    @property
    def created_ago(self) -> str:
        return arrow.get(self.created_at).humanize()
    