from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(slots=True, frozen=True)
class CategoryOutput:
    id: str
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime