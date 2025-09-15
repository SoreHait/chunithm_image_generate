from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal


class LxnsPlayer(BaseModel):
    name: str
    friend_code: int


class LxnsBestsRecordItem(BaseModel):
    id: int
    song_name: str
    level: str
    full_combo: Optional[str]
    score: Decimal
    level_index: int


class LxnsBestsRecords(BaseModel):
    bests: List[LxnsBestsRecordItem]
    currents: List[LxnsBestsRecordItem]
