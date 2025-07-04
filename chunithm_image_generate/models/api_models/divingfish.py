from pydantic import BaseModel
from typing import List
from decimal import Decimal


class DivingfishBestsRecordItem(BaseModel):
    ds: Decimal
    fc: str
    level: str
    level_index: int
    mid: int
    score: Decimal
    title: str


class DivingfishBestsRecords(BaseModel):
    b30: List[DivingfishBestsRecordItem]
    r10: List[DivingfishBestsRecordItem]


class DivingfishBests(BaseModel):
    nickname: str
    records: DivingfishBestsRecords
