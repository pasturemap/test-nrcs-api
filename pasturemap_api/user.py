import dataclasses
from typing import Optional
from uuid import UUID


@dataclasses.dataclass
class User:
    token: str
    email: str
    password: str
    ranch_uuid: Optional[UUID] = None
