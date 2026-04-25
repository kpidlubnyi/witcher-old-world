import time
import uuid
import arrow

from pydantic import BaseModel, Field, computed_field, field_validator


class LobbyBase(BaseModel):
    name: str | None = None
    max_players: int = Field(default=4, ge=2, le=5)


class CreateLobby(LobbyBase):
    pass


class Lobby(LobbyBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    host_id: int
    host_name: str
    created_at: int = Field(default_factory=lambda: int(time.time()))

    @field_validator("name", mode="after")
    @classmethod
    def set_default_name(cls, v: str | None, info) -> str:
        if v:
            return v
        lobby_id = info.data.get("id", "unknown")
        return f"Lobby #{lobby_id[:8]}"


class LobbyResponse(Lobby):
    current_players: int = 1
    
    @computed_field
    @property
    def created_ago(self) -> str:
        return arrow.get(self.created_at).humanize()